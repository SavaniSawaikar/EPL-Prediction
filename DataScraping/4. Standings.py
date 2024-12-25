import pandas as pd
from tqdm import tqdm

tqdm.pandas()

# Import clean file that contains fatigue/attendance/strictness data
df = pd.read_csv('eplfatiguestrictness.csv')

dfFTR = df
#Changing the FTR columns to indicate the name of the winner to simplify the codes below
dfFTR['FTR'] = dfFTR.apply(lambda row: row['HomeTeam'] if row['FTR']=='H' else ('Draw' if row['FTR'] == 'D' else row['AwayTeam']), axis=1)

#Adding season round # values
dfFTR['Season'] = dfFTR.index // 380
dfFTR['Season'] = dfFTR['Season'].apply(lambda i: 2000 + i)

roundindex = (dfFTR.index - 10) // 10 + 1
dfFTR['Round'] = (roundindex % 38) + 1 

#Calculation algorithm of team points across rounds and seasons
def get_pts(team, season, round):
    '''
    e.g. (season = 2018) == (season = 2018-2019)
    '''
    if round == 1:
        return 0
    
    prevround = dfFTR[
        (dfFTR['Season'] == season) & 
        (dfFTR['Round'] == round-1)
    ]
    
    #Checking if the team won:
    homewin = (prevround['HomeTeam'] == team) & (prevround['FTR'] == team)
    awaywin = (prevround['AwayTeam'] == team) & (prevround['FTR'] == team)
    draw = ((prevround['HomeTeam'] == team) | (prevround['AwayTeam'] == team)) & (prevround['FTR'] == 'Draw')

    if homewin.any() or awaywin.any():
        roundpts = 3
    elif draw.any():
        roundpts = 1
    else:
        roundpts = 0
    
    return roundpts + get_pts(team, season, round-1)


dfFTR['Hpts'] = dfFTR.progress_apply(lambda row: get_pts(row['HomeTeam'], row['Season'], row['Round']), axis=1)
dfFTR['Apts'] = dfFTR.progress_apply(lambda row: get_pts(row['AwayTeam'], row['Season'], row['Round']), axis=1)

#Reversing the FTR column into what it used to be
dfFTR['FTR'] = dfFTR.progress_apply(lambda row: 'H' if row['FTR']==row['HomeTeam'] else ('D' if row['FTR']=='Draw' else 'A'), axis=1)

dfFTR.to_csv('Engineered Data/Strictness-Standings/FatigueStrictnessStandings.csv', index=False)