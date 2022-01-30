from scipy import stats
import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import kpss
import statistics
from statsmodels.tsa.stattools import grangercausalitytests
import csv
import random


######### viral::
print("VIRAL :::::::::::::::::")

Communal=[]

X=Communal


Politics= []

Y=Politics


print("communal vs politics 60mins ::",stats.ttest_ind(X, Y, equal_var=False))

Celeb= []

Y=Celeb


print("communal vs Celeb 60mins ::",stats.ttest_ind(X, Y, equal_var=False))


Product=[]

Y=Product


print("communal vs Product 60mins ::",stats.ttest_ind(X, Y, equal_var=False))


################## non viral
print("NON VIRAL :::::::::::::::::")

Communal= []

X=Communal

Politics=[]

Y=Politics

print("communal vs politics 60mins ::",stats.ttest_ind(X, Y, equal_var=False))


Celeb=[]

Y=Celeb


print("communal vs Celeb 60mins ::",stats.ttest_ind(X, Y, equal_var=False))

Product= []
Y=Product


print("communal vs Product 60mins ::",stats.ttest_ind(X, Y, equal_var=False))


########## viral vs non-viral
Communal_viral=[]
X=Communal_viral


Communal_non=[]

Y=Communal_non

print("communal vs Communal_non 60mins ::",stats.ttest_ind(X, Y, equal_var=False))

Politics_viral= []

X=Politics_viral


politics_non=[]

Y=politics_non

print("Politics_viral vs politics_non 60mins ::",stats.ttest_ind(X, Y, equal_var=False))

celeb_viral=[]

X=celeb_viral

celeb_non=[]

Y=celeb_non

print("celeb_viral vs celeb_non 60mins ::",stats.ttest_ind(X, Y, equal_var=False))

product_viral=[]
X=product_viral


product_non=  []

Y=product_non


print("product_viral vs product_non 60mins ::",stats.ttest_ind(X, Y, equal_var=False))

VIRAL :::::::::::::::::
communal vs politics 60mins :: Ttest_indResult(statistic=10.987260205072872, pvalue=5.5603653961444505e-09)
communal vs Celeb 60mins :: Ttest_indResult(statistic=20.224815191757493, pvalue=6.4071767631739526e-15)
communal vs Product 60mins :: Ttest_indResult(statistic=16.65361108010712, pvalue=3.065254461312997e-11)
NON VIRAL :::::::::::::::::
communal vs politics 60mins :: Ttest_indResult(statistic=3.2640796946486157, pvalue=0.0042742278001756465)
communal vs Celeb 60mins :: Ttest_indResult(statistic=15.571922731061925, pvalue=6.173815882565714e-13)
communal vs Product 60mins :: Ttest_indResult(statistic=13.405205945619615, pvalue=4.004491315619702e-11)
communal vs Communal_non 60mins :: Ttest_indResult(statistic=13.394936680421162, pvalue=6.787244384013615e-10)
Politics_viral vs politics_non 60mins :: Ttest_indResult(statistic=5.765366927527877, pvalue=1.3615236367704924e-05)
celeb_viral vs celeb_non 60mins :: Ttest_indResult(statistic=1.1538277206927252, pvalue=0.26162550287361985)
