import pandas as pd
from string import ascii_letters
import datetime

df = pd.read_excel(r'voter-list.xlsx')

# get column names
list(df.columns)

# print first row
df.iloc[0]

df_clean = df.drop(df[
            (df['Street_Dir_Suffix'] == "**") | (df['Street_Name'].map(type)==float)
            ].index) #remove bad data for Street Dir Suffix and

def streets_to_lowercase(street_name):
    res = []
    for index, c in enumerate(street_name):
        if c.isalpha():
            res.append(street_name[index].lower())
        else:
            res.append(street_name[index])
    return ''.join(res)

# Clean relevant columns for ordering and determining ANC district
df_clean['Street_Type'] = df_clean['Street_Type'].apply(str.lower)
df_clean['Street_Dir_Suffix'] = df_clean['Street_Dir_Suffix'].map(lambda x: x.lower() if isinstance(x, str) else x)
df_clean['Street_Name'] = df_clean['Street_Name'].apply(streets_to_lowercase)
df_clean['Street_Number'] = df['Street_Number'].map(lambda x: x.rstrip(ascii_letters) if isinstance(x, str) else x)
df_clean['Street_Number'] = df['Street_Number'].astype("int")

def get_addresses_from_df(df,min_street_num,max_street_num,street_name,street_type,quadrant,even_odd_all):
    temp = df.loc[
                    (df['Street_Name'] == street_name) & 
                    (df['Street_Type'] == street_type) & 
                    (df['Street_Number'] >= min_street_num) & 
                    (df['Street_Number'] <= max_street_num) &
                    (df['Street_Dir_Suffix'].str.lower() == quadrant)
                ]
    if even_odd_all == "even":
        return temp.loc[(temp['Street_Number']%2 == 0)]
    elif even_odd_all == "odd":
        return temp.loc[(temp['Street_Number']%2 == 1)]
    else:
        return temp


euclid = get_addresses_from_df(df_clean,700,999,"euclid","st","nw","all")
fairmont = get_addresses_from_df(df_clean,700,799,"fairmont","st","nw","even")
georgia = get_addresses_from_df(df_clean,2600,2699,"georgia","ave","nw","even")
sherman = get_addresses_from_df(df_clean,2251,2699,"sherman","ave","nw","odd")
ninth = get_addresses_from_df(df_clean,2300,2600,"9th","st","nw","all")
voters_df = pd.concat([euclid,fairmont,georgia,sherman,ninth], ignore_index=True, sort=False)
voters_df = voters_df.sort_values(by=["Street_Dir_Suffix","Street_Name","Street_Type","Street_Number"], axis = 0)

voters_df.to_csv("anc_voters.csv", index=False)

voters_df['Party'] = voters_df['Party'].apply(str.lower)


# Howard Plaza Towers - 2251 Sherman Ave NW (juniors and seniors)
howard = voters_df.loc[(voters_df['Street_Name'] == 'sherman') & (voters_df['Street_Number'] == 2251)].sort_values('Registration_Date')
howard_new = howard.loc[howard.Registration_Date >= pd.Timestamp(2018,9,1)]

# Trellis House - 2323 Sherman Ave NW
trellis = voters_df.loc[(voters_df['Street_Name'] == 'sherman') & (voters_df['Street_Number'] == 2323)].sort_values('Registration_Date')