# trecho retirado da linha 197

# escreve numeros
      we_all = []



      for lp in elem[1]:
          we_all.append(modelo[lp])

      we_orig = we_all[0]
      we_cand = we_all[1:]
      psico_orig = elem[3][0]
      psico_list = elem[3][1:]

      # reescrita só pra alterar a amostra das candidatas
      num_amostra = 0

      # grava embeddings anterior e posterior
      posterior = []
      for lp in [new_candidatas[elem_index + 1][0][1]]:
          posterior.append(modelo[lp])
      posterior = posterior[0]

      for we_cdt, psico_cdt in zip(we_cand, psico_list):
          coluna = 0
          # grava nome da amostra
          nome_amostra = nome_treinamento + '_' + str(
              elem[0][0]) + '_' + str(num_amostra)
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
              ws1.write(it2, coluna+4, psc2)
              coluna += 1

          # grava embeddings orig e cand
          coluna += 4
          for we1, we2 in zip(we_orig, we_cdt):
              ws1.write(it2, coluna, we1.astype(float))
              ws1.write(it2, coluna+50, we2.astype(float))
              coluna += 1

          coluna += 50

          for we1, we2 in zip(anterior, posterior):
              ws1.write(it2, coluna, we1.astype(float))
              ws1.write(it2, coluna+50, we2.astype(float))
              coluna += 1
          it2 += 1
      anterior = we_orig
      # printa a porcentagem de candidatas escritas
