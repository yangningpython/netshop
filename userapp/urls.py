from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^register/$',views.RegisterView.as_view()),
    url(r'^checkUname/$',views.CheckUnameView.as_view()),
    url(r'^center/$',views.CenterView.as_view()),
    url(r'^logout/$',views.LogoutView.as_view()),
    url(r'^login/$',views.LoginView.as_view()),
    url(r'^loadConde.jpg$',views.LoadCondeView.as_view()),
    url(r'^checkcode/$',views.CheckcodeView.as_view()),
    url(r'^address/$',views.AddressView.as_view()),
    url(r'^loadArea/$',views.LoadAreaView.as_view()),

]