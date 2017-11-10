import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsRegressor

from pandas import Series, DataFrame
#import quandl

##########################################################################################################################################################


def get_data():
    d = get_raw_gold()
    d = d.iloc[::-1] #or d = d.sort_index(axis=1 ,ascending=True)
    d['Date'] = pd.to_datetime(d['Date'])
    d.set_index('Date', inplace=True)
    d = d.drop(['Change'], axis=1) # Drop 'Change'
    return apply_funcs_to_df(d, 'Last', 'Open', 'High', 'Low')
    
def get_raw_gold(APIdata="https://www.quandl.com/api/v3/datasets/CHRIS/CME_GC2.csv?api_key=<API_Key>&collapse=monthly"):
    return pd.read_csv(APIdata) # a DataFrame


def apply_funcs_to_df(df, *cols):
    return Increasing_Decreasing(Previous_Difference(Calc_Diff_OCHL(df),*cols),*cols)

def Calc_Diff_OCHL(df):
    d_OC = (df['Open']-df['Last']).apply(np.abs).to_frame(name='OpenCloseDiff')
    d_HL = (df['High']-df['Low']).to_frame(name='HighLowDiff')
    return pd.concat([df,d_OC,d_HL], axis=1)

def Previous_Difference(df,*cols):
    # e.g. cols = ['Last', 'Open', 'High', 'Low']
    prev_diff = lambda s,col_name: s.rolling(2).apply(lambda x:abs(x[0]-x[1])).to_frame(name='{}Diff'.format(col_name))
    return pd.concat([df]+[prev_diff(df[col],col) for col in cols], axis=1)

def Increasing_Decreasing(df,*cols):
    # e.g. cols = ['Last', 'Open', 'High', 'Low']
    prev_diff = lambda s,col_name: s.rolling(2)\
    .apply(lambda x: 1 if x[1]>x[0] else -1)\
    .to_frame(name='{}IncrDecr'.format(col_name))\
    .applymap(lambda x: 'Increasing' if x==1.0 else 'Decreasing')
    return pd.concat([df]+[prev_diff(df[col],col) for col in cols], axis=1)


def print_to_excel(df, filename):
    writer = pd.ExcelWriter(f'{filename}.xlsx')
    df.to_excel(writer,'Sheet1')
    writer.save()


def test_run():
#    print(get_raw_gold())
#    print(get_data())
#    print(get_data().columns)
#    print(get_data().dtypes)
#    print_to_excel(get_data(),'TestGoldData')
    pass


if __name__ == '__main__':
    test_run()








