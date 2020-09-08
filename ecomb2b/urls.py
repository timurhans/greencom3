"""ecomb2b URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views
from django.urls import path,re_path
from core.views import (login_view,logout_view,
produtos,carrinho_view,generate_PDF,limpa_cache,
users_log,login_api,dados_api,params_consulta_api,
cats_api)

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('colecao-<str:colecao>/', colecao_view),
    # path('colecao-<str:colecao>/categoria-<str:categoria>/', categoria_view),
    # path('colecao-<str:colecao>/categoria-<str:categoria>/subcategoria-<str:subcategoria>/', product_list_view),
    path('', produtos, name='home'),
    path('login/', login_view,name='login'),
    path('login_api/', login_api,name='login_api'),
    path('dados_api/', dados_api),
    path('cats_api/', cats_api),
    path('params_api/', params_consulta_api),
    path('accounts/logout/', logout_view), 
    path('carrinho/', carrinho_view),
    path('carrinho/pedido/', generate_PDF),
    path('limpa_cache/', limpa_cache),
    path('log/', users_log),
]

# urlpatterns += [
#     re_path(r'(?P<path>.*)', produtos, name='home')
# ]