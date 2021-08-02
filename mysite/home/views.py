import os
import pandas as pd
from pathlib import Path
from django.shortcuts import render
from .config import SITE_ROOT
def index(request):
    data = pd.read_csv(SITE_ROOT+'\\data\\disease-symptoms.csv', encoding='utf-8', index_col=0)
    trans_df = data.T
    data = list(trans_df.iloc[1])
    return render(request,'home.html',{'data':data})
def chandoanpost(request):
    f = open(SITE_ROOT+'\\data\\input.txt', "w")
    post = list(request.POST.items())
    for i in range(1,len(post)):
        f.write(post[i][1]+"\n")
    f.close()
    #Start excute Engine
    FILE_ENGINE = SITE_ROOT[0:-4] + '\\MES.py'
    os.system('python '+FILE_ENGINE)
    #End excute Engine
  

    #Show result
    f = open(SITE_ROOT + '\\data\\output.txt', "r", encoding='utf-8')
    result = f.read()
    f.close()
    return render(request,'chandoan.html',{'result':result})
