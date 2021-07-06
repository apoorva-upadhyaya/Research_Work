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
Y1=[[9.444444444444445, 8.762292952063277, 76.77777777777779], [13.666666666666666, 9.565563234854496, 91.5], [8.894736842105264, 7.015021476502369, 49.21052631578947], [9.681818181818182, 8.703509766242712, 75.75108225108227], [9.88888888888889, 10.31926254570449, 106.48717948717949], [9.5, 7.994610253379978, 63.91379310344828], [9.545454545454545, 8.958553556137387, 80.25568181818181], [11.2, 9.600245094910491, 92.16470588235295], [12.95, 13.522915024846927, 182.86923076923077], [12.936170212765957, 11.84575553286116, 140.3219241443108], [13.89090909090909, 15.585692307812467, 242.91380471380472], [16.210526315789473, 19.990834365944224, 399.63345864661653]]

#### feature value (avg degree) containing mean,stdev,variance for every 5 min time interval #############
Y2=[[1.7555555555555555, 0.5277485372016852, 0.2785185185185185], [2.3532316630355845, 2.452940808815036, 6.016918611550164], [2.1820616883116886, 4.691411838247801, 22.009345036051613], [3.4676237024624124, 5.685517526446004, 32.32510954352469], [4.6964830975700542, 2.8326308395826234, 8.023797473354557], [5.280731772257954, 13.829766452096655, 191.26244011953807], [5.975626115998472, 7.355721567487309, 54.10663977839795], [6.627031280597777, 14.48711788383328, 209.87658458008207], [6.9794481642963424, 3.7683652346617067, 14.200576541806981], [7.0551136474249, 9.070597981303585, 82.27574773842869], [7.28890325331746, 8.954898038734784, 80.19019888413608], [7.309613525704945, 8.05320157028956, 64.85405553171421]]

############## No. of retweets per 5 min time interval for 1 hour ###########
Z1=[95,162,201,242,286,327, 381, 454, 609, 708, 868, 1068]

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