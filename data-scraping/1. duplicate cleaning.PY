import pandas as pd

epl = pd.read_csv('epl-training.csv')

NSeasons = 24
MatchesPerSeason = 380
ExpectedLength = NSeasons*MatchesPerSeason

print(f'Length of epl before is {len(epl)}, which is {len(epl)-ExpectedLength} longer than expected')

#removing empty rows
epl = epl.dropna(how='all')

duplicates = epl.iloc[:, :3].duplicated()
if duplicates.any():
    dupindex = duplicates[duplicates].index.tolist()
    print(f"Duplicate rows found at indices {dupindex}")
    print(f'there are {len(dupindex)} duplicates')
else:
    print("All rows in the first three columns of epl are unique")

# Eliminate duplicate rows with the indices stored in dupindex
epl = epl.drop(dupindex)
print(f"Duplicate rows have been removed and length is now {len(epl)}")

epl.to_csv('Engineered Data/Fatigue/eplclean.csv',index=False)