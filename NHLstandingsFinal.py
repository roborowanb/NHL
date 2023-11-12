# Import the requests library.
import requests
import pandas as pd
import pygsheets
import datetime




# NHL standings API Call.
nhl_url = "https://statsapi.web.nhl.com/api/v1/standings/byLeague"
nhl_standings_raw = requests.get(nhl_url)
standings_json = nhl_standings_raw.json()

records_parse = []
for i in standings_json['records']:
    records_parse.append(i)
df_raw = pd.DataFrame(records_parse)
print(df_raw)

df = df_raw.explode('teamRecords')

oo=pd.json_normalize(df['teamRecords']).apply(pd.Series)

final_df = oo[['team.name', 'points', 'gamesPlayed']]
print(final_df)




# Google sheet update
my_path = 'c:\\Users\\Rowan\\NHL\\clever-span-353301-da89d891f9c6.json'
spreadsheet_id= "1-pPKqK3UBoFmQW9cFqnPoou_53Uf7QUeoCL1BbbRbww"
sheet_name = "DataPull"


def write_to_gsheet(service_file_path, spreadsheet_id, sheet_name, standings_df):
    """
    this function takes data_df and writes it under spreadsheet_id
    and sheet_name using your credentials under service_file_path
    """
    gc = pygsheets.authorize(service_file=service_file_path)
    sh = gc.open_by_key(spreadsheet_id)
    try:
        sh.add_worksheet(sheet_name)
    except:
        pass
    wks_write = sh.worksheet_by_title(sheet_name)
    wks_write.clear('A1',None,'*')
    wks_write.set_dataframe(standings_df, (1,1), encoding='utf-8', fit=True)
    wks_write.frozen_rows = 1

write_to_gsheet(my_path, spreadsheet_id, sheet_name, final_df)

# x = datetime.datetime.now()
# print(x)


print("done")