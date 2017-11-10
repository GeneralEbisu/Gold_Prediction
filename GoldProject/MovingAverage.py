import pandas as pd
import numpy as np
import Raw_Data_Preprocessing_ver2
import matplotlib.pyplot as plt

import math
############################################################################################################
"""
Conventions:
    example: var = d['Last']
"""

__all__=["apply_functions",
         "MA",
         "ROC",
         "Bollinger_Bands",
         "MA_multi_ndays",
         "MA_for_all_numeric",
         "MA_multi_ndays_for_all_numeric"]

############################################################################################################
#--------Test Data--------#
def data():
	return Raw_Data_Preprocessing_ver2.get_data()
############################################################################################################
def MA(s, ndays=100):
    return s.rolling(window=ndays, min_periods=ndays).mean()

def ROC(s, ndays=20): # s-->s
    M = s.diff(ndays-1)
    N = s.shift(ndays-1)
    ROC_out = (M/N) # Convert Series to DataFrame.
    return ROC_out

def Bollinger_Bands(s, K=2.5, ndays=25, out_as='tuple'):
    bb_ma = s.rolling(window=ndays).mean()
    bb_std = s.rolling(window=ndays).std()
    bb_ub = (bb_ma + bb_std*K)
    bb_lb = (bb_ma - bb_std*K)
    
    
    if out_as == 'dataframe':
        bb_ub = bb_ub.to_frame(name='Bollinger_Bands_Upper_Band')
        bb_lb = bb_lb.to_frame(name='Bollinger_Bands_Lower_Band')
        bb_ma = bb_ma.to_frame(name='Bollinger_Bands_Moving_Average')
        return pd.concat([bb_ub, bb_ma, bb_lb], axis=1) # Return as dataframe.
    elif out_as == 'tuple':
        return bb_ub, bb_ma, bb_lb # Return as tuple
############################################################################################################
#--------Apply Indicators--------#
def apply_functions(df=Raw_Data_Preprocessing_ver2.get_data()):
    f1 = MA_multi_ndays_for_all_numeric(df, [2,3,4,5,6,7,8,9,10,25,50,100,150,200], include_df=True)
    f2 = ROC_of_Prices(f1, 20, include_df=True)
    f3 = BB_of_Prices(f2, include_df=True)
    return f3
############################################################################################################
# ROC
def ROC_of_Prices(df, ndays, include_df=False):
    out1 = {'{}_{}_ROC'.format(column,ndays): ROC(df[column], ndays=ndays) for column in ['Last', 'High', 'Low', 'Open', 'Volume']}
    if include_df == False:
        return pd.DataFrame(out1)
    else:
        return pd.concat([df, pd.DataFrame(out1)], axis=1)
###########################################################################################################
# Bollinger Bands
def BB_of_Prices(df, K=2.5, ndays=25, include_df=False):
    out1 = {'{}_BB_UB'.format(column): Bollinger_Bands(df[column], K=K, ndays=ndays)[0] for column in ['Last', 'High', 'Low', 'Open', 'Volume']}
    out2 = {'{}_BB_MA'.format(column): Bollinger_Bands(df[column], K=K, ndays=ndays)[1] for column in ['Last', 'High', 'Low', 'Open', 'Volume']}
    out3 = {'{}_BB_LB'.format(column): Bollinger_Bands(df[column], K=K, ndays=ndays)[2] for column in ['Last', 'High', 'Low', 'Open', 'Volume']}
    
    out1 = pd.DataFrame(out1)
    out2 = pd.DataFrame(out2)
    out3 = pd.DataFrame(out3)
    
    if include_df == False:
        return pd.concat([out1, out2, out3], axis=1)
    else:
        return pd.concat([df, out1, out2, out3], axis=1)
###########################################################################################################
def MA_multi_ndays(s, iter_n, include_s=False):
    out1 = {'{}_{}_MA'.format(s.name,n):MA(s,ndays=n) for n in iter_n}
    if include_s == False:
        return pd.DataFrame(out1)
    else:
        return pd.concat([s.to_frame(), pd.DataFrame(out1)], axis=1)

def MA_for_all_numeric(df, ndays=100, include_df=False):
    col_types = [np.float, np.float64, np.int, np.int64]
    col_list = [col for col in df.columns if df[col].dtype in col_types]
    dict1 = {"{}_{}_MA".format(col,ndays):MA(df[col], ndays=ndays) for col in col_list}
    if include_df==False:
        return pd.DataFrame(dict1)
    else:
        return pd.concat([df, pd.DataFrame(dict1)], axis=1)

def MA_multi_ndays_for_all_numeric(df, iter_n, include_df=False):
    df_temp = {'{}'.format(n):MA_for_all_numeric(df, ndays=n) for n in iter_n}
    list_temp = list(df_temp.values()) 
    df_out = pd.concat(list_temp, axis=1)
    if include_df == False:
        return df_out #Return a dataframe, excluding var.
    elif include_df == True:
        return pd.concat([df, df_out], axis=1) #Return a dataframe, including var.
############################################################################################################
#--------Utilities--------#
def print_to_excel(df, filename):
    writer = pd.ExcelWriter(f'{filename}.xlsx')
    df.to_excel(writer,'Sheet1')
    writer.save()

############################################################################################################
# --------Test--------#

def test_run():
    d = data()
    dd = apply_functions()
    print_to_excel(dd, 'Gold_with_Features')
    pass
    
   
if __name__ == '__main__':
   test_run()
