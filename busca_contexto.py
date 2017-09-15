import argparse
from nltk.tokenize import word_tokenize

def parse_argumentos():
    parser = argparse.ArgumentParser()
    parser.add_argument('nome_texto',
                        default='Embeddings/EST_2014_01_000496.txt',
                        help='Caminho do texto.')
    return parser.parse_args()

def carregar_texto(filepath):

    texto = ''

    with open(filepath) as arq:
        for linhas in arq:
            texto += linhas
    arq.close()

    # tokenização
    texto = word_tokenize(texto)

    return texto

def main():
    args = parse_argumentos()
    texto = carregar_texto(args.nome_texto)
    while(True):
        nb = int(input('Posicao: '))
        aux = 0 if (nb - 20) < 0 else (nb-20)
        print('----------')
        for item in texto[aux:nb]:
            print(item, end=" ")
        print('')
        print(texto[nb])

        for item in texto[nb+1:nb+20]:
            print(item, end=" ")
        print('')
        print('----------')

if __name__ == '__main__' :
    main()
