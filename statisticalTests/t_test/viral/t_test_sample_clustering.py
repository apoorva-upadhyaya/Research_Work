from scipy import stats
import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import kpss
import statistics
from statsmodels.tsa.stattools import grangercausalitytests
import csv


def welch_ttest(x1,x2,x3,n1,y1,y2,y3,n2): 
    ## Welch-Satterthwaite Degrees of Freedom ##
    dof = (x3/n1 + y3/n2)**2 / ((x3/n1)**2 / (n1-1) + (y3/n2)**2 / (n2-1))
    dof = (((x2)**2)/n1 + ((y2)**2)/n2)**2 / ((((x2)**2)/n1)**2 / (n1-1) + (((y2)**2)/n2)**2 / (n2-1))
    t, p = stats.ttest_ind_from_stats(x1,x2,n1,y1,y2,n2,equal_var = False)
    
    print("\n",
          f"Welch's t-test= {t}", "\n",
          f"p-value = {p}", "\n",
          f"Welch-Satterthwaite Degrees of Freedom= {dof:.4f}")

    return t,p,dof

# N1=[8, 9, 10, 13, 15, 18, 21, 23, 25, 26, 31, 35]
N1=[9, 14, 19, 22, 27, 30, 33, 35, 40, 47, 55, 60]
# Communal= [[1.2956778499278498, 2.711073807891004, 7.349921191832629],[1.8098244277090432, 2.1571992296210194, 4.653508516277519],[2.074074074074074, 2.4657126395296047, 6.0797388207360505],[2.9988949844151707, 1.8301167900905726, 3.349327465371421], [2.8923454490665277, 4.056347277700524, 16.453953237308447],[3.1656065861166893, 2.908992881279247, 8.462239583333334],[3.714267746344232, 5.059232901100186, 25.595837547574607],[3.679989888934922, 5.416612462355202, 29.339690567341687],[3.9775790644540643, 2.081419506619085, 4.332307162534435],[4.037790646232143, 3.137618602763751, 9.844650496409153],[5.217544317505718, 7.960505761688764, 63.36965198188001],[6.530503054447099, 7.972396164728007, 63.559100607369835]]

Communal= [[0.16911559649156843, 0.10867500982953085, 0.011810257761448626], [0.2290579173615016, 0.1334509481177091, 0.01780915555351549], [0.1963457917006025, 0.08855812614276996, 0.007842541705918757], [0.23349682460758334, 0.06728901333798758, 0.004527811315999871], [0.24505446222546112, 0.0760293177047048, 0.0057804571506429375], [0.2668355808733887, 0.10384025788733187, 0.010782799158107589], [0.20804727243002835, 0.07555594853744003, 0.005708701359392287], [0.2655597287488239, 0.1449809045925937, 0.021019462696486756], [0.2104239836132102, 0.05468042397757203, 0.002989948766367034], [0.24691008992184366, 0.15325462428236075, 0.023486979863927556], [0.20527573189428644, 0.08502233890269349, 0.007228798112484468], [0.22525679819293512, 0.0843133308846019, 0.007108737764856364]]

X=Communal

N2=[6, 7, 8 ,  11 ,  14,  15,   16, 17   , 21, 22, 24 , 27]

Celebrity= [[0.3043027509321399, 0.07336789853986064, 0.005382848536155286],[0.2956231218225273, 0.046272716097135146, 0.00214116425500607],[0.2818475288881162, 0.05257973321306295, 0.0027646283447568753], [0.27972216525720917, 0.04079188316815028, 0.008243166049219049],[0.2504772171910914, 0.0666662874282364, 0.005877771962789951],[0.2938646505171976, 0.05042202292260785, 0.0025423803956079916],[0.27382933768664175, 0.06372301549515764, 0.004060622703796102], [0.2667330933335794, 0.05574109085492681, 0.003107069209697205], [0.26371618557351284, 0.05483503190180825, 0.003006880723672329],[0.25663822569310246, 0.0899077879210988, 0.00808341032886528],[0.21760275789014477, 0.08764326473134529, 0.007681341852768674],[0.20330278865766519, 0.10519625683167873, 0.011066252451396514]]
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
	t,p,dof=welch_ttest(x1,x2,x3,n1,y1,y2,0,n2)
	y=[]
	y.append("No of Nodes")
	y.append("Celebrity")
	y.append(j)
	y.append(t)
	y.append(p)
	y.append(dof)
	final.append(y)

