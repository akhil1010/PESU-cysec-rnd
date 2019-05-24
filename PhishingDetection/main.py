# -*- coding: utf-8 -*-
"""
Created on Sun May 19 16:33:04 2019

@author: Niveditha Patil
"""

import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.linear_model import LogisticRegression

import Extract_features
#url=sys.argv[1]
#url='https://chained-advancement.000webhostapp.com/next.php'
#url='https://braprodutosservicos.eu/procedimentotrimestral/html/classic/?'
url='https://www.instagram.com'
df = pd.read_csv('Training Dataset.csv', header =0)

#df.isnull().values.any()

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

#X = df.drop(df.columns[[1,4,8,17,19,20,23,26,30]], axis=1)  


#create an instance and fit the model 
logmodel = LogisticRegression(solver='lbfgs')
logmodel.fit(X, y.values.ravel())
# Due to updates to scikit-learn, we now need a 2D array as a parameter to the predict function.
features_test = Extract_features.generate_data_set(url)
print(features_test)
features_test = np.array(features_test).reshape((1, -1))
pred = logmodel.predict(features_test)
print(pred)
if int(pred[0]) == 1:
        # print "The website is safe to browse"
        print("SAFE")
elif int(pred[0]) == -1:
        # print "The website has phishing features. DO NOT VISIT!"
        print("PHISHING")

        # print 'Error -', features_test'''
#print(features_test)
    

