#coding=utf-8
# 需要将这个文件配置到setting中的template中才能被系统认可
def getUserInfo(request):
    return {'suser':request.session.get('user',None)}