from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, request
from django.shortcuts import render

# Create your views here.
from django.views import View

from cart.cartmanager import SessionCartManager
from userapp.models import UserInfo, Area, Address
from utils import code
from django.core.serializers import serialize


class RegisterView(View):
    def get(self,request):
        return render(request,'register.html')

    def post(self, request):
        # 获取请求参数
        uname=request.POST.get("uname","")
        pwd = request.POST.get("pwd", "")

        #插入数据库
        user=UserInfo.objects.create(uname=uname,pwd=pwd)
        #判断是否注册成功
        if user:
            # 在所有的页面中都共享session中的数据，用全局上下文
            request.session["user"]=user
            # 重定向到别的网页
            return HttpResponseRedirect('/user/center/')
        return HttpResponseRedirect('/user/register/')


class CheckUnameView(View):
    def get(self,request):
        # 获取请求参数
        uname=request.GET.get('uname','')
        # 根据用户名去数据库查询

        userList=UserInfo.objects.filter(uname=uname)

        flag=False
        if userList:
            flag=True

        return JsonResponse({'flag':flag})


class CenterView(View):
    def get(self,request):
        return render(request,'center.html')


class LogoutView(View):
    def post(self,request):
        # 删除session中登录用户数据
        if 'user' in request.session:
            del request.session['user']
        return JsonResponse({'delflag':True})


class LoginView(View):
    def get(self, request):

        # 获取请求参数
        redirect=request.GET.get('redirct','')

        print(redirect,"---get")

        # if redirect:
        #     return render(request, 'login.html')

        return render(request, 'login.html',{'redirect':redirect})

    def post(self, request):
        uname=request.POST.get('uname','')
        pwd=request.POST.get('pwd', '')

        userList=UserInfo.objects.filter(uname=uname,pwd=pwd)

        #print(uname,pwd,userList)
        if userList:
            request.session['user'] = userList[0]
            redirect = request.POST.get('redirect', '')
            print(redirect,"--hello")
            if redirect=='cart':
                request.session['user'] = userList[0]
                SessionCartManager(request.session).migrateSession2DB()
                return HttpResponseRedirect('/cart/querAll/')
            elif redirect=='order':
                return HttpResponseRedirect('/order/order.html?cartitrms=' + request.POST.get('cartitems',''))


            return HttpResponseRedirect('/user/center/')
        return HttpResponseRedirect('/user/login/')


class LoadCondeView(View):
    def get(self, request):
        img,str=code.gene_code()
        # 存码到session中，为后面做校验
        request.session['sessioncode'] = str
        # 二进制要转换图片类型'image/png'

        return HttpResponse(img,content_type='image/png' )


class CheckcodeView(View):
    def get(self, request):
        code = request.GET.get('code','')
        sessioncode=request.session.get('sessioncode',None)
        flag=code==sessioncode
        # 二进制要转换图片类型'image/png'
        return JsonResponse({'checkFlag':flag})


class AddressView(View):
    def get(self, request):
        user = request.session.get('user', '')
        # 获取当前用户所有地址
        addrList = user.address_set.all()
        return render(request, 'address.html', {'addrList': addrList})
    def post(self, request):
        aname=request.POST.get('aname','')
        aphone = request.POST.get('aphone', '')
        addr = request.POST.get('addr', '')
        user = request.session.get('user', '')

        # 插入数据库
        address=Address.objects.create(aname=aname,aphone=aphone,addr=addr,userinfo=user,\
                               isdefault=(lambda count: True if count==0 else False)(user.address_set.all().count()))

        # 获取当前用户所有地址
        addrList=user.address_set.all()
        return render(request,'address.html',{'addrList':addrList})


class LoadAreaView(View):
    def get(self, request):
        pid = int(request.GET.get('pid', -1))
        #根据父id查询区块信息
        areaList = Area.objects.filter(parentid=pid)

        #进行序列号
        jareaList=serialize('json',areaList)
        return JsonResponse({'jareaList':jareaList})
        # 二进制要转换图片类型'image/png'