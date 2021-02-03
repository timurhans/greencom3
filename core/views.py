#DJANGO IMPORTS
from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse,JsonResponse
from django.core.cache import cache
from django.template.loader import get_template
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.db.models import Q

#APP IMPORTS
from .ondas import (Produto,Estoque,get_produto,get_produtos)
from .models import Eventos
from .forms import LoginForm
from params.models import (ColecaoB2b,ColecaoErp,Banner,Periodo)
# THIRD PARTY IMPORTS
from xhtml2pdf import pisa
import pickle
import base64
import pandas as pd
import json
# import time
from datetime import date
import re
import os, zipfile
import glob
import shutil
from djqscsv import render_to_csv_response
import csv
import ntpath


# FUNCOES AUXILIARES

class Produto():
    pass

class ItemPedido():
    pass

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def registra_log(user,ip,tipo):
    Eventos.objects.create(user = user,ip = ip, tipo = tipo)

def adciona_carrinho(request,periodo):

    tabela=request.user.first_name
    session = request.COOKIES.get('sessionid')
    pedido = Produto()


    produto = request.POST.get('produto')
    pedido.produto = get_produto(produto,tabela,periodo)
    pedido.periodo = periodo
    itens = []
    er_cor = r'@(.+)@'
    qtd_tot = 0
    for key, value in request.POST.items():
        #checa se info confere com padrao cor
        cor = re.match(er_cor,key)
        if cor is not None:
            qtds = request.POST.getlist(key)
            qtds = [int(q) for q  in qtds ]
            qtd_tot = qtd_tot + sum(qtds)
            print(qtds)
            #checa se itens nao estao zerados
            if all(i == 0 for i in qtds):
                continue
            cor = cor.group(1)
            item = ItemPedido()
            item.cor = cor
            item.qtds = qtds
            item.qtd_item = sum(qtds)
            item.valor_item = round(item.qtd_item*pedido.produto['preco'],2)
            itens.append(item)
    pedido.qtd_tot = qtd_tot
    pedido.valor_tot = round(qtd_tot*pedido.produto['preco'],2)
    if len(itens)>0:
        pedido.itens = itens #qtd pedido

        if cache.get(session) is None:
            pedidos = []
            pedidos.append(pedido)   
            cache.set(session, pedidos, 60*60)
        else:
            pedidos = cache.get(session)
            if any(x.produto['produto'] == pedido.produto['produto'] for x in pedidos):
                pedidos = [pedido if x.produto['produto'] == pedido.produto['produto'] else x for x in pedidos]
            else:
                pedidos.append(pedido)
            cache.set(session, pedidos, 60*60)



# VIEWS DA APLICACAO

def produtos(request,path=None):

    colecoes = list(ColecaoB2b.objects.filter(active=True).order_by('ordem').values_list('title', flat=True).distinct())
    banners = Banner.objects.all().order_by('ordem')

    page_size = 16

    print(request.COOKIES)
    session = request.COOKIES.get('sessionid')
    lista_carrinho = cache.get(session)
    try:
        qtd_carrinho = len(lista_carrinho)
    except:
        qtd_carrinho = 0

    if request.user.is_authenticated:

        try:
            periodo = request.GET['periodo']
        except:
            periodo = 'Imediato'

        if request.method == 'POST':
            adciona_carrinho(request,periodo)
            return HttpResponse('<script>history.back();</script>')

        try:
            col = request.GET['colecao']
        except:
            col = ''
        try:
            cat = request.GET['categoria']
            print(cat)
        except:
            cat = ''
        try:
            subcat = request.GET['subcategoria']
        except:
            subcat = ''

        if cat != '':
            queryset = get_produtos(tabela=request.user.first_name,
            colecao=col,categoria=cat,subcategoria=subcat,periodo=periodo)
        else:
            queryset = []
                
        paginator = Paginator(queryset, page_size)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        qtd_pags = paginator.num_pages
        qtd_prods = len(queryset)
        #filtra periodos que ja passaram
        periodos = list(Periodo.objects.filter(Q(periodo_faturamento__gt=date.today()) | Q(desc_periodo='Imediato')).order_by(
                'periodo_faturamento').values_list('desc_periodo', flat=True).distinct())
        if qtd_prods>page_size:
            is_paginated = True
        else:
            is_paginated = False

        cats = cache.get('cats')
        context = {
        'object_list' : queryset,
        'categorias' : cats,
        'colecoes' : colecoes,
        'page_obj': page_obj,
        'is_paginated' : is_paginated,
        'selected_col' : col,
        'selected_cat' : cat,
        'selected_subcat' : subcat,
        'selected_periodo' : periodo,
        'qtd_carrinho' : qtd_carrinho,
        'qtd_pags' : qtd_pags,
        'qtd_prods' : qtd_prods,
        'banners' : banners,
        'periodos' : periodos
        }
        return render(request,"core/produtos.html",context)
    else:
        print(request)
        return redirect('/login')


