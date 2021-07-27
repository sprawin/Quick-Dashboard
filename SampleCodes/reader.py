import pandas as pd
import numpy as np
import os
import seaborn as sns
import matplotlib.pyplot as plt
from numpy import mean
dirname = os.getcwd()+'/dataset/'
filename = 'supermarket_sales' #input("Enter File Name: ")
extension = '.csv' # input("Enter extension eg: '.csv' ")
file = dirname+filename+extension
dataset = pd.read_csv(file)

column_list = []
numerical_variables =[]
categorical_variables = []
datetime_variables = []

for column in dataset.columns:
    column_list.append(column)

print("Categorize numerical, categorical and datetime columns from the column list mentioned below")
print("If there is no column in mentioned category type '.' and then press enter key")
print(column_list)

def checkAvailability(column_name,column_list,numerical_variables,categorical_variables,datetime_variables):
    if column_name not in column_list:
        print("please enter correct column name")
        return 0
    elif column_name in categorical_variables:
        print("column already available in categorical variables list")
        return 0
    elif column_name in numerical_variables:
        print("column already available in numerical variables list")
        return 0
    elif column_name in datetime_variables:
        print("column already available in datetime variables list")
        return 0
    else:
        return True

def categorizeVariables(category,column_list,numerical_variables,categorical_variables,datetime_variables):
        while(True):
            column_name = input("Enter "+category+" variables: ")
            if(column_name == "."):
                break
            else:
                if checkAvailability(column_name,column_list,numerical_variables,categorical_variables,datetime_variables):
                    if category == "categorical":
                        categorical_variables.append(column_name)
                    elif category == "numerical":
                        numerical_variables.append(column_name)
                    elif category == "datetime":
                        datetime_variables.append(column_name)
                    else:
                        print("Mentioned category not available")

def clearList(listname):
    if listname == "all":
        numerical_variables =[]
        categorical_variables = []
        datetime_variables = []
    elif listname == "numerical":
        numerical_variables =[]
    elif listname == "categorical":
        categorical_variables = []
    elif listname == "datetime":
        datetime_variables = []

def boxPlot(column_name,numerical_variables,dataset):
    if column_name in numerical_variables:
        f1 = plt.figure()
        plt.clf()
        plt.cla()
        plt.title(column_name)
        sns.boxplot(x = dataset[column_name])
        imagename = str(column_name)+'.png'
        fullpath = os.path.join(os.getcwd(),'plots',imagename)
        plt.savefig(fullpath, dpi=300, bbox_inches='tight')
    else:
        print("Only numerical variables can be plotted in boxplot")

def countPlot(column_name,categorical_variables,dataset):
    if column_name in categorical_variables:
        f2 = plt.figure()
        plt.clf()
        plt.cla()
        plt.title(column_name)
        sns.countplot(x = dataset[column_name])
        plt.xticks(rotation = 45)
        imagename = str(column_name)+'.png'
        fullpath = os.path.join(os.getcwd(),'plots',imagename)
        plt.savefig(fullpath, dpi=300, bbox_inches='tight')
    else:
        print("Only Categorical variables can be plotted in Count Plot")

def groupbyPlot(xaxis,yaxis,aggrfunc,kind):
    f3 = plt.figure()
    plt.clf()
    plt.cla()
    plt.title(yaxis)
    dataset.groupby(xaxis)[yaxis].agg(aggrfunc).unstack().plot(kind = kind)
    imagename = str(yaxis)+'.png'
    fullpath = os.path.join(os.getcwd(),'plots',imagename)
    plt.savefig(fullpath, dpi=300, bbox_inches='tight')

categorizeVariables("categorical",column_list,numerical_variables,categorical_variables,datetime_variables)
categorizeVariables("numerical",column_list,numerical_variables,categorical_variables,datetime_variables)
categorizeVariables("datetime",column_list,numerical_variables,categorical_variables,datetime_variables)

print("\nCheck Once if everything is added correctly\n")
print("numerical_variables: ",numerical_variables)
print("categorical_variables: ",categorical_variables)
print("datetime_variables: ",datetime_variables)
print("\nCount Plot")
while(True):
    cvar = input("Enter Categorical variables only: ")
    if cvar == '.':
        cvar = ''
        break
    else:
        countPlot(cvar,categorical_variables,dataset)
print("Box Plot")
while(True):
    nvar = input("Enter numerical variables only: ")
    if nvar == '.':
        nvar = ''
        break
    else:
        boxPlot(nvar,numerical_variables,dataset)

groupbyPlot(['City','Gender'],'gross income',mean,'bar')
