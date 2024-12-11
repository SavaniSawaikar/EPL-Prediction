import pandas as pd

# Import clean file that contains fatigue/attendance/strictness data
cleanepl = pd.read_csv('UpToNormalisedFatigue.csv')
MarketVal = pd.read_csv('Scraped Data/MarketValues.csv')
Posession = pd.read_csv('Scraped Data/PosessionData.csv')
SetPiece = pd.read_csv('Scraped Data/SetPiece.csv')


Alterations = {
    'Manchester City': 'Man City',
    'Arsenal FC': 'Arsenal',
    'Chelsea FC': 'Chelsea',
    'Liverpool FC': 'Liverpool',
    'Manchester United': 'Man United',
    'Tottenham Hotspur': 'Tottenham',
    'Newcastle United': 'Newcastle',
    'Brighton & Hove Albion': 'Brighton',
    'West Ham United': 'West Ham',
    'Nottingham Forest': "Nott'm Forest",
    'Brentford FC': 'Brentford',
    'Wolverhampton Wanderers': 'Wolves',
    'AFC Bournemouth': 'Bournemouth',
    'Everton FC': 'Everton',
    'Fulham FC': 'Fulham',
    'Southampton FC': 'Southampton',
    'Leicester City': 'Leicester',
    'Ipswich Town': 'Ipswich',
    'West Bromwich Albion': 'West Brom',
    'Queens Park Rangers': 'QPR',
    'Hull City': 'Hull',
    'Stoke City': 'Stoke',
    'Swansea City': 'Swansea',
    'Manchester Utd': 'Man United',
    'Newcastle Utd': 'Newcastle',
    "Nott'ham Forest": "Nott'm Forest",
    "Luton Town": "Luton",
    'Sheffield Utd': 'Sheffield United',
    'Leeds United': 'Leeds',
    'Norwich City': 'Norwich',
    'Cardiff City': 'Cardiff',
    'Birmingham City': 'Birmingham',
    'Blackburn Rovers': 'Blackburn',
    'Blackpool FC': 'Blackpool',
    'Bolton Wanderers': 'Bolton',
    'Bradford City': 'Bradford',
    'Burnley FC': 'Burnley',
    'Charlton Athletic': 'Charlton',
    'Coventry City': 'Coventry',
    'Derby County': 'Derby',
    'Huddersfield Town': 'Huddersfield',
    'Middlesbrough FC': 'Middlesbrough',
    'Portsmouth FC': 'Portsmouth',
    'Reading FC': 'Reading',
    'Sunderland AFC': 'Sunderland',
    'Watford FC': 'Watford',
    'Wigan Athletic': 'Wigan',
               }

MarketVal['Club'] = MarketVal['Club'].apply(lambda name: Alterations[name] if name in Alterations else name)
SetPiece['Team'] = SetPiece['Team'].apply(lambda name: Alterations[name] if name in Alterations else name)
Posession['Team'] = Posession['Team'].apply(lambda name: Alterations[name] if name in Alterations else name)

# Checking if all names are covered in the dictionary
cleaneplteams = list(cleanepl['HomeTeam'].unique())
MarketValteams = list(MarketVal['Club'].unique())
Posessionteams = list(Posession['Team'].unique())
setPieceteams = list(SetPiece['Team'].unique())
print(len(cleaneplteams),len(MarketValteams),len(Posessionteams), len(setPieceteams))
uniqueepl = sorted([team for team in cleaneplteams if team not in MarketValteams])
UniqueMarketVal = sorted([team for team in MarketValteams if team not in cleaneplteams])
UniquePosession = [team for team in Posessionteams if team not in cleaneplteams]
UniqueSetPiece = [team for team in setPieceteams if team not in cleaneplteams]

# Applying the dictionary to the dataframes
MarketVal['Club'] = MarketVal['Club'].apply(lambda name: Alterations[name] if name in Alterations else name)
SetPiece['Team'] = SetPiece['Team'].apply(lambda name: Alterations[name] if name in Alterations else name)
Posession['Team'] = Posession['Team'].apply(lambda name: Alterations[name] if name in Alterations else name)


# Cleaning the market value data
MarketVal['TMV'] = MarketVal['TMV'].apply(
    lambda value: float(str(value)[:-2]) * 1000 if isinstance(value, str) and value[-2:] == 'bn' else 
                  float(str(value)[:-1]) if isinstance(value, str) and value[-1] == 'm' else 
                  value
)

#Transferring market values to the cleanepl df
MarketVal = MarketVal[['Club', 'Year', 'TMV']]
print(MarketVal.head())

cleanepl = pd.merge(
    cleanepl,
    MarketVal.rename(columns={'Club':'HomeTeam', 'TMV':'HTV', 'Year':'Season'}),
    how='left',
    on=['HomeTeam', 'Season'],
)

cleanepl = pd.merge(
    cleanepl,
    MarketVal.rename(columns={'Club':'AwayTeam', 'TMV':'ATV', 'Year':'Season'}),
    how='left',
    on=['AwayTeam', 'Season'],
)


# Transferring posession data to the clean epl df
Posession['year'] = Posession['year'].apply(lambda name: name[:4])
Posession['year'] = Posession['year'].astype(int)
Posession['Poss'] = Posession['Poss'].apply(lambda pos: pos/100)
Posession = Posession[['Team', 'Poss', 'year']]
print(Posession.head())

cleanepl = pd.merge(
    cleanepl,
    Posession.rename(columns={'Team':'HomeTeam', 'Poss':'HTAvgPos', 'year':'Season'}),
    how='left',
    on= ['HomeTeam', 'Season']
)

cleanepl = pd.merge(
    cleanepl,
    Posession.rename(columns={'Team':'AwayTeam', 'Poss':'ATAvgPos', 'year':'Season'}),
    how='left',
    on= ['AwayTeam', 'Season']
)

#Transferring set piece values
SetPiece = SetPiece.dropna()
SetPiece['Season'] = SetPiece['Season'].apply(lambda year: year[:4]).astype(int)
SetPiece = SetPiece[['Season','Team','Set Piece Efficiency (%)','Penalty Efficiency (%)']]

cleanepl = pd.merge(
    cleanepl,
    SetPiece.rename(columns={'Team':'HomeTeam','Set Piece Efficiency (%)': 'Home SPE (%)', 'Penalty Efficiency (%)': 'Home PE (%)'}),
    how='left',
    on=['HomeTeam','Season']
)

cleanepl = pd.merge(
    cleanepl,
    SetPiece.rename(columns={'Team':'AwayTeam', 'Set Piece Efficiency (%)': 'Away SPE (%)', 'Penalty Efficiency (%)': 'Away PE (%)'}),
    how='left',
    on=['AwayTeam','Season']
)


cleanepl.to_csv('ALLDATAtest.csv')