import pandas as pd
import os
import pathinfo

__if_file = os.path.join(pathinfo.src_dir(), 'impact', 'impact_df.xlsx')

# dataframe
df = pd.read_excel(__if_file, index_col=0, dtype=str)


if __name__ == '__main__':
    print(df)
    print('new england journal of medicine' in df['periodical'].values)
    print(df.columns)