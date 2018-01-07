import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

import warnings
warnings.filterwarnings('ignore')

train = pd.read_csv('./train.csv')
test  = pd.read_csv('./test.csv')

# print train.sample(5)
print train.describe( include='all' )

def checkNull() :
	print pd.isnull(train).sum()
	print pd.isnull(test).sum()

checkNull()
test = test.dropna()
checkNull()

thief_mapping = {'Home':1, 'Bike':2, 'Car':3}
dist_mapping = {'Beitou':1, 'Daan':2, 'Datong':3, 'Nangang':4, 'Neihu':5, 'Shilin':6, 'Songshan':7, 'Wanhua':8, 'Wenshan':9, 'Xinyi':10, 'Zhongshan':11, 'Zhongzheng':12 }
train['Category'] = train['Category'].map( thief_mapping )
train['District'] = train['District'].map( dist_mapping )
test['District'] = test['District'].map( dist_mapping )
train = train.drop('Day', 1)
test = test.drop('Day', 1)
print train.sample(5)


def setDate () :
	from datetime import datetime
	baseDate = datetime.strptime( '1911/10/10', '%Y/%m/%d' )
	for i in range( len(train['Date']) ) :
		nowDate = datetime.strptime( train['Date'][i], '%Y/%m/%d' )
		print (nowDate - baseDate).days, train['Date'][i]
		train['Date'][i] = (nowDate - baseDate).days	

setDate()
# print train['Date'], type( np.array(train['Date']))
# print train.sample(5)



def rlt () :
	from sklearn.model_selection import train_test_split
	from sklearn.metrics import accuracy_score

	predictors = train.drop(['Category', 'Id'], axis=1)
	target = train["Category"]
	x_train, x_val, y_train, y_val = train_test_split(predictors, target, test_size = 0.22, random_state = 0)
	
	from sklearn.tree import DecisionTreeClassifier

	decisiontree = DecisionTreeClassifier()
	decisiontree.fit(x_train, y_train)
	y_pred = decisiontree.predict(x_val)
	acc_decisiontree = round(accuracy_score(y_pred, y_val) * 100, 2)
	print 'Decision Tree', acc_decisiontree

	from sklearn.ensemble import RandomForestClassifier

	randomforest = RandomForestClassifier()
	randomforest.fit(x_train, y_train)
	y_pred = randomforest.predict(x_val)
	acc_randomforest = round(accuracy_score(y_pred, y_val) * 100, 2)
	print 'Random Forest', acc_randomforest

	from sklearn.neighbors import KNeighborsClassifier

	knn = KNeighborsClassifier()
	knn.fit(x_train, y_train)
	y_pred = knn.predict(x_val)
	acc_knn = round(accuracy_score(y_pred, y_val) * 100, 2)
	print 'KNN', acc_knn

	from sklearn.svm import SVC

	svc = SVC()
	svc.fit(x_train, y_train)
	y_pred = svc.predict(x_val)
	acc_svc = round(accuracy_score(y_pred, y_val) * 100, 2)
	print 'SVM', acc_svc

	from sklearn.linear_model import LogisticRegression

	logreg = LogisticRegression()
	logreg.fit(x_train, y_train)
	y_pred = logreg.predict(x_val)
	acc_logreg = round(accuracy_score(y_pred, y_val) * 100, 2)
	print 'LogisticRegression', acc_logreg

	from sklearn.naive_bayes import GaussianNB

	gaussian = GaussianNB()
	gaussian.fit(x_train, y_train)
	y_pred = gaussian.predict(x_val)
	acc_gaussian = round(accuracy_score(y_pred, y_val) * 100, 2)
	print 'GaussianNB', acc_gaussian

rlt()

