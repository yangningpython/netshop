from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$',views.ToOrderCartView.as_view()),
    url(r'^order.html$',views.OrderView.as_view()),
    url(r'^topay/$',views.ToPayView.as_view()),
    url(r'^checkPay/$',views.CheckPayView.as_view()),

    #url(r'^cart.html$',views.QuerAllView.as_view())

]