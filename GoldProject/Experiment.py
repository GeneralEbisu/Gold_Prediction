import Raw_Data_Preprocessing_ver2, MovingAverage_ver3
from df_type_partition import df_type_partition
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import linear_model


def predict_gold():
    data = MovingAverage_ver3.MA_multi_ndays_for_all_numeric(Raw_Data_Preprocessing_ver2.get_data(), [5,10,25,50,100,200],include_df=True)
    data = data.dropna()
    data1 = df_type_partition(data)
    data_numeric = data1.numeric_partition
    X = data_numeric.loc[:, data_numeric.columns != 'Last']
    y = data_numeric[['Last']]
    our_model = linear_model.LinearRegression()
    our_model.fit(X, y)
    
    y_prediction = float(our_model.predict(X.iloc[-1,:].reshape(1, -1)))
    y_actual = data['Last'][-1]
    error = abs(y_prediction - y_actual)
    
    #Return a dataframe
    out1 = pd.DataFrame({'y_prediction':[y_prediction],
                         'y_actual':[y_actual],
                         'Error':[error],
                         'Date':[Raw_Data_Preprocessing_ver2.get_data().index[-1].date()]})
    
    return out1.set_index('Date') #Set Date column as index


def test_run():
    print(predict_gold())
    

if __name__ == '__main__':
    test_run()