N2=[5, 7, 9, 13, 17, 19, 23, 24, 25, 27, 29, 30]
Politics=[[0.35966322938810413, 0.10412250683261198, 0.01084149642910733], [0.33469180307794255, 0.1291387945779585, 0.016676828265048158],[0.30000283443933584, 0.09327996009825527, 0.008701150955932097],[0.2882358725531455, 0.10693880925181551, 0.011435908924196183],[0.2968008418730337, 0.08943072907670552, 0.0079978553031911], [0.29180111287375604, 0.08457183960368024, 0.007152396053950617], [0.26268011126008567, 0.09921520187385194, 0.009843656282869194],[0.2659625175812898, 0.13736611736543905, 0.018869450200055572], [0.2506824939727938, 0.0965126753066972, 0.009314696494855959], [0.23080815025729737, 0.08476846674687157, 0.007185692954615471],[0.24657817696223547, 0.10430365817106688, 0.010879253107866766],[0.20112273381921927, 0.0738846089251961, 0.0054589354360291675]]
Y=Politics

j=0
for i in range(len(X)):
	x1,x2,x3=X[i][0],X[i][1],X[i][2]
	n1=N1[i]
	y1,y2=Y[i][0],Y[i][1]
	n2=N2[i]
	j=j+5
	print("Minutes ::::",j)
	t,p,dof=welch_ttest(x1,x2,x3,n1,y1,y2,0,n2)
	y=[]
	y.append("No of Nodes")
	y.append("Politics")
	y.append(j)
	y.append(t)
	y.append(p)
	y.append(dof)
	final.append(y)


N2=[5, 6, 11, 12,  15  ,  17, 19 , 20,22, 24, 25, 26  ]
Product= [[0.21611111111111111, 0.09245008972987526, 0.037037037037037035], [0.2050537634408602, 0.0048087483387092254, 2.3124060585038733e-05], [0.19000131388779397, 0.01699797108464401, 0.0002889310209943939], [0.14347961406784935, 0.02366639308710144, 0.0005600981617532029], [0.138917114246298265, 0.010327610600426317, 0.00010665954071403802], [0.13130775032367203, 0.021027586492049586, 0.00044215939368062615], [0.120838410049079326, 0.02320810009407104, 0.0005386159099764203], [0.1356338342681882425, 0.10664320800339418, 0.011372773813255197], [0.12885321027830776, 0.021313142858811772, 0.00045425005852011926], [0.112211538598781827, 0.018555956595197355, 0.00034432352516284816], [0.11007499285856657334, 0.04501978474728137, 0.002026781018691548], [0.102576872148830399, 0.026911423092093833, 0.0007242246928416813]]
Y=Product

j=0
for i in range(len(X)):
	x1,x2,x3=X[i][0],X[i][1],X[i][2]
	n1=N1[i]
	y1,y2=Y[i][0],Y[i][1]
	n2=N2[i]
	j=j+5
	print("Minutes ::::",j)
	t,p,dof=welch_ttest(x1,x2,x3,n1,y1,y2,0,n2)
	y=[]
	y.append("No of Nodes")
	y.append("Product")
	y.append(j)
	y.append(t)
	y.append(p)
	y.append(dof)
	final.append(y)

myfile = open('T_Test.csv','w')
wrtr = csv.writer(myfile, delimiter=',', quotechar='"')
for row in final:
    wrtr.writerow(row)
    myfile.flush() # whenever you want, and/or
myfile.close()