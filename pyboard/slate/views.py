from django.shortcuts import render,redirect
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.conf import settings
import pandas as pd
import numpy as np
import os
import seaborn as sns
import matplotlib.pyplot as plt
from numpy import mean, median
col_list_dict = []
column_list = []
numerical_variables =[]
categorical_variables = []
datetime_variables = []
dataset = pd.DataFrame()
file = ''
categorical_list_dict = []
numerical_list_dict = []
datetime_list_dict = []
charttype_list_dict = [{'name':'Bar_Chart'},{'name':'Count_Plot'},{'name':'Box_Plot'},{'name':'Pie_Chart'}]
aggrfuns = [{'name':'sum'},{'name':'mean'},{'name':'min'},{'name':'max'}]
image_num = 0
image_name = []

def deleteimagefiles():
    directory = os.path.join(os.getcwd(),'static/images')
    for file in os.listdir(directory):
        os.remove(os.path.join(directory,file))

def clearVariables():
    global column_list, numerical_variables, categorical_variables, datetime_variables
    global col_list_dict, categorical_list_dict, numerical_list_dict, datetime_list_dict, aggrfuns
    global dataset, file, image_num

    col_list_dict = []
    column_list = []
    numerical_variables =[]
    categorical_variables = []
    datetime_variables = []
    dataset = pd.DataFrame()
    file = ''
    categorical_list_dict = []
    numerical_list_dict = []
    datetime_list_dict = []
    charttype_list_dict = [{'name':'Bar_Chart'},{'name':'Count_Plot'},{'name':'Box_Plot'},{'name':'Line_Chart'}]

def checkAvailability(column_name):
    global column_list, numerical_variables, categorical_variables, datetime_variables
    global col_list_dict, categorical_list_dict, numerical_list_dict, datetime_list_dict, aggrfuns
    global dataset, file, image_num, image_name

    print("Checking availability for column: ",column_name)
    if column_name not in column_list:
        print("please enter correct column name")
        return False
    elif column_name in categorical_variables:
        print("column already available in categorical variables list")
        return True
    elif column_name in numerical_variables:
        print("column already available in numerical variables list")
        return True
    elif column_name in datetime_variables:
        print("column already available in datetime variables list")
        return True
    else:
        return True

def categorizeVariables(category,column_name):
    global column_list, numerical_variables, categorical_variables, datetime_variables
    global col_list_dict, categorical_list_dict, numerical_list_dict, datetime_list_dict, aggrfuns
    global dataset, file, image_num, image_name

    if checkAvailability(column_name):
        if category == "categorical":
            categorical_variables.append(column_name)
            categorical_list_dict.append({'name':column_name})
        elif category == "numerical":
            numerical_variables.append(column_name)
            numerical_list_dict.append({'name':column_name})
        elif category == "datetime":
            datetime_variables.append(column_name)
            datetime_list_dict.append({'name':column_name})
        else:
            print("Mentioned category not available")


def clearList(listname):
    global column_list, numerical_variables, categorical_variables, datetime_variables
    global col_list_dict, categorical_list_dict, numerical_list_dict, datetime_list_dict, aggrfuns
    global dataset, file, image_num, image_name

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
    else:
        print("listname not available")

def boxPlot(column_name):
    global column_list, numerical_variables, categorical_variables, datetime_variables
    global col_list_dict, categorical_list_dict, numerical_list_dict, datetime_list_dict, aggrfuns
    global dataset, file, image_num, image_name

    f1 = plt.figure()
    plt.clf()
    plt.cla()
    plt.title(column_name)
    sns.boxplot(x = dataset[column_name])
    image_num = image_num + 1
    imagename = str(image_num)+'.png'
    plotname = os.getcwd()+'\static\images\\'+imagename
    plt.savefig(plotname, dpi=300, bbox_inches='tight')
    image_name.append({"name":imagename})

def countPlot(column_name):
    global column_list, numerical_variables, categorical_variables, datetime_variables
    global col_list_dict, categorical_list_dict, numerical_list_dict, datetime_list_dict, aggrfuns
    global dataset, file, image_num, image_name

    f2 = plt.figure()
    plt.clf()
    plt.cla()
    plt.title(column_name)
    sns.countplot(x = dataset[column_name])
    plt.xticks(rotation = 45)
    image_num = image_num + 1
    imagename = str(image_num)+'.png'
    plotname = os.getcwd()+'\static\images\\'+imagename
    plt.savefig(plotname, dpi=300, bbox_inches='tight')
    image_name.append({"name":imagename})

def groupPlot(xaxis,yaxis,aggrfunc,kind):
    global column_list, numerical_variables, categorical_variables, datetime_variables
    global col_list_dict, categorical_list_dict, numerical_list_dict, datetime_list_dict, aggrfuns
    global dataset, file, image_num, image_name

    f3 = plt.figure()
    plt.clf()
    plt.cla()
    if kind == "bar":
        dataset.groupby(xaxis)[yaxis].agg(aggrfunc).unstack().plot(kind = kind)
    elif kind == "pie":
        dataset.groupby(xaxis)[yaxis].agg(aggrfunc).plot(kind = kind)
    else:
        print("No plot defined.")

    image_num = image_num + 1
    imagename = str(image_num)+'.png'
    plotname = os.getcwd()+'\static\images\\'+imagename
    plt.savefig(plotname, dpi=300, bbox_inches='tight')
    image_name.append({"name":imagename})

def piePlot(xaxis,yaxis,aggrfunc):
    global column_list, numerical_variables, categorical_variables, datetime_variables
    global col_list_dict, categorical_list_dict, numerical_list_dict, datetime_list_dict, aggrfuns
    global dataset, file, image_num, image_name

    f4 = plt.figure()
    plt.clf()
    plt.cla()
    dataset.groupby(xaxis)[yaxis].agg(aggrfunc).plot(kind = 'pie')
    imagename = str(image_num)+'.png'
    plotname = os.getcwd()+'\static\images\\'+imagename
    plt.savefig(plotname, dpi=300, bbox_inches='tight')
    image_name.append({"name":imagename})

