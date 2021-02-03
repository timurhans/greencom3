#DJANGO IMPORTS
from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.contrib.auth import authenticate, login, logout
<<<<<<< HEAD
from django.http import HttpResponse
=======
from django.contrib.auth.models import User
from django.http import HttpResponse,JsonResponse
>>>>>>> 8a45137b9376bd9d457abf976e6a9af0f9dc5c97
from django.core.cache import cache
from django.template.loader import get_template
from django.core.files.storage import FileSystemStorage
from django.conf import settings
<<<<<<< HEAD
#APP IMPORTS
from .ondas import (Produto,Estoque,cats_subcats,get_produto,prods_sem_imagem,get_produtos)
from .models import Eventos
from .forms import LoginForm
from params.models import (ColecaoB2b,ColecaoErp,Banner)
# THIRD PARTY IMPORTS
from xhtml2pdf import pisa
=======
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
>>>>>>> 8a45137b9376bd9d457abf976e6a9af0f9dc5c97
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

<<<<<<< HEAD
=======
class Produto():
    pass

>>>>>>> 8a45137b9376bd9d457abf976e6a9af0f9dc5c97
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
<<<<<<< HEAD
            item.valor_item = round(item.qtd_item*pedido.produto.preco,2)
            itens.append(item)
    pedido.qtd_tot = qtd_tot
    pedido.valor_tot = round(qtd_tot*pedido.produto.preco,2)
=======
            item.valor_item = round(item.qtd_item*pedido.produto['preco'],2)
            itens.append(item)
    pedido.qtd_tot = qtd_tot
    pedido.valor_tot = round(qtd_tot*pedido.produto['preco'],2)
>>>>>>> 8a45137b9376bd9d457abf976e6a9af0f9dc5c97
    if len(itens)>0:
        pedido.itens = itens #qtd pedido

        if cache.get(session) is None:
            pedidos = []
            pedidos.append(pedido)   
            cache.set(session, pedidos, 60*60)
        else:
            pedidos = cache.get(session)
<<<<<<< HEAD
            if any(x.produto.produto == pedido.produto.produto for x in pedidos):
                pedidos = [pedido if x.produto.produto == pedido.produto.produto else x for x in pedidos]
=======
            if any(x.produto['produto'] == pedido.produto['produto'] for x in pedidos):
                pedidos = [pedido if x.produto['produto'] == pedido.produto['produto'] else x for x in pedidos]
>>>>>>> 8a45137b9376bd9d457abf976e6a9af0f9dc5c97
            else:
                pedidos.append(pedido)
            cache.set(session, pedidos, 60*60)



# VIEWS DA APLICACAO

def produtos(request,path=None):

    colecoes = list(ColecaoB2b.objects.filter(active=True).order_by('ordem').values_list('title', flat=True).distinct())
    banners = Banner.objects.all().order_by('ordem')

    page_size = 16

<<<<<<< HEAD
=======
    print(request.COOKIES)
>>>>>>> 8a45137b9376bd9d457abf976e6a9af0f9dc5c97
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
<<<<<<< HEAD
=======
        #filtra periodos que ja passaram
        periodos = list(Periodo.objects.filter(Q(periodo_faturamento__gt=date.today()) | Q(desc_periodo='Imediato')).order_by(
                'periodo_faturamento').values_list('desc_periodo', flat=True).distinct())
>>>>>>> 8a45137b9376bd9d457abf976e6a9af0f9dc5c97
        if qtd_prods>page_size:
            is_paginated = True
        else:
            is_paginated = False

<<<<<<< HEAD
        cats = cats_subcats()
=======
        cats = cache.get('cats')
>>>>>>> 8a45137b9376bd9d457abf976e6a9af0f9dc5c97
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
<<<<<<< HEAD
        'banners' : banners
=======
        'banners' : banners,
        'periodos' : periodos
>>>>>>> 8a45137b9376bd9d457abf976e6a9af0f9dc5c97
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
<<<<<<< HEAD
                adciona_carrinho(request)
