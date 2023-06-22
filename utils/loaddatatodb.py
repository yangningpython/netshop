#coding=utf-8
import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "netshop.settings")# project_name 项目名称
django.setup()
from utils.loaddata import *
#
test_model()