def preprocess(filepath):
    global column_list, numerical_variables, categorical_variables, datetime_variables
    global col_list_dict, categorical_list_dict, numerical_list_dict, datetime_list_dict, aggrfuns
    global dataset, file, image_num, image_name

    dataset = pd.read_csv(filepath)
    for column in dataset.columns:
        col_dict = {"name":column}
        col_list_dict.append(col_dict)
        column_list.append(column)

def requestDashboard(req):
    global column_list, numerical_variables, categorical_variables, datetime_variables
    global col_list_dict, categorical_list_dict, numerical_list_dict, datetime_list_dict, aggrfuns
    global dataset, file, image_num, image_name

    if req.method == 'GET':
        print('HomePage')
        clearVariables()
        deleteimagefiles()
        template = 'requestDashboard.html'
        content = {"disable_fileUploadForm":False, "disable_upadatelistForm":True}
        return render(req, template, content)

def processfile(req):
    global column_list, numerical_variables, categorical_variables, datetime_variables
    global col_list_dict, categorical_list_dict, numerical_list_dict, datetime_list_dict, aggrfuns
    global dataset, file, image_num, image_name

    if req.method == 'POST':
        clearVariables()
        file = req.FILES['myfile']
        filename = file.name
        fs = FileSystemStorage()
        fs.save(filename,file)
        filepath = os.getcwd()+'\media'+'\\'+filename
        preprocess(filepath)

        template = 'requestDashboard.html'
        content = {
                    "disable_fileUploadForm":True,
                    "disable_upadatelistForm":False,
                    "col_list_dict":col_list_dict,
                    "msg":"Pick Only Categorical Columns",
                    "variable_type":"categorical"
                    }

        return render(req,template,content)

def updatelist(req):
    global column_list, numerical_variables, categorical_variables, datetime_variables
    global col_list_dict, categorical_list_dict, numerical_list_dict, datetime_list_dict, aggrfuns
    global dataset, file, image_num, image_name

    if req.method == 'POST':
        if req.POST['variable_type'] == "categorical":
            for key,value in req.POST.items():
                if key in column_list:
                    categorizeVariables("categorical",key)
            template = 'requestDashboard.html'
            content = {
                        "disable_fileUploadForm":True,
                        "disable_upadatelistForm":False,
                        "col_list_dict":col_list_dict,
                        "msg":"Pick Only numerical Columns",
                        "variable_type":"numerical"
                        }
            return render(req,template,content)
        elif req.POST['variable_type'] == "numerical":
            for key,value in req.POST.items():
                if key in column_list:
                    categorizeVariables("numerical",key)
            template = 'requestDashboard.html'
            content = {
                        "disable_fileUploadForm":True,
                        "disable_upadatelistForm":False,
                        "col_list_dict":col_list_dict,
                        "msg":"Pick Only datetime Columns",
                        "variable_type":"datetime"
                        }
            return render(req,template,content)
        else:
            for key,value in req.POST.items():
                if key in column_list:
                    categorizeVariables("datetime",key)
            template = 'requestchart.html'
            content = {
                        "numerical_variables":numerical_list_dict,
                        "categorical_variables":categorical_list_dict,
                        "datetime_variables":datetime_list_dict,
                        "charttypes":charttype_list_dict,
                        "aggrfuns": aggrfuns
                        }
            return render(req,template,content)

def plotchart(req):
    global column_list, numerical_variables, categorical_variables, datetime_variables
    global col_list_dict, categorical_list_dict, numerical_list_dict, datetime_list_dict, aggrfuns
    global dataset, file, image_num, image_name
    xaxis = []
    yaxis = ''
    if req.method == 'POST':
        requested_plot = req.POST['plots']

        if requested_plot == "Box_Plot":
            for key,value in req.POST.items():
                if key in numerical_variables:
                    boxPlot(value)
                else:
                    print("please select only numerical variables for box plot")

        elif requested_plot in ["Bar_Chart","Pie_Chart"]:
            for key,value in req.POST.items():
                if key == "numerical_variables_picklist":
                    yaxis = value
                elif key in categorical_variables:
                    xaxis.append(value)
                elif key == "aggregateFunc":
                    aggregate_func = value
                else:
                    print("Either no numerical variable is picked or the value chosen is wrong")
            if yaxis != '':
                if requested_plot == "Bar_Chart":
                    groupPlot(xaxis,yaxis,aggregate_func,"bar")
                else:
                    groupPlot(xaxis,yaxis,aggregate_func,"pie")
            else:
                print("no value for yaxis")


        elif requested_plot == "Count_Plot":
            for key,value in req.POST.items():
                if key in categorical_variables:
                    countPlot(value)
                else:
                    print("please select only categorical variables for Count Plot")


        template = 'requestchart.html'
        content = {
                    "numerical_variables":numerical_list_dict,
                    "categorical_variables":categorical_list_dict,
                    "datetime_variables":datetime_list_dict,
                    "charttypes":charttype_list_dict,
                    "aggrfuns": aggrfuns
                    }
        return render(req,template,content)

def dashboard(req):
    global column_list, numerical_variables, categorical_variables, datetime_variables
    global col_list_dict, categorical_list_dict, numerical_list_dict, datetime_list_dict, aggrfuns
    global dataset, file, image_num, image_name

    if req.method == 'GET':
        template = 'dashboard.html'
        content = {"image_name":image_name}
        for img in image_name:
            print("image name: ",img)
        image_num = 0
        return render(req,template,content)
