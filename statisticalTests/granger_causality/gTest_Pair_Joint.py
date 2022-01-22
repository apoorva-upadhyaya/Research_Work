import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from scipy import stats
from statsmodels.tsa.api import VAR
from statsmodels.tools.eval_measures import rmse, aic
import pickle
from statsmodels.tsa.stattools import kpss
import statistics
from statsmodels.tsa.stattools import grangercausalitytests
from statsmodels.stats.stattools import durbin_watson


def kpss_test(series, **kw):    
    statistic, p_value, n_lags, critical_values = kpss(series, **kw)
    # Format Output
    print(f'KPSS Statistic: {statistic}')
    print(f'p-value: {p_value}')
    print(f'num lags: {n_lags}')
    print('Critial Values:')
    for key, value in critical_values.items():
        print(f'   {key} : {value}')
    print(f'Result: The series is {"not " if p_value < 0.05 else ""}stationary')

def adful_test(series):
    result = adfuller(series)
    print('ADF Statistic series: %f' % result[0])
    print('p-value: %f' % result[1])
    if (result[1] < .05):
        print("stationary")


def grangers_causation_matrix(data, variables,maxlag_ip, test='ssr_ftest',verbose=False):    
    """Check Granger Causality of all possible combinations of the Time series.
    The rows are the response variable, columns are predictors. The values in the table 
    are the P-Values. P-Values lesser than the significance level (0.05), implies 
    the Null Hypothesis that the coefficients of the corresponding past values is 
    zero, that is, the X does not cause Y can be rejected.

    data      : pandas dataframe containing the time series variables
    variables : list containing names of the time series variables.
    """
    maxlag=maxlag_ip
    
    df = pd.DataFrame(np.zeros((len(variables), len(variables))), columns=variables, index=variables)
    df1 = pd.DataFrame(np.zeros((len(variables), len(variables))), columns=variables, index=variables)
    for c in df.columns:
        for r in df.index:
            test_result = grangercausalitytests(data[[r, c]], maxlag=maxlag, verbose=False)
            # print("test_result",test_result)
            p_values = [(test_result[i+1][0][test][1]) for i in range(maxlag)]
            # print("p_values",p_values)
            if verbose: print(f'Y = {r}, X = {c}, P Values = {p_values}')
            min_p_value = np.min(p_values)
            df.loc[r, c] = min_p_value
            s_values = [(test_result[i+1][0][test][0]) for i in range(maxlag)]
            # print("s_values",s_values)
            # if verbose: print(f'Y = {r}, X = {c}, P Values = {p_values}')
            min_s_value = np.min(s_values)
            df1.loc[r, c] = min_s_value
    df.columns = [var + '_x' for var in variables]
    df.index = [var + '_y' for var in variables]
    df1.columns = [var + '_x' for var in variables]
    df1.index = [var + '_y' for var in variables]
    print(df,df1)
    return df,df1




#### feature value (mean no of nodes) containing mean,stdev,variance for every 5 min time interval #############
Y1=[[y11,y12,y13],[y21,y22,y23], [y31,y32,y33],[y41,y42,y43],[y51,y52,y53],[y61,y62,y63],[y71,y72,y73],[y81,y82,y83],[y91,y92,y93],[y101,y102,y103],[y111,y112,y113],[y121,y122,y123]]

#### feature value (avg degree) containing mean,stdev,variance for every 5 min time interval #############
Y2=[[y11,y12,y13],[y21,y22,y23], [y31,y32,y33],[y41,y42,y43],[y51,y52,y53],[y61,y62,y63],[y71,y72,y73],[y81,y82,y83],[y91,y92,y93],[y101,y102,y103],[y111,y112,y113],[y121,y122,y123]]

############## No. of retweets per 5 min time interval for 1 hour ###########
Z1=[x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12]

#### X1,X2 contains mean feature values only per 5 min interval ####
X1=[]
for i in Y1:
	X1.append(i[0])

X2=[]
for i in Y2:
    X2.append(i[0])


X1=np.array(X1)
X1 = X1[~np.isnan(X1)]

X2=np.array(X2)
X2 = X2[~np.isnan(X2)]

Z1=np.array(Z1)
Z1 = Z1[~np.isnan(Z1)]


############## check whether series are statinary (if nt, try differencing the series and again check) ##########
kpss_test(X1)
kpss_test(X2)
kpss_test(Z1)

############ creating dataframe ########

df = pd.DataFrame(list(zip(Z1, X1)), columns =['Mean_Retweet','Feature'],index=None) 
df = df.dropna()
# print("df :::::",df)
# df = pd.read_csv('file.csv', index_col='time');

rawData = df.copy(deep=True)

# df['Feature'] = df['Feature'] - df['Feature'].shift(1)
# df['Mean_Retweet'] = df['Mean_Retweet'] - df['Mean_Retweet'].shift(1)

