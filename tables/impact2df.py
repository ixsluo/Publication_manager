# from txt to dataframe to excel
import pandas as pd

impact_df = pd.read_table(
    'impact.txt',
    usecols=[0, 1],
    header=0,
)
# change title
impact_df.rename(columns={
    'Full Journal Title': 'periodical',
    'Journal Impact Factor': '2019',
}, inplace=True)
print(impact_df.columns)

# to string
impact_df.periodical = impact_df.periodical.astype(str)
impact_df['2019'] = impact_df['2019'].astype(str)
# title to lower
impact_df.periodical = impact_df.periodical.str.lower()
# strip
impact_df.periodical = impact_df.periodical.str.strip()
impact_df['2019'] = impact_df['2019'].str.strip()
#print(impact_df)

title1 = 'new england journal of medicine'

# to dict
impact_dict = impact_df.set_index('periodical')['2019'].to_dict()
#print(impact_dict)
if title1 in impact_dict.keys():
    print(title1, impact_dict[title1])

with pd.ExcelWriter('impact_df.xlsx') as writer:
    impact_df.to_excel(writer)