
from numpy import array
import json
import  random
from sklearn.preprocessing import MinMaxScaler
import ast
from sklearn.metrics import accuracy_score,classification_report, confusion_matrix
from sklearn import svm


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


#Create a svm Classifier
model = svm.SVC(kernel='rbf')

model.fit(train_data, train_labels)

pred = model.predict(test_data)
print(pred)

test_accuracy=accuracy_score(test_labels, pred)
print("test accuracy::::",test_accuracy)

class_rep=classification_report(test_labels, pred)
print("specific confusion matrix",confusion_matrix(test_labels, pred))
print(class_rep)