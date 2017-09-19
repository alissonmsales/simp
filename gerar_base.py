import argparse
import rotinas as r
import xlrd

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from xlrd import open_workbook
from xlutils.copy import copy
from gensim.models import KeyedVectors

def parse_argumentos():
    parser = argparse.ArgumentParser()
    parser.add_argument('-filename',
                        default='classificados/beyonce_cb50_v2.xls',
                        help='Caminho do xls.')
    return parser.parse_args()

def ler_classificados(arq):
    # variável que irá ser retornada do tipo dict
    class_list = []
    # leitura do arquivo xlsx
    book = xlrd.open_workbook(arq, on_demand=True)
    sh = book.sheet_by_index(1)

    for rx in range(0, sh.nrows):
        codigo = sh.cell_value(rx, colx=0)
        #trocar quando tiver duas palavras no nome
        posicao = codigo.split('_')[-2]
        original = sh.cell_value(rx, colx=1)
        candidata = sh.cell_value(rx, colx=2)
        classe = sh.cell_value(rx, colx=3)

        # carregamento de um dictionary com 4 informações
        class_list.append([codigo, posicao, original, candidata, classe])

    book.release_resources()

    # deleção instantane da váriavel pois o arquivo é muito extenso
    del book

    return class_list

def main():
    zeros = [0,0,0,0]
    # faz o parse dos argumentos recebidos
    args = parse_argumentos()
    arquivo = args.filename
    classificados = ler_classificados(arquivo)
    arquivo = arquivo.split("/")[1]
    we = arquivo.split("_")[1]
    texto = arquivo.split("_")[0]

    txt_orig = ""
    # apenas os indices do texto tokenizado original
    txt_filtrado = []
    candidatas = []

    # controle
    print("---> 1. Carregando Texto")
    with open("txt/"+texto+".txt") as arq:
        for linhas in arq:
            txt_orig += linhas
    arq.close()

    # controle
    print("---> 2. Iniciando Tokenização")
    # tokenização
    txt_tokenizado = word_tokenize(txt_orig)
    print("        (", len(txt_tokenizado), ")")

    # controle
    print("---> 3. Removendo Stop Words")
    # remoção de stop-words
    for w_index, w in enumerate(txt_tokenizado):
        stop_words = [',', '.', '(', ')', 'em', ':', 'e', 'é', 'n.º']
        if w.lower() not in (stopwords.words('portuguese') + stop_words):
            """ armazena apenas o indice da palavra que nao e stop-word """
            txt_filtrado.append([w_index, w.lower()])
    print("        (", len(txt_filtrado), ")")

    # controle
    print("---> 6. Salvando Palavras Para Lematizar")
    # gravar arquivo texto com as palavras
    path = 'tmp/palavras.txt'
    with open(path, "w+") as arq:
        for c in classificados:
            k = c[2]+' '+c[3]
            arq.write("%s " % k)
            arq.write("\n")
    arq.close()

    # controle
    print("---> 7. Lematização")
    candidatas = r.lematizacao()
    candidatas.pop()
    # controle
    print("---> 8. Buscando Informações Psicolinguisticas")

    # adicionar info psico
    psic_dict = r.carregar_base_psico()
    for cl, cd in zip(classificados, candidatas):
        if cd[0] in psic_dict:
            cl.append(psic_dict[cd[0]])
        else:
            cl.append(zeros)

        if cd[1] in psic_dict:
            cl.append(psic_dict[cd[1]])
        else:
            cl.append(zeros)

    rb = open_workbook(args.filename)
    wb = copy(rb)
    s = wb.get_sheet(0)

    print("---> 9. Buscando WE")
    tamanho = len(classificados)

    # carrega o modelo de embedding
    modelo = KeyedVectors.load_word2vec_format(
        'we/cbow_s50.txt', unicode_errors="ignore")
    if we == 'sg50':
        modelo = KeyedVectors.load_word2vec_format(
            'we/skip_s50.txt', unicode_errors="ignore")
    elif we == 'g50':
        modelo = KeyedVectors.load_word2vec_format(
            'we/glove_s50.txt', unicode_errors="ignore")

    for elem_index, elem in enumerate(classificados):
        elem.append(modelo[elem[2]])
        elem.append(modelo[elem[3]])

        # adiciona as palavras anterior e posterior
        for tf_index, tf in enumerate(txt_filtrado):
            if tf[0] == int(elem[1]):
                i = 1
                pr = an = True
                while(pr or an):
                    if (txt_filtrado[tf_index-i][1] in modelo.wv.vocab) and an:
                        elem.append(modelo[txt_filtrado[tf_index - i][1]])
                        an = False
                    if (txt_filtrado[tf_index+i][1] in modelo.wv.vocab) and pr:
                        elem.append(modelo[txt_filtrado[tf_index + i][1]])
                        pr = False
                    i+=1
        elem.append(r.manhattan_distance(elem[7], elem[8]))

        # grava as informacoes iniciais
        # nome da amostra
        s.write(elem_index, 0, elem[0])
        # posicao da palavra no texto original
        s.write(elem_index, 1, elem[1])
        # palavra original
        s.write(elem_index, 2, elem[2])
        # palavra candidata
        s.write(elem_index, 3, elem[3])
        # classe
        s.write(elem_index, 4, elem[4])

        # grava os dados psico.
        for i in range(4):
            s.write(elem_index, 5 + i, elem[5][i])
            s.write(elem_index, 9 + i, elem[6][i])

        # grava os embeddings
        for i in range(50):
            s.write(elem_index, 13 + i, (elem[7][i]).astype(float))
            s.write(elem_index, 63 + i, (elem[8][i]).astype(float))
            s.write(elem_index, 113 + i, (elem[9][i]).astype(float))
            s.write(elem_index, 163 + i, (elem[10][i]).astype(float))

        s.write(elem_index, 213, elem[11])

        # printa a porcentagem
        pctg = (elem_index+1 / tamanho) * 100
        print("        (  {0:3.1f}% )".format(pctg))

    del modelo
    print("--->10. Salvando XLS")
    wb.save(args.filename)


if __name__ == '__main__':
    main()