import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler


# Aqui carregamos os dados
colunas  = ['usuario_id', 'filem_id','nota', 'timestamp']
df = pd.read_csv('ml100k/u.data', sp ='\t', names = colunas)

matriz = df.pivot_table( index = 'usuario_id', coluns ='filme_id', values = 'nota' )

matriz.fillna(0, inplace = True)

similaridade = cosine_similarity(matriz)

def recomendar_filems(usuario_id, n = 5):
    sim_scores = list(enumerate(similaridade[usuario_id -1]))
    sim_scores = sorted(sim_scores, key = lambda x: x[1], reverse = True)
    usuarios_similares = [ i for i , _ in sim_scores[1:6]]

    recomendacoes = matriz.iloc[usuarios_similares].mean(axis = 0)

    filmes_assistidos = matriz.iloc[usuario_id - 1]
    recomendacoes = recomendacoes[filmes_assistidos == 0]

    return recomendacoes.sort_values(ascending = False).head(n)

print("Filmes recomendados para o usuário 1:")
print(recomendar_filems(1))