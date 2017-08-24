# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

from django.db import models

from django.db import models

class csvprint(models.Model):    
    
    MES = (
    (0, 'Janeiro'),
    (1, 'Fevereiro'),
    (2, 'Março'),
    (3, 'Abril'),
    (4, 'Maio'),
    (5, 'Junho'),
    (6, 'Julho'),
    (7, 'Agosto'),
    (8, 'Setembro'),
    (9, 'Outubro'),
    (10, 'Novembro'),
    (11, 'Dezembro'),
    )
    
    ANO = (
    (2017,'2017'),
    (2018,'2018'),
    (2019,'2019'),
    )

    COOPERATIVA = (
    (4117,'Credinova'),
    )

    PA = (
    (0,'Sede'),
    (1,'Pa01'),
    (2,'Pa02'),
    (3,'Pa03'),
    (3,'Pa04'),
    )

    ano = models.IntegerField('Ano',choices=ANO)
    
    mes = models.IntegerField('Mês',choices=MES)
    
    cooperativa = models.IntegerField('Cooperativa',choices=COOPERATIVA)

    pa = models.IntegerField('PA',choices=PA)

    csvfileref = models.FileField('Arquivo csv',upload_to='csv/')

