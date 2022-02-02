import numpy as np
import  random
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.metrics import accuracy_score,classification_report, confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import statsmodels.api as sm
from sklearn import svm

import numpy as np
import pandas as pd

from sklearn.feature_selection import mutual_info_classif
from sklearn.datasets import make_classification




label=[]
nodes_viral=[]
with open("viral/nodes.txt",'r',encoding='utf-8') as file:
    for line in file:
        line=line
        id_=line
        nodes_viral.append(float(id_))
        label.append(1)

deg_viral=[]
with open("viral/deg.txt",'r',encoding='utf-8') as file:
    for line in file:
        line=line
        id_=line
        deg_viral.append(float(id_))


gc_viral=[]
with open("viral/gc.txt",'r',encoding='utf-8') as file:
    for line in file:
        line=line
        id_=line
        gc_viral.append(float(id_))


cc_viral=[]
with open("viral/cc.txt",'r',encoding='utf-8') as file:
    for line in file:
        line=line
        id_=line
        cc_viral.append(float(id_))


recp_viral=[]
with open("viral/recp.txt",'r',encoding='utf-8') as file:
    for line in file:
        line=line
        id_=line
        recp_viral.append(float(id_))


sv_viral=[]
with open("viral/sv.txt",'r',encoding='utf-8') as file:
    for line in file:
        line=line
        id_=line
        sv_viral.append(float(id_))


depth_viral=[]
with open("viral/depth.txt",'r',encoding='utf-8') as file:
    for line in file:
        line=line
        id_=line
        depth_viral.append(float(id_))


useract_viral=[]
with open("viral/user_act.txt",'r',encoding='utf-8') as file:
    for line in file:
        line=line
        id_=line
        useract_viral.append(float(id_))


userbehav_viral=[]
with open("viral/user_behav.txt",'r',encoding='utf-8') as file:
    for line in file:
        line=line
        id_=line
        userbehav_viral.append(float(id_))


neg_viral=[]
with open("viral/neg.txt",'r',encoding='utf-8') as file:
    for line in file:
        line=line
        id_=line
        neg_viral.append(float(id_))


anger_viral=[]
with open("viral/anger.txt",'r',encoding='utf-8') as file:
    for line in file:
        line=line
        id_=line
        anger_viral.append(float(id_))


power_viral=[]
with open("viral/power.txt",'r',encoding='utf-8') as file:
    for line in file:
        line=line
        id_=line
        power_viral.append(float(id_))


################################ non viral

nodes_non_viral=[]
with open("non_viral/nodes.txt",'r',encoding='utf-8') as file:
    for line in file:
        line=line
        id_=line
        nodes_non_viral.append(float(id_))
        # nodes_viral.append(float(id_))
        label.append(0)

deg_non_viral=[]
with open("non_viral/deg.txt",'r',encoding='utf-8') as file:
    for line in file:
        line=line
        id_=line
        deg_non_viral.append(float(id_))
        # deg_viral.append(float(id_))


gc_non_viral=[]
with open("non_viral/gc.txt",'r',encoding='utf-8') as file:
    for line in file:
        line=line
        id_=line
        gc_non_viral.append(float(id_))
        # gc_viral.append(float(id_))


cc_non_viral=[]
with open("non_viral/cc.txt",'r',encoding='utf-8') as file:
    for line in file:
        line=line
        id_=line
        cc_non_viral.append(float(id_))
        # cc_viral.append(float(id_))



recp_non_viral=[]
with open("non_viral/recp.txt",'r',encoding='utf-8') as file:
    for line in file:
        line=line
        id_=line
        recp_non_viral.append(float(id_))
        # recp_viral.append(float(id_))



sv_non_viral=[]
with open("non_viral/sv.txt",'r',encoding='utf-8') as file:
    for line in file:
        line=line
        id_=line
        sv_non_viral.append(float(id_))
        # sv_viral.append(float(id_))


