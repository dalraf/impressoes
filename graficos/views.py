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

def get_dict_csv(tipo,daterange):
    
    csvfile = csv_diretorio + '/papercut-print-log-' + daterange + '.csv'
    csvfileopen = csv.DictReader(open(csvfile).readlines()[1:], delimiter=str(u','),dialect=csv.excel)
    csvdict = []
    for line in csvfileopen:
        csvdict.append(line)
    
    dadosdict = {}
    for line in csvdict:
        if tipo == "usuario":
            if line['User'] in dadosdict:
                dadosdict[line['User']] = dadosdict[line['User']] + ( int(line['Pages']) * int(line['Copies']) ) 
            else:
                dadosdict[line['User']] = ( int(line['Pages']) * int(line['Copies']) )
        elif tipo == "impressora":
            if line['Printer'] in dadosdict:
                dadosdict[line['Printer']] = dadosdict[line['Printer']] + ( int(line['Pages']) * int(line['Copies']) ) 
            else:
                dadosdict[line['Printer']] = ( int(line['Pages']) * int(line['Copies']) ) 
    dadosdict = OrderedDict(sorted(dadosdict.items(), key=itemgetter(1), reverse=True))
    return dadosdict



def default(request):
    path=csv_diretorio
    cvslist = [re.sub(r'^papercut-print-log-([0-9-]+).csv',r'\1',w) for w in os.listdir(path)]
    return render(request,'listar.html', {'csvs': cvslist})


def report(request, detalhe):

    dadosusuario = get_dict_csv('usuario',detalhe)
    dadosimpressora = get_dict_csv('impressora',detalhe)

    arquivofonte = 'papercut-print-log-' + detalhe + '.csv'

    return render(request,'detalhe.html', { 'detalhe': detalhe, 'arquivofonte': arquivofonte, 'dadosusuario': dadosusuario, 'dadosimpressora': dadosimpressora })



def plot(request, detalhe, tipo):
    from django.http import HttpResponse

    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    
    from matplotlib.figure import Figure
    
    import matplotlib.pyplot as plt

    dicionario_plot = get_dict_csv(tipo,detalhe)
    if tipo == 'usuario':
        plot_title = 'Páginas por usuário (12+)'
    elif tipo == 'impressora':
        plot_title = 'Páginas por impressora (12+)'

    fig=Figure()
    ax=fig.add_subplot(111)
    ax.bar(range(1,len(dicionario_plot)+1), dicionario_plot.values(), align='center')
    ax.set_title(plot_title)
    ax.set_ylabel('Páginas')
    ax.set_xticklabels(dicionario_plot.keys())
    ax.set_xticks(range(1,len(dicionario_plot)+1))
    ax.set_xlim(0,12)
    fig.autofmt_xdate()
    canvas=FigureCanvas(fig)
    response=HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response