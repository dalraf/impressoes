# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.http import HttpResponse

from django.shortcuts import render

import re

import os

import csv

# Create your views here.


def default(request):
    path="/home/daniel/csv"  # insert the path to your directory
    cvslist = [re.sub(r'^papercut-print-log-([0-9-]+).csv',r'\1',w) for w in os.listdir(path)]
    return render(request,'listar.html', {'csvs': cvslist})


def gerar(request, detalhe):
    csvfile = '/home/daniel/csv/papercut-print-log-' + detalhe + '.csv'
    csvfileopen = csv.DictReader(open(csvfile).readlines()[1:], delimiter=str(u','),dialect=csv.excel)
    csvdict = []
    for line in csvfileopen:
        csvdict.append(line)
    return render(request,'detalhe.html', {'csvdict': list(csvdict), 'csvfile': csvfile})


