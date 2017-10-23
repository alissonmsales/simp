import xlrd, xlwt
from gensim.models import KeyedVectors
from gensim.models.wrappers import FastText
import rotinas as r


def carregar_modelo(pos):
    files = ['we/fasttext_cbow_s50.txt',
             'we/fasttext_skip_s50.txt',
             'we/wang_cbow_s50.txt',
             'we/wang_skip_s50.txt']

    modelo = KeyedVectors.load_word2vec_format(files[pos], unicode_errors="ignore")

    return modelo

# abre xls com palavras
book = xlrd.open_workbook("classificados/cbow/amostras_cb50.xls", on_demand=True)
#book = xlrd.open_workbook("classificados/skip-gram/amostras_sg50.xls", on_demand=True)
#book = xlrd.open_workbook("classificados/glove/amostras_g50.xls", on_demand=True)

# abre sheet de cada um
#sh_cb = book.sheet_by_index(0)
#sh_cb = book.sheet_by_index(0)
sh_cb = book.sheet_by_index(0)

#cria workbook
#fasttext = xlwt.Workbook()
wang2vec = xlwt.Workbook()

# cria sheet pra cada caso
#sheet_cb_fcb = fasttext.add_sheet('cb-fcb')
#sheet_cb_fsg = fasttext.add_sheet('cb-fsg')

sheet_cb_fcb = wang2vec.add_sheet('cb-wcb')
sheet_cb_fsg = wang2vec.add_sheet('cb-wsg')

#sheet_g_fcb = fasttext.add_sheet('g-fcb')
#sheet_g_fsg = fasttext.add_sheet('g-fsg')

#wang2vec.add_sheet('cb-wcb')
#wang2vec.add_sheet('cb-wsg')
#wang2vec.add_sheet('sg-wcb')
#wang2vec.add_sheet('sg-wcg')
#wang2vec.add_sheet('g-wcb')
#wang2vec.add_sheet('g-wcg')
#wang2vec.add_sheet('class')

# fasttext cbow
fcb = carregar_modelo(2)
fsg = carregar_modelo(3)

for rx in range(sh_cb.nrows):
    print('linha: ', str(rx))
    orig = sh_cb.cell_value(rx, colx=2)
    cand = sh_cb.cell_value(rx, colx=3)
    classe = sh_cb.cell_value(rx, colx=4)
    psic = []
    for i in range(5,13):
        psic.append(sh_cb.cell_value(rx, colx=i))

    emb_orig_fcb = fcb[orig]
    emb_cand_fcb = fcb[cand]
    dist_fcb = r.manhattan_distance(emb_orig_fcb, emb_cand_fcb)

    # gravando cb-fcb
    sheet_cb_fcb.write(rx, 0, orig)
    sheet_cb_fcb.write(rx, 1, cand)
    sheet_cb_fcb.write(rx, 2, classe)

    for i in range(8):
        sheet_cb_fcb.write(rx, 3 + i, psic[i])
    for i in range(50):
        sheet_cb_fcb.write(rx, 11 + i, emb_orig_fcb[i].astype(float))
        sheet_cb_fcb.write(rx, 61 + i, emb_cand_fcb[i].astype(float))
    sheet_cb_fcb.write(rx, 111, dist_fcb)

    # gravando cb-fsg
    emb_orig_fsg = fsg[orig]
    emb_cand_fsg = fsg[cand]
    dist_fsg = r.manhattan_distance(emb_orig_fsg, emb_cand_fsg)

    sheet_cb_fsg.write(rx, 0, orig)
    sheet_cb_fsg.write(rx, 1, cand)
    sheet_cb_fsg.write(rx, 2, classe)
    for i in range(8):
        sheet_cb_fsg.write(rx, 3 + i, psic[i])
    for i in range(50):
        sheet_cb_fsg.write(rx, 11 + i, emb_orig_fsg[i].astype(float))
        sheet_cb_fsg.write(rx, 61 + i, emb_cand_fsg[i].astype(float))
    sheet_cb_fsg.write(rx, 111, dist_fsg)


print("--->10. Salvando XLS")
wang2vec.save('classificados/wang/amostras_cb-f50.xls')