def carrinho_view(request):

    colecoes = list(ColecaoB2b.objects.filter(active=True).order_by('ordem').values_list('title', flat=True).distinct())

    session = request.COOKIES.get('sessionid')
    lista_carrinho = cache.get(session)
    try:
        qtd_carrinho = len(lista_carrinho)
    except:
        qtd_carrinho = 0

    if request.user.is_authenticated:

        if request.method == 'POST':

            if request.POST.get('altera') is not None:
                try:
                    periodo = request.POST.get('periodo')
                except:
                    periodo = 'Imediato'                
                adciona_carrinho(request,periodo)
                return HttpResponse('<script>history.back();</script>')
            elif request.POST.get('remove') is not None:
                #exclusao carrinho
                produto = request.POST.get('produto')
                print(produto)
                pedidos = cache.get(session)
                pedidos = list(filter(lambda x: x.produto['produto'] != produto, pedidos))
                cache.set(session, pedidos, 60*60)
            elif request.POST.get('processa') is not None:
                #processa pedido
                ip = get_client_ip(request)
                registra_log(request.user.username,ip,'processa_pedido')
                observacoes = request.POST.get('obs_pedido')
                return generate_PDF(request,observacoes)
        try:
            queryset = cache.get(session)
            valor_tot = round(sum([x.valor_tot for x in queryset]),2)
            qtd_tot = sum([x.qtd_tot for x in queryset])
        except:
            queryset = []
            valor_tot = 0
            qtd_tot = 0

        cats = cache.get('cats')
        context = {
        'object_list' : queryset,
        'categorias' : cats,
        'colecoes' : colecoes,
        'valor_tot' : valor_tot,
        'qtd_tot' : qtd_tot,
        'qtd_carrinho' : qtd_carrinho
        }
        return render(request,"core/carrinho.html",context)
    else:
        print(request)
        return redirect('/login')



def generate_PDF(request,observacoes):

    session = request.COOKIES.get('sessionid')
    queryset = cache.get(session)

    valor_total_pedido = round(sum([x.valor_tot for x in queryset]),2)
    qtd_total_pedido = sum([x.qtd_tot for x in queryset])
    today = date.today().strftime("%d/%m/%Y")
    data = {'object_list' : queryset,
            'data' : today,
            'valor_total' : valor_total_pedido,
            'qtd_total' : qtd_total_pedido,
            'observacoes' : observacoes
            }

    template = get_template('core/pedido.html')
    html  = template.render(data)

    file_path = 'static/pdfs/'+session
    file = open(file_path, "w+b")
    pisaStatus = pisa.CreatePDF(html.encode('utf-8'), dest=file,
            encoding='utf-8')

    file.seek(0)
    pdf = file.read()
    file.close()      
    return HttpResponse(pdf, 'application/pdf')



def login_view(request):
    
    print(request.COOKIES)

    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['user']
            password = form.cleaned_data['password']
            try:
                user = authenticate(username=username, password=password)
                login(request, user)
                ip = get_client_ip(request)
                registra_log(user.username,ip,'login')
                return redirect('home')
            except:
                form = LoginForm()
                context = {
                    'form' : form,
                    'erro_login' : 'erro'
                }
                return render(request,"core/login.html",context)

    else:
        form = LoginForm()
        context = {
            'form' : form
        }

        return render(request,"core/login.html",context)

def login_api(request):
    
    print(request.COOKIES)

    if request.user.is_authenticated:
        return JsonResponse({'sessionid': 'erro'})
    
    if request.method == 'POST':
        print(request.POST)
        try:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            login(request, user)
            ip = get_client_ip(request)
            registra_log(user.username,ip,'login')
            return JsonResponse({'sessionid': request.session.session_key})
        except:
            form = LoginForm()
            context = {
                'form' : form,
                'erro_login' : 'erro'
            }
            return JsonResponse({'sessionid': 'erro'})



def dados_api(request):
    
    print(request.COOKIES)
    
    if request.user.is_superuser:
        if request.method == 'POST':
            dados = request.POST['dados']
            periodo = request.POST['periodo']
            key = periodo
            dados = json.loads(dados)
            cache.set(key, dados, None)
            return JsonResponse({'result': 'ok'})
    return JsonResponse({'result': 'erro'})

def cats_api(request):
    
    print(request.COOKIES)
    
    if request.user.is_superuser:
        if request.method == 'POST':
            cats = request.POST['cats']
            print(cats)
            key = 'cats'
            cats = json.loads(cats)
            print(cats)
            cache.set(key, cats, None)
            return JsonResponse({'result': 'ok'})
    return JsonResponse({'result': 'erro'})

    
def params_consulta_api(request):
    
    print(request.COOKIES)
    cols_erp = list(ColecaoErp.objects.filter(colecaoB2b__active=True).values_list('codigo', flat=True).distinct())
    tabelas = list(User.objects.all().values_list('first_name', flat=True).distinct())
    periodos = list(Periodo.objects.filter(Q(periodo_faturamento__gt=date.today()) | Q(desc_periodo='Imediato')).order_by(
                'periodo_faturamento').values())
    #User.objects.filter(Q(periodo_faturamento__gt=date.today()) | Q(desc_periodo='Imediato'))
    # periodos = list(Periodo.objects.filter(
    #     periodo_faturamento__gt=date.today()).order_by(
    #         'periodo_faturamento').values_list('desc_periodo', flat=True).distinct())
    return JsonResponse({'cols': cols_erp,'tabelas':tabelas,'periodos':periodos})


def logout_view(request):

    logout(request)
    return redirect('home')

   
def limpa_cache(request):
    if request.user.is_authenticated:
        cache.delete("dados")
        cache.delete("Processo")
        cache.delete("Imediato")
        cache.delete("df_30dias")
        cache.delete("df_Imediato")
        return redirect('home') 
    else:
        return redirect('/login')


def users_log(request):
    try:
        user = request.GET['user']
        pwd = request.GET['pwd']
        user = authenticate(username=user, password=pwd)
        if user.is_superuser:
            log = Eventos.objects.all()
            return render_to_csv_response(log)
        else:
            return redirect('/login')
    except:
        return redirect('/login')