depth_non_viral=[]
with open("non_viral/depth.txt",'r',encoding='utf-8') as file:
    for line in file:
        line=line
        id_=line
        depth_non_viral.append(float(id_))
        # depth_viral.append(float(id_))


useract_non_viral=[]
with open("non_viral/user_act.txt",'r',encoding='utf-8') as file:
    for line in file:
        line=line
        id_=line
        useract_non_viral.append(float(id_))
        # useract_viral.append(float(id_))


userbehav_non_viral=[]
with open("non_viral/user_behav.txt",'r',encoding='utf-8') as file:
    for line in file:
        line=line
        id_=line
        userbehav_non_viral.append(float(id_))
        # userbehav_viral.append(float(id_))


neg_non_viral=[]
with open("non_viral/neg.txt",'r',encoding='utf-8') as file:
    for line in file:
        line=line
        id_=line
        neg_non_viral.append(float(id_))
        # neg_viral.append(float(id_))


anger_non_viral=[]
with open("non_viral/anger.txt",'r',encoding='utf-8') as file:
    for line in file:
        line=line
        id_=line
        anger_non_viral.append(float(id_))
        # anger_viral.append(float(id_))


power_non_viral=[]
with open("non_viral/power.txt",'r',encoding='utf-8') as file:
    for line in file:
        line=line
        id_=line
        power_non_viral.append(float(id_))
        # power_viral.append(float(id_))



train_data=[]

tot=len(nodes_viral) 

train_label=[]

dataset=[]

for i in range(len(nodes_viral)):
    y=[]
    y.append(nodes_viral[i])
    y.append(deg_viral[i])
    y.append(gc_viral[i])
    y.append(cc_viral[i])
    y.append(recp_viral[i])
    y.append(sv_viral[i])
    y.append(depth_viral[i])
    y.append(useract_viral[i])
    y.append(userbehav_viral[i])
    y.append(neg_viral[i])
    y.append(anger_viral[i])
    y.append(power_viral[i])
    y.append(1)
    dataset.append(y)


for i in range(len(nodes_non_viral)):
    y=[]
    y.append(nodes_non_viral[i])
    y.append(deg_non_viral[i])
    y.append(gc_non_viral[i])
    y.append(cc_non_viral[i])
    y.append(recp_non_viral[i])
    y.append(sv_non_viral[i])
    y.append(depth_non_viral[i])
    y.append(useract_non_viral[i])
    y.append(userbehav_non_viral[i])
    y.append(neg_non_viral[i])
    y.append(anger_non_viral[i])
    y.append(power_non_viral[i])
    y.append(0)
    dataset.append(y)


random.shuffle(dataset)
random.shuffle(dataset)
random.shuffle(dataset)


tot=len(nodes_viral) + len(nodes_non_viral)

X_celeb,Y_celeb=[],[]
X_comm,Y_comm=[],[]
X_pol,Y_pol=[],[]
X_pro,Y_pro=[],[]

for i in range(tot):
    y=[]
    y.append(dataset[i][0])
    y.append(dataset[i][2])
    y.append(dataset[i][3])
    y.append(dataset[i][7])
    X_celeb.append(y)
    Y_celeb.append(dataset[i][12])


X_train_celeb, X_test_celeb, y_train_celeb, y_test_celeb = train_test_split(X_celeb, Y_celeb, test_size=0.2)



######## communal domain

for i in range(tot):
    y=[]
    y.append(dataset[i][0])
    y.append(dataset[i][1])
    y.append(dataset[i][4])
    y.append(dataset[i][5])
    y.append(dataset[i][6])
    y.append(dataset[i][8])
    y.append(dataset[i][9])
    y.append(dataset[i][10])
    y.append(dataset[i][11])
    X_comm.append(y)
    Y_comm.append(dataset[i][12])


X_train_comm, X_test_comm, y_train_comm, y_test_comm = train_test_split(X_comm, Y_comm, test_size=0.2)

