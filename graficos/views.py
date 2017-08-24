# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.http import HttpResponse

from django.shortcuts import render

from collections import OrderedDict

from operator import itemgetter

import re

import os

import glob

import csv

from django.shortcuts import redirect

from django.core.files.storage import FileSystemStorage

from .forms import csvform

from .models import csvprint

from django.conf import settings

# Create your views here.


def get_dict_csv(tipo, cooperativa, pa, ano, mes):
    
    csvquery = csvprint.objects.filter(cooperativa=cooperativa,pa=pa,ano=ano,mes=mes)[0]

    csvfile = settings.MEDIA_ROOT + "/" + csvquery.csvfileref.name
    
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
    csvs = csvprint.objects.all()
    return render(request,'listar.html', {'csvs': csvs})


def deletecsv(request, cooperativa, pa, ano, mes):
    csvquery = csvprint.objects.filter(cooperativa=cooperativa,pa=pa,ano=ano,mes=mes)
    csvquery.delete()
    return redirect('default')


def report(request, cooperativa, pa, ano, mes):

    dadosusuario = get_dict_csv('usuario', cooperativa, pa, ano, mes)
    dadosimpressora = get_dict_csv('impressora',cooperativa, pa, ano,  mes)

    return render(request,'detalhe.html', { 'cooperativa': cooperativa, 'pa': pa, 'ano': ano, 'mes': mes, 'dadosusuario': dadosusuario, 'dadosimpressora': dadosimpressora })



def plot(request, cooperativa, pa, ano, mes, tipo):
    from django.http import HttpResponse

    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    
    from matplotlib.figure import Figure
    
    import matplotlib.pyplot as plt

    dicionario_plot = get_dict_csv(tipo, cooperativa, pa, ano, mes )

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

def cvs_upload(request):
    if request.method == 'POST':
        form = csvform(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('default')
    else:
        form = csvform()
    return render(request, 'csv_upload.html', {
        'form': form
    })