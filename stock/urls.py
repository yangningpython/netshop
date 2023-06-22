from django.conf.urls import url
from . import views

urlpatterns=[
    # url(r'^$',views.stock_play.as_view()),
    url(r'^stock_play/$',views.stock_play.as_view()),
    url(r'^k_line_similitude/$',views.k_line_similitude.as_view()),
    #url(r'^cart.html$',views.QuerAllView.as_view())

]