print("No of Nodes ################## ")
rawData = df.dropna()

####### VAR Model (use AIC value in selecting smallest lag order) #####
model = VAR(rawData)
for i in [1,2,3,4]:
    result = model.fit(i)
    try:
        print('Lag Order =', i)
        print('AIC : ', result.aic)
        print('BIC : ', result.bic)
        print('FPE : ', result.fpe)
        print('HQIC: ', result.hqic, '\n')
    except:
        continue

results = model.fit(maxlags=2, ic='aic')
results.summary()

#############

########## DUrbin Watson measures autocorrelation in residuals ######
out = durbin_watson(results.resid)
print("Dubin Watson Corelation Coefficients")
for col, val in zip(df.columns, out):
    print(col, ':', round(val, 2))


#############granger causality test returns p values and coefficients values matrices ##########

p,coeff = grangers_causation_matrix(df, variables = df.columns,maxlag_ip=2,test="ssr_chi2test") 

print("coeff,pvlue Retweet causes feature :::::::;",coeff.iloc[0,1],p.iloc[0,1])
print("coeff,pvlue Feature causes retweet::::::::",coeff.iloc[1,0],p.iloc[1,0])

########### Test other features similarly ###

############ creating dataframe ########

df = pd.DataFrame(list(zip(Z1, X2)), columns =['Mean_Retweet','Feature'],index=None) 
df = df.dropna()
# print("df :::::",df)
# df = pd.read_csv('file.csv', index_col='time');

rawData = df.copy(deep=True)

# df['Feature'] = df['Feature'] - df['Feature'].shift(1)
# df['Mean_Retweet'] = df['Mean_Retweet'] - df['Mean_Retweet'].shift(1)

print("Avg Degree ################## ")
rawData = df.dropna()

####### VAR Model (use AIC value in selecting smallest lag order) #####
model = VAR(rawData)
for i in [1,2,3,4]:
    result = model.fit(i)
    try:
        print('Lag Order =', i)
        print('AIC : ', result.aic)
        print('BIC : ', result.bic)
        print('FPE : ', result.fpe)
        print('HQIC: ', result.hqic, '\n')
    except:
        continue

results = model.fit(maxlags=2, ic='aic')
results.summary()

#############

########## DUrbin Watson measures autocorrelation in residuals ######
out = durbin_watson(results.resid)
print("Dubin Watson Corelation Coefficients")
for col, val in zip(df.columns, out):
    print(col, ':', round(val, 2))


#############granger causality test returns p values and coefficients values matrices ##########

p,coeff = grangers_causation_matrix(df, variables = df.columns,maxlag_ip=2,test="ssr_chi2test") 

print("coeff,pvlue Retweet causes feature :::::::;",coeff.iloc[0,1],p.iloc[0,1])
print("coeff,pvlue Feature causes retweet::::::::",coeff.iloc[1,0],p.iloc[1,0])

# df = pd.DataFrame(list(zip(Z1, X2)), columns =['Mean_Retweet','Feature'],index=None) 

###Results indicate X1 has causality with Z1 but X2 does not have significant p values, hence no causality ###


################check for joint features casuality with retweet ###

df = pd.DataFrame(
    {'nnodes': X1,'deg': X2,'tweet': Z1
    })

df = df.dropna()
# print("df :::::",df)
# df = pd.read_csv('file.csv', index_col='time');

rawData = df.copy(deep=True)

# df['Feature'] = df['Feature'] - df['Feature'].shift(1)
# df['Mean_Retweet'] = df['Mean_Retweet'] - df['Mean_Retweet'].shift(1)

print("Joint Model ################## ")
rawData = df.dropna()

####### VAR Model (use AIC value in selecting smallest lag order) #####
model = VAR(rawData)
for i in [1,2,3,4]:
    result = model.fit(i)
    try:
        print('Lag Order =', i)
        print('AIC : ', result.aic)
        print('BIC : ', result.bic)
        print('FPE : ', result.fpe)
        print('HQIC: ', result.hqic, '\n')
    except:
        continue

results = model.fit(maxlags=2, ic='aic')
results.summary()

#############

########## DUrbin Watson measures autocorrelation in residuals ######
out = durbin_watson(results.resid)
print("Dubin Watson Corelation Coefficients")
for col, val in zip(df.columns, out):
    print(col, ':', round(val, 2))


#############granger causality test returns p values and coefficients values matrices ##########

p,coeff = grangers_causation_matrix(df, variables = df.columns,maxlag_ip=2,test="ssr_chi2test") 

print("coeff,pvlue Retweet causes feature :::::::;",coeff.iloc[0,1],p.iloc[0,1])
print("coeff,pvlue Feature causes retweet::::::::",coeff.iloc[1,0],p.iloc[1,0])
