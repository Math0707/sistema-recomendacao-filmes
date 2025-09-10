import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity

# -------------------------
# 1. Carregar os dados
# -------------------------

colunas = ['usuario_id', 'filme_id', 'nota', 'timestamp']
df = pd.read_csv('ml-100k/u.data', sep='\t', names=colunas)  # ✅ CORRETO

# -------------------------
# 2. Análise gráfica - Distribuição das notas
# -------------------------

sns.set(style="whitegrid")
sns.histplot(df['nota'], bins=5, kde=True)

plt.title('Distribuição de Notas dos Filmes')
plt.xlabel('Nota')
plt.ylabel('Frequência')
plt.show()

# -------------------------
# 3. Criar matriz usuário-filme
# -------------------------

matriz = df.pivot_table(index='usuario_id', columns='filme_id', values='nota')
matriz.fillna(0, inplace=True)

# -------------------------
# 4. Calcular similaridade entre usuários
# -------------------------

similaridade = cosine_similarity(matriz)

# -------------------------
# 5. Função de recomendação com nomes dos filmes
# -------------------------

def recomendar_filmes(usuario_id, n=5):
    sim_scores = list(enumerate(similaridade[usuario_id - 1]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    usuarios_similares = [i for i, _ in sim_scores[1:6]]

    recomendacoes = matriz.iloc[usuarios_similares].mean(axis=0)
    filmes_assistidos = matriz.iloc[usuario_id - 1]
    recomendacoes = recomendacoes[filmes_assistidos == 0]
    top_filmes = recomendacoes.sort_values(ascending=False).head(n)

    # Carregar nomes dos filmes
    filmes_cols = ['filme_id', 'titulo', 'genero1', 'genero2', 'genero3', 'genero4', 'genero5',
                   'genero6', 'genero7', 'genero8', 'genero9', 'genero10', 'genero11', 'genero12',
                   'genero13', 'genero14', 'genero15', 'genero16', 'genero17', 'genero18', 'genero19']
    
    filmes_df = pd.read_csv('ml-100k/u.item', sep='|', encoding='latin-1', names=filmes_cols, usecols=[0,1])

    # Juntar nomes dos filmes com as recomendações
    resultados = pd.DataFrame({
        'filme_id': top_filmes.index,
        'nota_prevista': top_filmes.values
    })

    resultados = resultados.merge(filmes_df, on='filme_id')
    resultados = resultados[['titulo', 'nota_prevista']]

    return resultados

# -------------------------
# 6. Testar a recomendação
# -------------------------

print("Filmes recomendados para o usuário 1:")
print(recomendar_filmes(1))
