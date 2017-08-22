# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.http import HttpResponse

from django.shortcuts import render

from collections import OrderedDict

from operator import itemgetter

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
    
    dadosusuario = {}
    dadosimpressora = {}
    for line in csvdict:
        if line['User'] in dadosusuario:
            dadosusuario[line['User']] = dadosusuario[line['User']] + int(line['Pages'])
        else:
            dadosusuario[line['User']] = int(line['Pages'])
        if line['Printer'] in dadosimpressora:
                dadosimpressora[line['Printer']] = dadosimpressora[line['Printer']] + int(line['Pages'])
        else:
            dadosimpressora[line['Printer']] = int(line['Pages'])
    dadosusuariorder = OrderedDict(sorted(dadosusuario.items(), key=itemgetter(1), reverse=True))
    dadosimpressoraorder = OrderedDict(sorted(dadosimpressora.items(), key=itemgetter(1), reverse=True))

    return render(request,'detalhe.html', { 'csvfile': csvfile, 'dadosusuario': dadosusuariorder, 'dadosimpressora': dadosimpressoraorder })


