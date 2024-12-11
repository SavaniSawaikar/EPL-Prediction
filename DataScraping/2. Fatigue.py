import pandas as pd
from datetime import timedelta
from tqdm import tqdm

#Importing data scraping files (EPL teams' matches in other comptetitions)
EPL = pd.read_csv('COMBINED_EPL.csv') #this is a similar dataframe to epltraining, yet it has the advantage of having attendance data
FA = pd.read_csv('COMBINED_FA_E.csv')
EFL = pd.read_csv('COMBINED_EFL_E.csv')
UCL = pd.read_csv('COMBINED_UCL_E.csv')
UEL = pd.read_csv('COMBINED_UEL_E.csv')
#Importing clean epltraining file
epltraining = pd.read_csv('Engineered Data/Fatigue/Data/EPL-training-C.csv')

#Combining data scraping files into a single dataframe
EPL.insert(0, 'df name', 'EPL')
FA.insert(0, 'df name', 'FA')
EFL.insert(0, 'df name', 'EFL')
UCL.insert(0, 'df name', 'UCL')
UEL.insert(0, 'df name', 'UEL')
combined = pd.concat([EPL, FA, EFL, UCL, UEL])

#Just to ensure the correct date format
epltraining['Date'] = pd.to_datetime(epltraining['Date'])
combined['Date'] = pd.to_datetime(combined['Date'])

combined.sort_values(['Date','HomeTeam'], ascending=[True, True], inplace=True)

#Calculating A14/H14 "14-day match density" algorithm:
def calculate_matches(team, match_date):
    StartDate = match_date - timedelta(days=14)
    matches = combined[
        ((combined["HomeTeam"]==team) | (combined['AwayTeam']==team)) &
        (combined['Date'] >= StartDate) &
        (combined['Date'] < match_date)
        ]
    return len(matches)

combined_epl = combined[combined['df name'] == 'EPL']

combined_epl['H14'] = combined_epl.apply(lambda row: calculate_matches(row['HomeTeam'], row['Date']), axis=1)
combined_epl['A14'] = combined_epl.apply(lambda row: calculate_matches(row['AwayTeam'], row['Date']), axis=1)

#Merging the combined dataframe with the clean epltraining dataframe to add the A14/H14 + Attendance columns
epltraining = epltraining.merge(
    combined_epl[['Date', 'HomeTeam', 'AwayTeam', 'H14', 'A14', 'Attendance']],
    on= ['Date', 'HomeTeam', 'AwayTeam'],
    how='left'
)

#Fixing the Date format
epltraining['Date'] = epltraining['Date'].dt.strftime('%d/%m/%Y')

epltraining.to_csv('Engineered Data/Fatigue/eplfatigue.csv', index=False)