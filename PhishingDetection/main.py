# -*- coding: utf-8 -*-
"""
Created on Sun May 19 16:33:04 2019

@author: Niveditha Patil
"""

import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.linear_model import LogisticRegression

import Extract_features, sys
#url=sys.argv[1]
url='https://chained-advancement.000webhostapp.com/next.php'

df = pd.read_csv('D:\Machine learning\Phishing\Training Dataset.csv', header =0)

#df.isnull().values.any()

def categorical_to_numeric(x):
    if x==-1:
        return 0
    if x==1:
        return 1
df['Result'] = df['Result'].apply(categorical_to_numeric)

X=df.iloc[:,:30]
y=df.iloc[:,-1:]

#dropped the following columns since they had lower ranking (RFE)
"""from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.30,random_state=101)
columns = X_train.columns
from imblearn.over_sampling import SMOTE
os = SMOTE(random_state=0)
os_data_X,os_data_y=os.fit_sample(X_train, y_train.values.ravel())
os_data_X = pd.DataFrame(data=os_data_X,columns=columns )
os_data_y= pd.DataFrame(data=os_data_y,columns=['y'])

rfe = RFE(logreg, 20)
rfe = rfe.fit(os_data_X, os_data_y.values.ravel())
print(rfe.support_)
print(rfe.ranking_)
"""

X = df.drop(df.columns[[1,4,8,12,17,19,20,21,23,26,30]], axis=1) 

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.30,random_state=101)

from sklearn.linear_model import LogisticRegression
#create an instance and fit the model 
logmodel = LogisticRegression(solver='lbfgs')
logmodel.fit(X_train, y_train.values.ravel())

#logmodel.predict(X_test)

#logmodel.score(X_test,y_test.values.ravel())



features_test=Extract_features.main(url)
print(features_test)

pred=logmodel.predict([X.iloc[6]])
#pred=logmodel.predict([features_test])
print(pred)
if pred:
    print ("This is a safe website.")
else:
    print ("This is a phishing website..!")


