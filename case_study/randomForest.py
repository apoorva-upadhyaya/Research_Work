
from numpy import array
from sklearn.ensemble import RandomForestClassifier
import json
import  random
from sklearn.preprocessing import MinMaxScaler
import ast
from sklearn.metrics import accuracy_score,classification_report, confusion_matrix
from sklearn.tree import DecisionTreeClassifier

train_data=[]
with open("data/train_data.txt",'r',encoding='utf-8') as file:
        for line in file:
            data=line
            data=ast.literal_eval(data)
            train_data.append((data))


test_data=[]
with open("data/test_data.txt",'r',encoding='utf-8') as file:
        for line in file:
            data=line
            data=ast.literal_eval(data)
            test_data.append((data))

train_labels=[]
with open("data/train_labels.txt",'r',encoding='utf-8') as file:
        for line in file:
            label=line
            train_labels.append(int(label))

test_labels=[]
with open("data/test_labels.txt",'r',encoding='utf-8') as file:
        for line in file:
            label=line
            test_data.append(int(label))

# scaler = MinMaxScaler()
# scaler.fit(train_data)
# train_data=scaler.transform(train_data)

# scaler.fit(test_data)
# test_data=scaler.transform(test_data)


RSEED = 100

model = RandomForestClassifier(n_estimators=30, random_state=RSEED, verbose = 1)

model.fit(train_data, train_labels)

pred = model.predict(test_data)
print(pred)

test_accuracy=accuracy_score(test_labels, pred)
print("test accuracy::::",test_accuracy)

class_rep=classification_report(test_labels, pred)
print("specific confusion matrix",confusion_matrix(test_labels, pred))
print(class_rep)