=======
                try:
                    periodo = request.POST.get('periodo')
                except:
                    periodo = 'Imediato'                
                adciona_carrinho(request,periodo)
>>>>>>> 8a45137b9376bd9d457abf976e6a9af0f9dc5c97
                return HttpResponse('<script>history.back();</script>')
            elif request.POST.get('remove') is not None:
                #exclusao carrinho
                produto = request.POST.get('produto')
                print(produto)
                pedidos = cache.get(session)
<<<<<<< HEAD
                pedidos = list(filter(lambda x: x.produto.produto != produto, pedidos))
=======
                pedidos = list(filter(lambda x: x.produto['produto'] != produto, pedidos))
>>>>>>> 8a45137b9376bd9d457abf976e6a9af0f9dc5c97
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

<<<<<<< HEAD
        cats = cats_subcats()
=======
        cats = cache.get('cats')
>>>>>>> 8a45137b9376bd9d457abf976e6a9af0f9dc5c97
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
    
<<<<<<< HEAD
=======
    print(request.COOKIES)

>>>>>>> 8a45137b9376bd9d457abf976e6a9af0f9dc5c97
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

<<<<<<< HEAD



def logout_view(request):

    logout(request)
    return redirect('home')


def upload_img(request):


    if request.user.is_superuser:
        session = request.COOKIES.get('sessionid')
        dir_imports = 'static/imports/'
        dir_imports_session = dir_imports + session+'/' #pasta para sessao para nao ter conflito na importacao
        dir_imgs = 'static/imgs/'
        if request.method == 'POST':
            try:
                myfile = request.FILES['myfile']
            except:
                return render(request, 'core/upload.html')
            fs = FileSystemStorage() 
            filename = fs.save(dir_imports+myfile.name, myfile) # salva arquivo
            zip_ref = zipfile.ZipFile(filename)
            zip_ref.extractall(dir_imports_session) # extrai para pasta da sessao
            zip_ref.close()
            os.remove(filename) #exlui arquivo zip
            fotos = glob.glob(dir_imports_session+'**/*.jpg', recursive=True) # busca todos os arquivos jpg recursivamente
            cont_novas = 0
            cont_atualiz = 0
            for f in fotos:
                novo_path = dir_imgs+ntpath.basename(f)
                # novo_path = dir_imgs+os.path.basename(f)
                # novo_path = dir_imgs+f.rsplit(os.sep,1)[-1]
                if glob.glob(novo_path):
                    cont_atualiz = cont_atualiz+1
                else:
                    cont_novas = cont_novas+1
                print(novo_path)
                os.replace(f, novo_path) # move para a pasta imgs

            shutil.rmtree(dir_imports_session) #exclui pasta sessao
            return render(request, 'core/upload.html', {
                'novas': cont_novas,
                'atualizadas' : cont_atualiz
            })
        return render(request, 'core/upload.html')
    else:
        return redirect('/login')    

=======
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

   
>>>>>>> 8a45137b9376bd9d457abf976e6a9af0f9dc5c97
def limpa_cache(request):
    if request.user.is_authenticated:
        cache.delete("dados")
        cache.delete("Processo")
        cache.delete("Imediato")
<<<<<<< HEAD
=======
        cache.delete("df_30dias")
        cache.delete("df_Imediato")
>>>>>>> 8a45137b9376bd9d457abf976e6a9af0f9dc5c97
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
<<<<<<< HEAD
        return redirect('/login')


def produtos_sem_imagem_view(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="prods_sem_img.csv"'
    prods = prods_sem_imagem()
    writer = csv.writer(response)
    writer.writerow(['PRODUTO', 'COLECAO', 'DISP'])
    for index,row in prods.iterrows():
        writer.writerow([row['PRODUTO'], row['COLECAO'], row['DISP']])

    return response
=======
        return redirect('/login')
>>>>>>> 8a45137b9376bd9d457abf976e6a9af0f9dc5c97
