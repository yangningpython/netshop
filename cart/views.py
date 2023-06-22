from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.views import View
from cart.cartmanager import *



class AddCartView(View):
    def post(self,request):
        # session本身原因不会实时更新，需要设置调用去更新，从而显示在前台购物车
        request.session.modified=True

        flag=request.POST.get('flag','')
        if flag=='add':
            #创建cartmanger对象
            cartManagerobj=getCartManger(request)
            # 加入购物车
            cartManagerobj.add(**request.POST.dict())
        elif flag=="plus":
            cartManagerobj = getCartManger(request)
            # 修改商品数量，追加
            cartManagerobj.update(step=1,**request.POST.dict())
        elif flag=="minus":
            cartManagerobj = getCartManger(request)
            # 修改商品数量，追加
            cartManagerobj.update(step=-1,**request.POST.dict())
        elif flag=="delete":
            cartManagerobj = getCartManger(request)
            # 逻辑删除商品数量，追加
            cartManagerobj.delete(**request.POST.dict())

        #print(request.POST.dict())
        return HttpResponseRedirect("/cart/querAll/")


class QuerAllView(View):
    def get(self,request):
        # 创建caertmanage对象
        cartManagerobj=getCartManger(request)

        # 查询所有购物信息
        cartList=cartManagerobj.queryAll()

        return render(request,'cart.html',{'cartList':cartList})

