import xlrd
from gensim.models import KeyedVectors
import subprocess
import re

"""faz o carregamento da base psicolinguista em um dictionary
"""


def carregar_base_psico():
    # variável que irá ser retornada do tipo dict
    psic_dict = {}
    # leitura do arquivo xlsx
    book = xlrd.open_workbook("bases/psico_dict.xls",
                              on_demand=True)
    sh = book.sheet_by_index(0)

    for rx in range(1, sh.nrows):
        word = sh.cell_value(rx, colx=0)
        concreteness = sh.cell_value(rx, colx=1)
        imagery = sh.cell_value(rx, colx=2)
        familiarity = sh.cell_value(rx, colx=3)
        aoa = sh.cell_value(rx, colx=4)

        # carregamento de um dictionary com 4 informações
        psic_dict[word] = [concreteness, imagery, familiarity, aoa]

    book.release_resources()

    # deleção instantane da váriavel pois o arquivo é muito extenso
    del book

    return psic_dict



"""carregamento de palavras de baixa frequência
"""


def carregar_base_freq():
    # variável dict de retorno
    freq_dict = {}
    arquivo = "bases/wl_cb_full_1gram_sketchengine.txt"

    # leitura do arquivo .txt
    with open(arquivo) as a:
        linhas = a.readlines()
    a.close()

    linhas = linhas[7:-1]

    for l in linhas:
        item = l.split("\t")
        item[0] = item[0].lower()
        item[1] = int(item[1].replace("\n", ""))

        if item[0] not in freq_dict:
            freq_dict[item[0]] = item[1]
        else:
            freq_dict[item[0]] += item[1]

    return freq_dict

"""retorna uma matriz com as n palavras mais proximas na
   mesma ordem da lista passada como parâmetro
   argumentos

   palavra_central = lista de palavras a serem buscadas
   n = número de palavras próximas a ser retornada
   base = nome da base de embeddings, default skip_s50.txt
"""


def buscar_embeddings(palavra_central, base, n=2):
    embeddings = []

    # carrega modelo passado na variável base
    modelo = KeyedVectors.load_word2vec_format(
            'we/cbow_s50.txt', unicode_errors="ignore")
    if base=='sg50':
        modelo = KeyedVectors.load_word2vec_format(
            'we/skip_s50.txt', unicode_errors="ignore")
    elif base=='g50':
        modelo = KeyedVectors.load_word2vec_format(
            'we/glove_s50.txt', unicode_errors="ignore")


    for p in palavra_central:
        if p in modelo.wv.vocab:
            # ranking de embeddings
            temp  = modelo.most_similar_cosmul(positive=[p],
                                               negative=[],
                                               topn=n)
            temp = [item[0] for item in temp]
            embeddings.append(temp)
        else:
            embeddings.append([])
    return embeddings

"""lematizacao do arquivo palavras.txt na pasta temp"""


def lematizacao():

    # lista que será retornada
    lemma = []
    subprocess.call(['java',
                     '-jar',
                     'lematizador.jar',
                     'tmp/palavras.txt',
                     'nf'])

    subprocess.call(['rm',
                     'tmp/palavras.txt',
                     'tmp/palavras.txt.mxp',
                     'tmp/palavras.txt.tagged'])


    path = 'tmp/palavras.txt.out'

    with open(path) as arq:
        for linhas in arq:
            linhas = re.sub(' \(.*?\)', '', linhas).strip()
            linhas = linhas.replace(' \n', '').split(' ')
            lemma.append(linhas)
    arq.close()

    subprocess.call(['rm', 'tmp/palavras.txt.out'])
    return lemma

""" calcula a distância manhatan entre dois vetores passados
    vec1 e vec2 são listas com as n dimensões de vetores
"""


def manhattan_distance(vec1, vec2):
    dist = 0.0
    vec2 = vec2[0]

    for v1, v2 in zip(vec1, vec2):
        dist += abs(v1-v2)
    return dist

""" retorna vetor de embeddings de 1xn array de palavras, todas as palavras
    todas as palavras devem ja estar na base, nao ha checagem
"""


def retornar_vetor(lista_palavras, base):
    retorno = []

    # carrega modelo passado na variável base
    modelo = KeyedVectors.load_word2vec_format(
            'we/cbow_s50.txt', unicode_errors="ignore")
    if base == 'sg50':
        modelo = KeyedVectors.load_word2vec_format(
            'we/skip_s50.txt', unicode_errors="ignore")
    elif base == 'g50':
        modelo = KeyedVectors.load_word2vec_format(
            'we/glove_s50.txt', unicode_errors="ignore")

    for lp in lista_palavras:
        retorno.append(modelo[lp])
    return retorno
