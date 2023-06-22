from django.apps import AppConfig
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'netshop.settings'   # myweb是改成自己的项目名称

class GoodsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'goods'
