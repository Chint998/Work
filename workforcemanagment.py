from datetime import datetime, timedelta
import pandas as pd

# Function to create table
def create_table(teams, peaks):
    # Initialize table
    table = pd.DataFrame()
    
    # Iterate through teams
    for i in range(len(teams)):
        team = teams[i]
        peak = peaks[i]
        
        # Get start date
        if team['start_date'] == None:
            start_date = team['milestone1_date'] - timedelta(days=90)
        else:
            start_date = team['start_date']
        
        # Get end date
        if team['end_date'] == None:
            end_date = team['milestone3_date'] + timedelta(days=180)
        else:
            end_date = team['end_date']
        
        # Get difference between start date and milestone1 date
        diff1 = (team['milestone1_date'] - start_date).days / 30
        
        # Get difference between milestone3 date and end date
        diff2 = (end_date - team['milestone3_date']).days / 30
        
        # Create dataframe for team
        team_df = pd.DataFrame(index=[team['name']], columns=pd.date_range(start_date, end_date, freq='MS'))
        
        # Fill dataframe with values
        team_df.loc[team['name'], start_date:team['milestone1_date']] = peak * 0.8 if diff1 == 1 else peak * 0.9 if diff1 == 2 else peak * 0.5
        team_df.loc[team['name'], team['milestone1_date']:team['milestone2_date']] = peak
        team_df.loc[team['name'], team['milestone2_date']:team['milestone3_date']] = peak
        team_df.loc[team['name'], team['milestone3_date']:end_date] = peak * 0.6 if diff2 == 1 else peak * 0.5 if diff2 == 2 else peak * 0.9
        
        # Append team dataframe to table
        table = pd.concat([table, team_df], axis=0)
    
    return table

# Example usage
teams = [{'name': 'Team 1', 'start_date': datetime(2022, 1, 1), 'milestone1_date': datetime(2022, 3, 1), 'milestone2_date': datetime(2022, 6, 1), 'milestone3_date': datetime(2022, 9, 1), 'end_date': datetime(2023, 1, 1)},
         {'name': 'Team 2', 'start_date': None, 'milestone1_date': datetime(2022, 2, 1), 'milestone2_date': datetime(2022, 5, 1), 'milestone3_date': datetime(2022, 8, 1), 'end_date': None}]
peaks = [100, 150]
table = create_table(teams, peaks)
print(table)
table.to_csv("WorkForcemanagment")