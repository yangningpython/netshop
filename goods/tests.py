from django.test import TestCase

# Create your tests here.
import pyodbc as pyodbc

# Create your tests here.
import django_pyodbc
import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "netshop.settings")# project_name 项目名称
django.setup()

# from utils.loaddata import *
#
# test_model()
#deleteall()
import os
# from pathlib import Path
# BASE_DIR = Path(__file__).resolve().parent.parent
#
# print(Path(BASE_DIR,'media'))

# from goods.models import Category, Goods
# a=Category()
# print(a)

# d = {'name':"Tom", 'age':10, 'Tel':110}
# print( d.has_key('name'))
# filter用法通过对象中外键对象获取第一个gdname系GoodsDetail，第二个gdname系对应外键GoodsDetailName表中数据
filter(gdname__gdname=u'参数规格')
from goods.models import *
GoodsDetail.objects.filter(gdname__gdname=u'参数规格').update(gdurl='/static/B5_03.png')

from goods.models import *
GoodsDetail.objects.filter(gdname__gdname=u'整体款式').update(gdurl='/static/B5_06.png')



