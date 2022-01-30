from scipy import stats
import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import kpss
import statistics
from statsmodels.tsa.stattools import grangercausalitytests
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import statsmodels.api as sm
import seaborn as sns

from scipy.stats import norm
from scipy import stats
import pylab
from scipy.stats import kstest, norm

##celeb################################
viral = []
print("celeb  viral***************:",stats.shapiro(viral))

nviral = []
print("celeb  nviral***************:",stats.shapiro(nviral))

##comm########################
viral = []
print("comm viral***************:",stats.shapiro(viral))

nviral = []
print("comm nviral***************:",stats.shapiro(nviral))

##politics######################
viral =  []
print("politics viral***************:",stats.shapiro(viral))

nviral = []
print("politics nviral***************:",stats.shapiro(nviral))

##prod###################################
viral = []
print("prod viral***************:",stats.shapiro(viral))

nviral =  []
print("prod nviral***************:",stats.shapiro(nviral))

#### results are as follows::::
#celeb  viral***************: ShapiroResult(statistic=0.9632120132446289, pvalue=0.828510046005249)
#celeb  nviral***************: ShapiroResult(statistic=0.9169479608535767, pvalue=0.2616336941719055)
#comm viral***************: ShapiroResult(statistic=0.9451097249984741, pvalue=0.5669428110122681)
#comm nviral***************: ShapiroResult(statistic=0.9541782736778259, pvalue=0.6986221671104431)
#politics viral***************: ShapiroResult(statistic=0.9103732109069824, pvalue=0.2157103419303894)
#politics nviral***************: ShapiroResult(statistic=0.8894777297973633, pvalue=0.11602722853422165)
#prod viral***************: ShapiroResult(statistic=0.9331579804420471, pvalue=0.41479024291038513)
#prod nviral***************: ShapiroResult(statistic=0.9331579804420471, pvalue=0.41479024291038513)
