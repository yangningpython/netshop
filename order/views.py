
import jsonpickle as jsonpickle
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from cart.cartmanager import *
from goods.models import Inventory
from order.models import Order, OrderItem
from userapp.models import Address
from utils.alipay import *


class ToOrderCartView(View):
    def get(self,request):
        # 获取请求参数
        cartitems=request.GET.get('cartitems','')
        # 判断用户是否登录
        #print(cartitems)
        if not request.session.get('user'):
            return render(request,'login.html',{'cartitems':cartitems,'redirect':'order'})
        return HttpResponseRedirect('/order/order.html?cartitems='+cartitems)


class OrderView(View):
    def get(self,request):
        # 获取请求参数
        cartitems = request.GET.get('cartitems', '')
        #蒋json格式字符串转换为python对象列表字典{goodsid:1,colorid:1,sizeid:1},jsonpickle.loads反序列化
        cartitemList=jsonpickle.loads("["+cartitems+"]")
        #将python列表对象转换成cartitems对象列表
        print("没有")
        cartitemobjList=[getCartManger(request).get_cartitems(**item) for item in cartitemList if item]
        
        #获取用户默认地址
        try :

            address=request.session.get('user').address_set.get(isdefault=True)
        except Exception:
            return HttpResponseRedirect("/user/address")
        #获取支付总金额
        totalPrice=0
        for cm in cartitemobjList:
            totalPrice+=cm.getTotalPrice()
        #print(address)
        #if not address :
        #print(cartitems,'---order')
        return render(request,'order.html',{'cartitemobjList':cartitemobjList,'address':address,'totalPrice':totalPrice})
        #return HttpResponseRedirect("/user/address")

alipay=AliPay(appid='2021000118687311', app_notify_url='http://118.31.114.138:8000/order/checkPay/', app_private_key_path='order/key/my_private_key.txt',
                 alipay_public_key_path='order/key/alipay_public_key.txt', return_url='http://118.31.114.138:8000/order/checkPay/', debug=True)
class ToPayView(View):
    def get(self, request):
        #pass
        # 1插入order表中数据
        # 获取请求参数
        import uuid,datetime
        #request.GET.get()
        data={
            'out_trade_num':uuid.uuid4().hex,
            'order_num':datetime.datetime.today().strftime('%Y%m%d%H%M%S'),
            'payway':request.GET.get('payway'),
            'address':Address.objects.get(id=request.GET.get('address','')),
            'user':request.session.get('user','')
        }
        orderObj=Order.objects.create(**data)
        # 2插入orderitem表中数据
        # goodsid = models.PositiveIntegerField()
        # colorid = models.PositiveIntegerField()
        # sizeid = models.PositiveIntegerField()
        # count = models.PositiveIntegerField()
        # order = models.ForeignKey(Order, on_delete=False)
        cartitems=jsonpickle.loads(request.GET.get('cartitems'))
        # print(request.GET.get('cartitems'))
        # print(cartitems,orderObj)
        orderItemList=[OrderItem.objects.create(**item,order=orderObj) for item in cartitems if item]
        totalprice=request.GET.get('totalprice')[1:]
        #3获取扫码支付页面
        params=alipay.direct_pay(subject='hello超市', out_trade_no=orderObj.out_trade_num, total_amount=str(totalprice))
        #拼接请求地址
        url=alipay.gateway+'?'+params
        return HttpResponseRedirect(url)


class CheckPayView(View):
    def get(self,request):
        # 校验是否支付成功
        params=request.GET.dict()
        #获取签名
        sign=params.pop('sign')
        print(sign,'---checkpay456666')
        if alipay.verify(params,sign):
            # 修改订单表中支付状态
            out_trade_no=params.get('out_trade_no','')
            order = Order.objects.get(out_trade_num=out_trade_no)
            order.status = u'待发货'
            order.save()
            #params.get('out_trade_no')
            # 修改库存
            orderitemList = order.orderitem_set.all()
            # 原先默认值用F查询
            [Inventory.objects.filter(goods_id=item.goodsid, size_id=item.sizeid, color_id=item.colorid).update(
                count=F('count') - item.count) for item in orderitemList if item]

            # 修改购物表
            [CartItem.objects.filter(goodsid=item.goodsid, sizeid=item.sizeid, colorid=item.colorid).delete() for item
             in orderitemList if item]

            return HttpResponse('支付成功！')

        return HttpResponse('支付失败！')
