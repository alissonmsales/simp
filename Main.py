import argparse
import xlwt
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import rotinas as r


def parse_argumentos():
    parser = argparse.ArgumentParser()
    parser.add_argument('-we',
                        choices=['sg50', 'cb50', 'g50'],
                        default=['cb50'],
                        help='Base de embedding a ser utilizada.')
    parser.add_argument('-viz',
                        default=4,
                        help='Número de vizinhos da palavra original a '
                             'retornar como candidatas.')
    parser.add_argument('-texto',
                        default='Embeddings/EST_2014_01_000496.txt',
                        help='Caminho do texto.')
    return parser.parse_args()


def main():
    # faz o parse dos argumentos recebidos
    args = parse_argumentos()
    nome_treinamento = args.texto
    nome_treinamento = nome_treinamento.split('/')[1].split('.')[0]
    nome_treinamento += '_'+args.we
    # entrada do texto original
    # arq_txt = "Embeddings/EST_2014_01_000495_cleaned.txt"
    # nome_treinamento = 'EST_2014_01_000495'

    txt_orig = ""
    # apenas os indices do texto tokenizado original
    txt_filtrado = []
    candidatas = []
    candidatas_dict = {}

    # controle
    print("---> 1. Carregando Texto")

    with open(args.texto) as arq:
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
        if w.lower() not in (stopwords.words('portuguese')+stop_words):
            """ armazena apenas o indice da palavra que nao e stop-word """
            txt_filtrado.append([w_index, w.lower()])
    print("        (", len(txt_filtrado), ")")
    # controle
    print("---> 4. Buscando Palavras na Base de Embeddings")

    # buscar embeddigs à lista e dá um append nas candidatas
    temp = [item[1] for item in txt_filtrado]
    temp = r.buscar_embeddings(temp, args.we, int(args.viz))
    # txt_filtrado = [a.append(b)
    for a, b in zip(txt_filtrado, temp):
        if b:
            candidatas.append([a[0], a[1], b])
            candidatas_dict[a[0]] = a[1]

    # controle
    print("---> 5. Eliminando Candidatas de Menor Frequência")

    # remoção de palavras com maior frequência
    freq_dict = r.carregar_base_freq()
    print(len(freq_dict))
    eliminar = []
    # palavra do texto
    for c_index, c in enumerate(candidatas):
        # print(c)
        k = c[1]
        if k in freq_dict and freq_dict[k]<3000:
            # print(k,': palavra no dic')
            # palavra candidata
            #print(c[2])
            for cand in reversed(c[2]):
                if cand not in freq_dict:
                    # print('cand removida pq nao ta na base de frequencia')
                    c[2].remove(cand)
                    #print('-', cand)
                # -300 é um número arbitrário
                elif (freq_dict[cand]-500) < freq_dict[k]:
                    #print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>', cand, str(freq_dict[cand]),str(freq_dict[cand]-300), k, str(freq_dict[k]))
                    c[2].remove(cand)
                    #print('-', cand)
                    # print('cand removida pq freq menor que palavra original')
                #else:
                    #print('+', cand)
            #print(c[2])

            if not c[2]:
                #print('< acabou candidatas >')
                eliminar.append(c_index)
        else:
            #print('ausencia na base de frequencia: ', k)
            eliminar.append(c_index)
    del freq_dict
    for e in reversed(eliminar):
        #print('pos:', e, 'palavra:', candidatas[e])
        del candidatas[e]
    print("        (", len(candidatas), ")")
    # controle
    print("---> 6. Salvando Palaras Para Lematizar")

    # gravar arquivo texto com as palavras
    path = 'tmp/palavras.txt'
    with open(path, "w+") as arq:
        for t in candidatas:
            k = [t[1]]+t[2]
            for elem in k:
                arq.write("%s " % elem)
            arq.write("\n")
    arq.close()

    # controle
    #print("---> 7. Lematização")
    candidatas = zip(candidatas, r.lematizacao())
    new_candidatas = []

    for t in candidatas:
        lista1 = t[0][:2]
        lista2 = t[0][2]
        lista2.insert(0, t[0][1])
        lista3 = t[1]
        print('tamanho listas: ', len(lista2), len(lista3))
        print(lista2)
        print(lista3)
        if len(lista2) == len(lista3):
            for i in reversed(range(1, len(lista3))):
                print(lista3[0], lista3[i])
                if lista3[0] == lista3[i]:
                    print('<< excluido >>')
                    del lista3[i]
                    del lista2[i]
            new_candidatas.append([lista1, lista2, lista3, []])
    del candidatas
    print(new_candidatas)

    # controle
    print("---> 8. Buscando Informações Psicolinguisticas")
    # adicionar info psico
    psic_dict = r.carregar_base_psico()
    remover = []
    for t_index, t in enumerate(new_candidatas):
        if t[2][0] in psic_dict:
            excluir_w = []
            for w_index, w in enumerate(t[2]):
                if w in psic_dict:
                    t[3].append(psic_dict[w])
                else:
                    excluir_w.append(w_index)
            for rev in reversed(excluir_w):
                del t[1][rev]
            if len(t[3]) == 1:
                remover.append(t_index)
        else:
            remover.append(t_index)
    del psic_dict
    for rev in reversed(remover):
        print(str(rev), new_candidatas[rev])
        del new_candidatas[rev]
    #print(new_candidatas)
    print("        (", len(new_candidatas), ")")

    wb = xlwt.Workbook()
    ws1 = wb.add_sheet('entrada')
    ws2 = wb.add_sheet('palavra')

    it = 0
    it2 = 0

    print("---> 9. Buscando WE")
    tamanho = len(new_candidatas)
    anterior = []

    # carregando base de we
    #if args.we == 'cb50':
    #    modelo = KeyedVectors.load_word2vec_format(
    #        'we/cbow_s50.txt', unicode_errors="ignore")
    #elif args.we == 'sg50':
    #    modelo = KeyedVectors.load_word2vec_format(
    #        'we/skip_s50.txt', unicode_errors="ignore")
    #elif args.we == 'g50':
    #    modelo = KeyedVectors.load_word2vec_format(
    #        'we/glove_s50.txt', unicode_errors="ignore")
    #print("        Base de embeddings carregada")
    # fim

    for elem_index, elem in enumerate(new_candidatas):
        if elem_index not in (0, tamanho-1):
            # escreve palavras
            for txt_cand_index, txt_cand in enumerate(elem[1][1:]):
                nome_amostra = nome_treinamento + "_" +\
                               str(elem[0][0]) + "_" +\
                               str(txt_cand_index)
                ws2.write(it, 0, nome_amostra)
                ws2.write(it, 1, elem[0][1])
                ws2.write(it, 2, txt_cand)
                it += 1

            pctg = (elem_index / (tamanho-2)) * 100
            print("        (  {0:3.1f}% )".format(pctg))

        #elif elem_index == 0:
            #anterior = []
            #for lp in [elem[0][1]]:
            #    anterior.append(modelo[lp])

    print("--->10. Salvando XLS")
    wb.save('treinamento/'+nome_treinamento+'.xls')

if __name__ == '__main__':
    main()
