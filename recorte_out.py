import pandas as pd
import numpy as np

def remove_outliers(train_df, test_df, parametro):
    flag_out_train=pd.DataFrame()
    flag_out_test=pd.DataFrame()

    columnas = train_df.columns
    for i in columnas:
        iqr = train_df[i].quantile(parametro/100) - train_df[i].quantile((100-parametro)/100)
        flag_out_train[i]=(train_df[i]< np.percentile(train_df[i], 100-parametro)-1.5*iqr) | (train_df[i]> np.percentile(train_df[i], parametro)+1.5*iqr)
        flag_out_train[i+"_lim_inf"] = ( train_df[i]< np.percentile(train_df[i], 100-parametro)-1.5*iqr ) 
        flag_out_train[i+"_lim_sup"] = ( train_df[i]> np.percentile(train_df[i], parametro)+1.5*iqr )
        
        flag_out_test[i]=(test_df[i]< np.percentile(train_df[i], 100-parametro)-1.5*iqr) | (test_df[i]> np.percentile(train_df[i], parametro)+1.5*iqr)
        flag_out_test[i+"_lim_inf"] = ( test_df[i]< np.percentile(train_df[i], 100-parametro)-1.5*iqr ) 
        flag_out_test[i+"_lim_sup"] = ( test_df[i]> np.percentile(train_df[i], parametro)+1.5*iqr )

    for c in columnas:
        q75 = train_df[c].quantile(parametro/100)
        q25 = train_df[c].quantile((100-parametro)/100)
        idx = train_df[ (flag_out_train[c]==True) & (flag_out_train[c+"_lim_sup"]==True) ].index.values
        if(len(idx)>0):
             train_df[c] = np.where( (flag_out_train[c]==True) & (flag_out_train[c+"_lim_sup"]==True)  , q75, train_df[c])
             test_df[c] = np.where( (flag_out_test[c]==True) & (flag_out_test[c+"_lim_sup"]==True)  , q75, test_df[c])

        idx = train_df[ (flag_out_train[c]==True) & (flag_out_train[c+"_lim_inf"]==True) ].index.values
        if(len(idx)>0):
            train_df[c] = np.where( (flag_out_train[c]==True) & (flag_out_train[c+"_lim_inf"]==True)  , q25, train_df[c])
            test_df[c] = np.where( (flag_out_test[c]==True) & (flag_out_test[c+"_lim_inf"]==True)  , q25, test_df[c])

    return train_df, test_df
