from django.db import models
import os


#os.environ['DJANGO_SETTINGS_MODULE'] = 'netshop.settings'   # myweb是改成自己的项目名称
# Create your models here.
#objects = models.Manager()
class Category(models.Model):
    cname=models.CharField(max_length=10)

    def __str__(self):
        return "cname:%s"%self.cname

class Goods(models.Model):
    gname=models.CharField(max_length=100)
    gdesc = models.CharField(max_length=100)
    oldprice = models.DecimalField(max_digits=5,decimal_places=2)
    price = models.DecimalField(max_digits=5,decimal_places=2)
    category=models.ForeignKey(Category,on_delete=True)

    def __str__(self):
        # inventory_set属于类名加_set,一个属性，存当前类下对应所有库存，应该是通过good的作为inventory对象，外键获得
        return 'Goods:%s'%(self.inventory_set.first().color.colorurl)
    # 获取商品大图
    def getGimg(self):
        return self.inventory_set.first().color.colorurl
    # 获取商品所有颜色对象
    def getColorList(self):
        colorList=[]
        for inventory in self.inventory_set.all():
            color=inventory.color
            if color not in colorList:
                colorList.append(color)
        return colorList

    # 获取商品所有尺寸对象
    def getSizeList(self):
        sizeList=[]
        for inventory in self.inventory_set.all():
            size=inventory.size
            if size not in sizeList:
                sizeList.append(size)
        return sizeList

    def getDetailList(self):
        # 创建有序字典，需要导入包collection,直接用{}列表不能有序
        import collections
        datas = collections.OrderedDict()
        for goodsdetail in self.goodsdetail_set.all():
            # 获取详情名称
            gdname=goodsdetail.name()
            if not gdname in datas.keys():
                datas[gdname]=[goodsdetail.gdurl]
            else:
                datas[gdname].append(goodsdetail.gdurl)
        return datas

class GoodsDetailName(models.Model):
    gdname=models.CharField(max_length=30)

    def __str__(self):
        return 'GoodsDetailName:%s'% self.gdname

class GoodsDetail(models.Model):
    gdurl=models.ImageField(upload_to='')# 存放mida图片地址
    gdname=models.ForeignKey(GoodsDetailName,on_delete=False)
    goods=models.ForeignKey(Goods,on_delete=True)

    def name(self):
        return self.gdname.gdname

    def __str__(self):
        return self.gdurl

class Size(models.Model):
    sname=models.CharField(max_length=100)

    def __str__(self):
        return 'Size:%s'%self.sname

class Color(models.Model):
    colorname=models.CharField(max_length=10)
    colorurl=models.ImageField(upload_to='color/')

    def __str__(self):
        return 'Color:%s'%self.colorname

class Inventory(models.Model):
    count=models.PositiveIntegerField()
    color=models.ForeignKey(Color,on_delete=True)
    goods=models.ForeignKey(Goods,on_delete=True)
    size=models.ForeignKey(Size,on_delete=True)



