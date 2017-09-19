import argparse
import rotinas as r
import xlwt
import xlrd

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from xlrd import open_workbook
from xlutils.copy import copy

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
            cl.append(0)

        if cd[1] in psic_dict:
            cl.append(psic_dict[cd[1]])
        else:
            cl.append(0)

    rb = open_workbook(args.filename)
    wb = copy(rb)
    s = wb.get_sheet(0)
    #wb.save('names.xls')

    print("---> 9. Buscando WE")
    tamanho = len(classificados)
    anterior = []

    for elem_index, elem in enumerate(classificados):
        # escreve numeros
        elem.append(r.retornar_vetor([elem[2]], we))
        elem.append(r.retornar_vetor([elem[3]], we))

        for tf_index, tf in enumerate(txt_filtrado):
            if tf[0] == elem[1]:
                elem.append(r.retornar_vetor([txt_filtrado[tf_index-1]], we))
                elem.append(r.retornar_vetor([txt_filtrado[tf_index+1]], we))


        for we_cdt, psico_cdt in zip(we_cand, psico_list):
            coluna = 0
            # grava nome da amostra
            nome_amostra = nome_treinamento + '_' + str(
                elem_index) + '_' + str(num_amostra)
            ws1.write(it2, coluna, nome_amostra)
            num_amostra += 1

            # grava distancia entre vetores
            coluna += 1
            distancia = r.manhattan_distance(we_orig, we_cand)
            ws1.write(it2, coluna, distancia)

            # grava 8 informacoes psico
            coluna += 1
            for psc1, psc2, in zip(psico_orig, psico_cdt):
                ws1.write(it2, coluna, psc1)
                ws1.write(it2, coluna + 4, psc2)
                coluna += 1

            # grava embeddings orig e cand
            coluna += 4
            for we1, we2 in zip(we_orig, we_cdt):
                ws1.write(it2, coluna, we1.astype(float))
                ws1.write(it2, coluna + 50, we2.astype(float))
                coluna += 1

            coluna += 50
            for we1, we2 in zip(anterior, posterior):
                ws1.write(it2, coluna, we1.astype(float))
                ws1.write(it2, coluna + 50, we2.astype(float))
                coluna += 1
            it2 += 1
        anterior = we_orig
        # printa a porcentagem de candidatas escritas
        pctg = (elem_index / (tamanho - 2)) * 100
        print("        (  {0:3.1f}% )".format(pctg))


    print("--->10. Salvando XLS")
    wb.save('treinamento/' + nome_treinamento + '.xls')


if __name__ == '__main__':
    main()