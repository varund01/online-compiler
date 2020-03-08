from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import Http404
from datetime import datetime,timedelta
from django.contrib.auth import logout
from django.core.files.base import ContentFile
from django.conf import settings as settingsFile
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
import random,os,shutil,subprocess,functools,hashlib
from django.contrib.auth import authenticate, login as login_user
from django.core.exceptions import PermissionDenied
from base64 import b64encode,b64decode
from collections import defaultdict
from django.core.files.storage import FileSystemStorage
# Create your views here.

def upload(request):
    context={}
    if(request.method=='POST'):
        if(request.POST['document']!=''):
            uploaded_file=request.FILES['document']
            fs=FileSystemStorage()
            name=fs.save(uploaded_file.name,uploaded_file)
            #take input

        else:
            fs=FileSystemStorage()
            content2=request.POST['code']
            contfile=ContentFile(content2)
            randomword=""
            for i in range(30):
                randomword+=random.choice('123456789abcdefghijklmnopqrstuvwxyz')
            randomword+=".cpp"
            name=fs.save(randomword,contfile)
        justname = name[:-4]
        context['url'] = fs.url(name)
        content1 = request.POST['input']
        inputtxtname = 'input' + justname + '.txt';
        contfile = ContentFile(content1)
        fs.save(inputtxtname, contfile)
        # now u should compile the file
        BASE_PATH = settingsFile.MEDIA_ROOT
        folder = BASE_PATH
        print(folder)
        p = subprocess.Popen(["g++", name, "-O2", "-o", "code", "-std=c++11"], cwd=BASE_PATH)

        print(p)
        if p:
            print('1ds')
        p = subprocess.call(folder + "/code < " + folder + "/" + inputtxtname + " > " + folder + "/output.txt",
                            shell=True)
        if p:
            print('1')
        with open(BASE_PATH + "/output.txt", mode="r") as f:
            lines = f.readlines()
            f.close()
        context['out'] = lines
    return render(request,'upload.html',context)

