from django.core.cache import cache
from params.models import (ColecaoErp)
from django.contrib.auth.models import User

class Produto():
    pass
class Estoque():
    pass

def get_produtos(tabela,colecao,categoria,subcategoria,periodo):

    key = periodo
    print('chave : ' + key)

    if cache.get(key) is None:
        print('Sem Dados na Cache')
    else:
        print('Cache')
        prods = cache.get(key)

    #Busca cols erp vinculadas a colecao b2b selecionada
    if colecao != '':
        cols_erp = list(ColecaoErp.objects.filter(colecaoB2b__title=colecao).values_list('codigo', flat=True).distinct()) 
        prods = list(filter(lambda x: x['colecao'] in cols_erp, prods))
    
    if categoria != '':
        prods = list(filter(lambda x: x['categoria'] == categoria, prods))
    if subcategoria != '':
        prods = list(filter(lambda x: x['subcategoria'] == subcategoria, prods))

    prods = list(filter(lambda x: x['tabela'] == tabela, prods))

    return prods


def get_produto(produto,tabela,periodo):

    key = periodo
    print('chave : ' + key)

    if cache.get(key) is None:
        print('Sem Dados na Cache')
    else:
        print('Cache')
        prods = cache.get(key)

    prods = list(filter(lambda x: x['produto'] == produto, prods))
    prods = list(filter(lambda x: x['tabela'] == tabela, prods))
    prod = prods[0]

    return prod
 
