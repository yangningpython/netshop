from django.contrib import admin
from .models import Category, Goods, GoodsDetailName, GoodsDetail, Size, Color, Inventory

# 为每个模型创建管理类，显示所有字段
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('cname',)

@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
    list_display = ('gname', 'gdesc', 'price', 'category')
    fieldsets = [(None, {'fields': ('gname', 'gdesc', 'oldprice', 'price', 'category')})]

@admin.register(GoodsDetailName)
class GoodsDetailNameAdmin(admin.ModelAdmin):
    list_display = ('gdname',)
    fieldsets = [(None, {'fields': ('gdname',)})]

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('sname',)
    fieldsets = [(None, {'fields': ('sname',)})]

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('colorname', 'colorurl')
    fieldsets = [(None, {'fields': ('colorname', 'colorurl')})]

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('count', 'color', 'goods', 'size')
    fieldsets = [(None, {'fields': ('count', 'color', 'goods', 'size')})]

@admin.register(GoodsDetail)
class GoodsDetailAdmin(admin.ModelAdmin):
    list_display = ('gdurl', 'gdname', 'goods')
    fieldsets = [(None, {'fields': ('gdurl', 'gdname', 'goods')})]
