from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$',views.AddCartView.as_view()),
    url(r'^querAll/$',views.QuerAllView.as_view()),
    #url(r'^cart.html$',views.QuerAllView.as_view())

]