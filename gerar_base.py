import argparse
import rotinas as r
import xlwt

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from os import listdir

def main():
    # recupera lista de arquivos xls
    lista_xls = [x for x in listdir("classificados/") if x.endswith(".xls")]
    

if __name__ == '__main__':
    main()