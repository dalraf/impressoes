# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

from django.db import models

class CVSFiles(models.Model):
    cvs = models.FileField('Arquivo CSV',upload_to='.')