############## politics domain ##############


for i in range(tot):
    y=[]
    y.append(dataset[i][0])
    y.append(dataset[i][2])
    y.append(dataset[i][4])
    y.append(dataset[i][5])
    y.append(dataset[i][6])
    y.append(dataset[i][11])
    X_pol.append(y)
    Y_pol.append(dataset[i][12])


X_train_pol, X_test_pol, y_train_pol, y_test_pol = train_test_split(X_pol, Y_pol, test_size=0.2)


############## product domain ##############


for i in range(tot):
    y=[]
    y.append(dataset[i][0])
    y.append(dataset[i][1])
    y.append(dataset[i][2])
    y.append(dataset[i][3])
    y.append(dataset[i][5])
    y.append(dataset[i][6])
    y.append(dataset[i][7])
    X_pro.append(y)
    Y_pro.append(dataset[i][12])


X_train_pro, X_test_pro, y_train_pro, y_test_pro = train_test_split(X_pro, Y_pro, test_size=0.2)

################## scaling all feature values #######

scaler = StandardScaler()
scaler.fit(X_train_celeb)
X_train_celeb=scaler.transform(X_train_celeb)
X_test_celeb=scaler.transform(X_test_celeb)


scaler = StandardScaler()
scaler.fit(X_train_comm)
X_train_comm=scaler.transform(X_train_comm)
X_test_comm=scaler.transform(X_test_comm)

scaler = StandardScaler()
scaler.fit(X_train_pol)
X_train_pol=scaler.transform(X_train_pol)
X_test_pol=scaler.transform(X_test_pol)

scaler = StandardScaler()
scaler.fit(X_train_pro)
X_train_pro=scaler.transform(X_train_pro)
X_test_pro=scaler.transform(X_test_pro)

X_train_celeb=np.array(X_train_celeb)
y_train_celeb=np.array(y_train_celeb)
X_test_celeb=np.array(X_test_celeb)
y_test_celeb=np.array(y_test_celeb)


X_train_comm=np.array(X_train_comm)
y_train_comm=np.array(y_train_comm)
X_test_comm=np.array(X_test_comm)
y_test_comm=np.array(y_test_comm)


X_train_pol=np.array(X_train_pol)
y_train_pol=np.array(y_train_pol)
X_test_pol=np.array(X_test_pol)
y_test_pol=np.array(y_test_pol)


X_train_pro=np.array(X_train_pro)
y_train_pro=np.array(y_train_pro)
X_test_pro=np.array(X_test_pro)
y_test_pro=np.array(y_test_pro)


################# decision tree classifier ################
print("DecisionTreeClassifier #################")

model = DecisionTreeClassifier(criterion = "entropy")
model.fit(X_train_celeb, y_train_celeb)
pred = model.predict(X_test_celeb)
# print("pred:",pred)
acc=accuracy_score(y_test_celeb, pred)
print("celeb attributes ***************")
print("accuracy ::::",acc)
class_rep=classification_report(y_test_celeb, pred)
print("class_rep::::::",class_rep)

### communal
model = DecisionTreeClassifier(criterion = "entropy")
model.fit(X_train_comm, y_train_comm)
pred = model.predict(X_test_comm)
# print("pred:",pred)
acc=accuracy_score(y_test_comm, pred)
print("communal attributes ***************")
print("accuracy ::::",acc)
class_rep=classification_report(y_test_comm, pred)
print("class_rep::::::",class_rep)

### politics
model = DecisionTreeClassifier(criterion = "entropy")
model.fit(X_train_pol, y_train_pol)
pred = model.predict(X_test_pol)
# print("pred:",pred)
acc=accuracy_score(y_test_pol, pred)
print("politics attributes ***************")
print("accuracy ::::",acc)
class_rep=classification_report(y_test_pol, pred)
print("class_rep::::::",class_rep)


