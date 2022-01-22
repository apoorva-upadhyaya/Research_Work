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
Communal=[[x11,x12,x13],[x21,x22,x23], [x31,x32,x33],[x41,x42,x43],[x51,x52,x53],[x61,x62,x63],[x71,x72,x73],[x81,x82,x83],[x91,x92,x93],[x101,x102,x103],[x111,x112,x113],[x121,x122,x123]]

X=Communal

N2=[N1,N2,N3,N4,N5,N6,N7,N8,N9,N10,N11,N12]

Celebrity=[[y11,y12,y13],[y21,y22,y23], [y31,y32,y33],[y41,y42,y43],[y51,y52,y53],[y61,y62,y63],[y71,y72,y73],[y81,y82,y83],[y91,y92,y93],[y101,y102,y103],[y111,y112,y113],[y121,y122,y123]]

Y=Celebrity


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
	y.append("Celebrity")
	y.append(j)
	y.append(t)
	y.append(dof)
	final.append(y)

N2=[P1,P2,P3,P4,P5,P6,P7,P8,P9,P10,P11,P12]
Politics=[[p11,p12,p13],[p21,p22,p23], [p31,p32,p33],[p41,p42,p43],[p51,p52,p53],[p61,p62,p63],[p71,p72,p73],[p81,p82,p83],[p91,p92,p93],[p101,p102,p103],[p111,p112,p113],[p121,p122,p123]]
Y=Politics

j=0
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
	y.append("Politics")
	y.append(j)
	y.append(t)
	y.append(p)
	final.append(y)


N2=[Pr1,Pr2,Pr3,Pr4,Pr5,Pr6,Pr7,Pr8,Pr9,Pr10,Pr11,Pr12]
Product=[[pr11,pr12,pr13],[pr21,pr22,pr23], [pr31,pr32,pr33],[pr41,pr42,pr43],[pr51,pr52,pr53],[pr61,pr62,pr63],[pr71,pr72,pr73],[pr81,pr82,pr83],[pr91,pr92,pr93],[pr101,pr102,pr103],[pr111,pr112,pr113],[pr121,pr122,pr123]]
Y=Product

j=0
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
	y.append("Product")
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
