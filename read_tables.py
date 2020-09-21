import pandas as pd
import os
import pathinfo

# impact factor
__if_file = os.path.join(pathinfo.src_dir(), 'tables', 'impact_df.xlsx')
# journal partition
__istic_file = os.path.join(pathinfo.src_dir(), 'tables', 'istic.xlsx')
#__cas_file = os.path.join(pathinfo.src_dir(), 'tables', 'cas.xlsx')

# dataframe
impact = pd.read_excel(__if_file, index_col=0, dtype=str)
istic = pd.read_excel(__istic_file, index_col=0, dtype=str)
#cas = pd.read_excel(__cas_file, index_col=0, dtype=str)

if __name__ == '__main__':
    print(impact)
    print('new england journal of medicine' in impact['periodical'].values)
    print(impact.columns)
    print(istic)
    print(istic.columns)