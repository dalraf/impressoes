# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.http import HttpResponse

from django.shortcuts import render

import os

# Create your views here.


def default(request):
    path="/home/daniel/csv"  # insert the path to your directory   
    cvslist =os.listdir(path)   
    return render(request,'listar.html', {'csvs': cvslist})