### product
model = DecisionTreeClassifier(criterion = "entropy")
model.fit(X_train_pro, y_train_pro)
pred = model.predict(X_test_pro)
# print("pred:",pred)
acc=accuracy_score(y_test_pro, pred)
print("product attributes ***************")
print("accuracy ::::",acc)
class_rep=classification_report(y_test_pro, pred)
print("class_rep::::::",class_rep)

############## Random forest classifier ##################

print("RandomForestClassifier #################")

model = RandomForestClassifier(n_estimators=30, random_state=50, verbose = 1)
model.fit(X_train_celeb, y_train_celeb)
pred = model.predict(X_test_celeb)
# print("pred:",pred)
acc=accuracy_score(y_test_celeb, pred)
print("celeb attributes ***************")
print("accuracy ::::",acc)
class_rep=classification_report(y_test_celeb, pred)
print("class_rep::::::",class_rep)

### communal
model = RandomForestClassifier(n_estimators=30, random_state=50, verbose = 1)
model.fit(X_train_comm, y_train_comm)
pred = model.predict(X_test_comm)
# print("pred:",pred)
acc=accuracy_score(y_test_comm, pred)
print("communal attributes ***************")
print("accuracy ::::",acc)
class_rep=classification_report(y_test_comm, pred)
print("class_rep::::::",class_rep)

### politics
model = RandomForestClassifier(n_estimators=30, random_state=50, verbose = 1)
model.fit(X_train_pol, y_train_pol)
pred = model.predict(X_test_pol)
# print("pred:",pred)
acc=accuracy_score(y_test_pol, pred)
print("politics attributes ***************")
print("accuracy ::::",acc)
class_rep=classification_report(y_test_pol, pred)
print("class_rep::::::",class_rep)


### product
model = RandomForestClassifier(n_estimators=30, random_state=50, verbose = 1)
model.fit(X_train_pro, y_train_pro)
pred = model.predict(X_test_pro)
# print("pred:",pred)
acc=accuracy_score(y_test_pro, pred)
print("product attributes ***************")
print("accuracy ::::",acc)
class_rep=classification_report(y_test_pro, pred)
print("class_rep::::::",class_rep)


################## SVM ################


model = svm.SVC(kernel='linear')
model.fit(X_train_celeb, y_train_celeb)
pred = model.predict(X_test_celeb)
# print("pred:",pred)
acc=accuracy_score(y_test_celeb, pred)
print("celeb attributes ***************")
print("accuracy ::::",acc)
class_rep=classification_report(y_test_celeb, pred)
print("class_rep::::::",class_rep)
print("coefficients",model.coef_)

### communal
model = svm.SVC(kernel='linear')
model.fit(X_train_comm, y_train_comm)
pred = model.predict(X_test_comm)
# print("pred:",pred)
acc=accuracy_score(y_test_comm, pred)
print("communal attributes ***************")
print("accuracy ::::",acc)
class_rep=classification_report(y_test_comm, pred)
print("class_rep::::::",class_rep)
print("coefficients",model.coef_)

### politics
model = svm.SVC(kernel='linear')
model.fit(X_train_pol, y_train_pol)
pred = model.predict(X_test_pol)
# print("pred:",pred)
acc=accuracy_score(y_test_pol, pred)
print("politics attributes ***************")
print("accuracy ::::",acc)
class_rep=classification_report(y_test_pol, pred)
print("class_rep::::::",class_rep)
print("coefficients",model.coef_)


### product
model = svm.SVC(kernel='linear')
model.fit(X_train_pol, y_train_pol)
pred = model.predict(X_test_pol)
# print("pred:",pred)
acc=accuracy_score(y_test_pro, pred)
print("product attributes ***************")
print("accuracy ::::",acc)
class_rep=classification_report(y_test_pro, pred)
print("coefficients",model.coef_)
print("class_rep::::::",class_rep)
