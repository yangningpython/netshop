import math

from django.shortcuts import render

# Create your views here.
from django.views import View

from goods.models import Category, Goods
# 分页用
from django.core.paginator import Paginator


class IndexView(View):

    def get(self,request,cid=2,num=1):
        cid=int(cid)
        num = int(num)
        # 查询所有类信息
        print(cid,1000+num)

        categorys=Category.objects.all().order_by('id')
        for i in categorys:
            print(i.id,i.cname)
        # 查询当前类别下所有商品信息
        goodsList=Goods.objects.filter(category_id=cid).order_by('id')
        #print(goodsList)
        # 分页，每页显示八条记录
        pager=Paginator(goodsList,8)
        # 获取当前也数据
        page_goodsList=pager.page(num)

        # 每页开始页码
        begin = (num-int(math.ceil(10.0/2)))
        if begin<1:
            begin=1
        #每页结束页码
        end= begin+9
        if end > pager.num_pages:
            end=pager.num_pages

        if end<=10:
            begin=1
        else:
            begin=end-9
        pagelist=range(begin,end+1)

        return render(request,'index.html',{'categorys':categorys,'goodsList':page_goodsList,'currentCid':cid, "pagelist":pagelist,"currentNum":num})

def recommend_view(func):
    def wrapper(detailView,request,goodsid,*args,**kwagrs):
        #将存放在cookie中的goodsid获取到
        cookie_str=request.COOKIES.get('recommend','')
        #存放所有goodsid的列表
        goodsIdList=[gid for gid in cookie_str.split() if gid.strip()]

        # 需要获取的推荐商品对象
        goodsobjList=[Goods.objects.get(id=gsid) for gsid in goodsIdList if gsid!=goodsid and Goods.objects.get(id=gsid).category_id==Goods.objects.get(id=goodsid).category_id][:4]
        # 将goodsobjlist传递给get方法
        response=func(detailView,request,goodsid,goodsobjList,*args,**kwagrs)
        # 判断goodsid是否存在goodsidlist中
        if goodsid in goodsIdList:
            goodsIdList.remove(goodsid)
            goodsIdList.insert(0,goodsid)
        else:
            goodsIdList.insert(0,goodsid)
        #print(goodsobjList)
        #将goodsIdList中数据保存到cookie中
        response.set_cookie('recommend',' '.join(goodsIdList),max_age=3*24*60*60)
        return response

    return wrapper
class DetailView(View):
    @recommend_view
    def get(self,request,goodsid,recommendList=[]):
        goodsid=int(goodsid)
        print(request,"detail"+str(goodsid),recommendList)
        # 根据goodsid查询商品镶嵌（goods对象）
        goods=Goods.objects.get(id=goodsid)

        return render(request,'detail.html',{'goods':goods,'recommendList':recommendList})