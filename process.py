import pandas as pd
from string import ascii_letters
import datetime

df = pd.read_excel(r'voter-list.xlsx')

# get column names
list(df.columns)

# print first row
df.iloc[0]

# Get NW data
dfnw = df.loc[df['Street_Dir_Suffix'].str.lower() == 'nw']

# Make relevant columns lower case
dfnw['Street_Type'] = dfnw['Street_Type'].apply(str.lower)
dfnw['Street_Name'] = dfnw['Street_Name'].map(lambda x: x.lower() if isinstance(x, str) else x)
dfnw['Street_Number'] = dfnw['Street_Number'].map(lambda x: x.rstrip(ascii_letters) if isinstance(x, str) else x)
dfnw['Street_Number'] = dfnw['Street_Number'].astype("int")

# Euclid St NW from 700 -> 999 (all)
euclid = dfnw.loc[(dfnw['Street_Name'] == 'euclid') & (dfnw['Street_Type'] == 'st') & (dfnw['Street_Number'] >= 700) & (dfnw['Street_Number'] <= 999)]

# Fairmont St NW from 700 -> 799 (evens)
fairmount = dfnw.loc[(dfnw['Street_Name'] == 'fairmont') & (dfnw['Street_Type'] == 'st') & (dfnw['Street_Number'] >= 700) & (dfnw['Street_Number'] <= 799) & (dfnw['Street_Number']%2 == 0)]

# Georgia Ave NW from 2600 -> 2699 (evens)
georgia = dfnw.loc[(dfnw['Street_Name'] == 'georgia') & (dfnw['Street_Type'] == 'ave') & (dfnw['Street_Number'] >= 2600) & (dfnw['Street_Number'] <= 2699) & (dfnw['Street_Number']%2 == 0)]

# Sherman Ave NW from 2251 - 2699 (odds)
sherman = dfnw.loc[(dfnw['Street_Name'] == 'sherman') & (dfnw['Street_Type'] == 'ave') & (dfnw['Street_Number'] >= 2251) & (dfnw['Street_Number'] <= 2699) & (dfnw['Street_Number']%2 == 1)]

# 9th St NW from 2300 -> 2600 (all)
ninth = dfnw.loc[((dfnw['Street_Name'] == '9th') | (dfnw['Street_Name'] == '9TH') | (dfnw['Street_Name'] == '9Th')) & (dfnw['Street_Type'] == 'st') & (dfnw['Street_Number'] >= 2300) & (dfnw['Street_Number'] <= 2600)]

# Voters
voters_df = pd.concat([euclid,fairmount,georgia,sherman,ninth], ignore_index=True, sort=False)
voters_df['Party'] = voters_df['Party'].apply(str.lower)

# Howard Plaza Towers - 2251 Sherman Ave NW (juniors and seniors)
howard = voters_df.loc[(voters_df['Street_Name'] == 'sherman') & (voters_df['Street_Number'] == 2251)].sort_values('Registration_Date')

howard_new = howard.loc[howard.Registration_Date >= pd.Timestamp(2018,9,1)]

# Trellis House - 2323 Sherman Ave NW
trellis = voters_df.loc[(voters_df['Street_Name'] == 'sherman') & (voters_df['Street_Number'] == 2323)].sort_values('Registration_Date')

voters_df['Party'].value_counts()