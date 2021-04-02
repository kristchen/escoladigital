from django.conf.urls import url
from django.contrib.auth import views
from usuario import views as viewsUser

urlpatterns = [
   url(r'^login/$', views.login, {'template_name':'login.html'}, name='login'),
   url(r'^accounts/login/$', views.login, {'template_name':'login.html'}, name='accounts-login'),
   url(r'^logout/$', views.logout_then_login, {'login_url':'/login/'}, name='logout'),
   url(r'^home/$', viewsUser.home, name='home'),
]

	
