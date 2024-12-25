import pandas as pd
import statistics

# Import clean file that contains fatigue/attendance data
df = pd.read_csv("Engineered Data/Strictness-Standings/eplfatigue.csv")

#Standardising referee names:
def StandardNames(index, name):
    if index <= 379:
        parts = name.split()
        if len(parts) > 1:
            return f"{parts[0][0]} {parts[1]}" #double check
        else:
            return name
        
    elif index <= 549:
        parts = name.replace('.','').split()
        if len(parts) > 1:
            return f"{parts[0][0]} {parts[-1]}"
        else:
            return name
    
    elif index <= 759:
        parts = name.replace(',','').replace('.','').split()
        if len(parts) > 1:
            return f"{parts[1][0]} {parts[0]}"
        else:
            return name
    elif index >= 1855 and index <= 1863:
        parts = name.split()
        if len(parts) > 1:
            return f"{parts[0][-1]} {parts[1]}"
        else:
            return name
    else:
        return name
        
df['Referee'] = df.apply(lambda row: StandardNames(row.name, row['Referee']), axis=1) 

# Define a lookup dictionary for inconsistent names
name_corrections = {
    "D Gallaghe": "D Gallagher",
    "D Gallagh": "D Gallagher"
}

# Apply corrections to the 'Referee' column
df['Referee'] = df['Referee'].apply(lambda name: name_corrections[name] if name in name_corrections else name)


#Initialising dictionaries to 0
refs = df['Referee'].unique() 
Y = {ref: 0 for ref in refs} 
R = {ref: 0 for ref in refs}
MatchCount = {ref: 0 for ref in refs}
strictness = {}

#Loop to count referee stats
for index, row in df.iterrows(): 
    ref = row['Referee']
    if pd.notna(ref):
        Y[ref] += row['AY'] + row['HY']
        R[ref] += row['AY'] + row['HY']
        MatchCount[ref] += 1

#Loop to evaluate referee strictness
for ref in refs:
    if MatchCount[ref] >0:
        strictness[ref] = (Y[ref] + 3*R[ref])/MatchCount[ref]
    else:
        strictness[ref] = 0

#Add to dataframe and add to CSV
df['Strictness'] = df['Referee'].map(strictness)
df.to_csv("Engineered Data/Strictness-Standings/eplfatiguestrictness.csv", index = False)