from scipy import stats
import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import kpss
import statistics
from statsmodels.tsa.stattools import grangercausalitytests
import csv


def welch_ttest(x1,x2,n1,y1,y2,n2): 
    ## Welch-Satterthwaite Degrees of Freedom ##
    
    t, p = stats.ttest_ind_from_stats(x1,x2,n1,y1,y2,n2,equal_var = False)
    
    print("\n",
          f"Welch's t-test= {t}", "\n",
          f"p-value = {p}", "\n",)

    return t,p

N1=[n1,n2,n3,n4,n5,n6,n7,n8,n9,n10,n11,n12]
Communal_viral=[[x11,x12,x13],[x21,x22,x23], [x31,x32,x33],[x41,x42,x43],[x51,x52,x53],[x61,x62,x63],[x71,x72,x73],[x81,x82,x83],[x91,x92,x93],[x101,x102,x103],[x111,x112,x113],[x121,x122,x123]]
X=Communal_viral

N2 = [n1,n2,n3,n4,n5,n6,n7,n8,n9,n10,n11,n12]

Communal_non= [[x11,x12,x13],[x21,x22,x23], [x31,x32,x33],[x41,x42,x43],[x51,x52,x53],[x61,x62,x63],[x71,x72,x73],[x81,x82,x83],[x91,x92,x93],[x101,x102,x103],[x111,x112,x113],[x121,x122,x123]]
Y=Communal_non


j=0
final=[]
for i in range(len(X)):
	x1,x2,x3=X[i][0],X[i][1],X[i][2]
	n1=N1[i]
	y1,y2=Y[i][0],Y[i][1]
	n2=N2[i]
	j=j+5
	print("Minutes ::::",j)
	t,p=welch_ttest(x1,x2,n1,y1,y2,n2)
	y=[]
	y.append("No of Nodes")
	y.append("Communal_non")
	y.append(j)
	y.append(t)
	y.append(p)
	final.append(y)


myfile = open('T_Test.csv','w')
wrtr = csv.writer(myfile, delimiter=',', quotechar='"')
for row in final:
    wrtr.writerow(row)
    myfile.flush() # whenever you want, and/or
myfile.close()
