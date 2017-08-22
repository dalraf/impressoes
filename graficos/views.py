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

csv_diretorio="/home/daniel/csv"


def default(request):
    path=csv_diretorio
    cvslist = [re.sub(r'^papercut-print-log-([0-9-]+).csv',r'\1',w) for w in os.listdir(path)]
    return render(request,'listar.html', {'csvs': cvslist})


def gerar(request, detalhe):
    csvfile = csv_diretorio + '/papercut-print-log-' + detalhe + '.csv'
    csvfileopen = csv.DictReader(open(csvfile).readlines()[1:], delimiter=str(u','),dialect=csv.excel)
    csvdict = []
    for line in csvfileopen:
        csvdict.append(line)
    
    dadosusuario = {}
    dadosimpressora = {}
    for line in csvdict:
        if line['User'] in dadosusuario:
            dadosusuario[line['User']] = dadosusuario[line['User']] + ( int(line['Pages']) * int(line['Copies']) ) 
        else:
            dadosusuario[line['User']] = ( int(line['Pages']) * int(line['Copies']) ) 
        if line['Printer'] in dadosimpressora:
                dadosimpressora[line['Printer']] = dadosimpressora[line['Printer']] + ( int(line['Pages']) * int(line['Copies']) ) 
        else:
            dadosimpressora[line['Printer']] = ( int(line['Pages']) * int(line['Copies']) ) 
    dadosusuariorder = OrderedDict(sorted(dadosusuario.items(), key=itemgetter(1), reverse=True))
    dadosimpressoraorder = OrderedDict(sorted(dadosimpressora.items(), key=itemgetter(1), reverse=True))

    arquivofonte = csvfile.split('/')[-1]

    return render(request,'detalhe.html', { 'arquivofonte': arquivofonte, 'dadosusuario': dadosusuariorder, 'dadosimpressora': dadosimpressoraorder })



def plot(request, detalhe):
    from django.http import HttpResponse

    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    
    from matplotlib.figure import Figure
    
    import matplotlib.pyplot as plt

    D = {'Label1':26, 'Label2': 17, 'Label3':30}

    fig=Figure()
    ax=fig.add_subplot(111)
    ax.bar(range(1,len(D)+1), D.values(), align='center')
    ax.set_title('Impressões por usuário')
    ax.set_ylabel('Numero de páginas')
    ax.set_xticklabels(D.keys())
    ax.set_xticks(range(1,len(D)+1))
    ax.set_xlim(0,4)
    fig.autofmt_xdate()
    canvas=FigureCanvas(fig)
    response=HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response