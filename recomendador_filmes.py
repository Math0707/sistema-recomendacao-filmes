import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

# -------------------------
# 1. Carregar os dados
# -------------------------
colunas = ['usuario_id', 'filme_id', 'nota', 'timestamp']
df = pd.read_csv('ml-100k/u.data', sep='\t', names=colunas)

# Matriz usuário x filme
matriz = df.pivot_table(index='usuario_id', columns='filme_id', values='nota')
matriz.fillna(0, inplace=True)

# Similaridade entre usuários
similaridade = cosine_similarity(matriz)

# Carregar filmes
filmes_df = pd.read_csv('ml-100k/u.item', sep='|', encoding='latin-1', usecols=[0,1], names=['filme_id','titulo'])

# -------------------------
# 2. Adicionar pôsteres
# -------------------------
# Se já tiver CSV de pôsteres, use ele:
# filmes_df = pd.read_csv("filmes_com_posters.csv")

# Para teste rápido, placeholder
filmes_df['poster_url'] = "https://via.placeholder.com/200x300.png?text=Sem+Imagem"



# -------------------------
# 3. Funções
# -------------------------
def ultimos_filmes(usuario_id, n=5):
    filmes = matriz.iloc[usuario_id - 1]
    ultimos = filmes[filmes > 0].sort_values(ascending=False).head(n)
    ultimos_df = ultimos.reset_index()
    ultimos_df.columns = ['filme_id','nota']
    ultimos_df = ultimos_df.merge(filmes_df, on='filme_id', how='left')
    return ultimos_df[['titulo','nota']]

def recomendar_filmes(usuario_id, n=5):
    sim_scores = list(enumerate(similaridade[usuario_id - 1]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    usuarios_similares = [i for i,_ in sim_scores[1:6]]

    recomendacoes = matriz.iloc[usuarios_similares].mean(axis=0)
    filmes_assistidos = matriz.iloc[usuario_id - 1]
    recomendacoes = recomendacoes[filmes_assistidos==0]
    top_filmes = recomendacoes.sort_values(ascending=False).head(n)

    resultados = pd.DataFrame({
        'filme_id': top_filmes.index,
        'nota_prevista': top_filmes.values
    })

    resultados = resultados.merge(filmes_df, on='filme_id')
    resultados['usuarios_similares'] = str([u+1 for u in usuarios_similares])
    return resultados[['titulo','nota_prevista','usuarios_similares','poster_url']]

# -------------------------
# 4. Interface Streamlit
# -------------------------
st.set_page_config(page_title="🎬 Recomendador de Filmes", layout="wide")
st.title("🎬 Sistema de Recomendação de Filmes")

usuario_id = st.number_input("Digite o ID do usuário (1 a 943)", min_value=1, max_value=943, value=1)
n = st.slider("Quantas recomendações deseja?", 1, 20, 5)

if st.button("Recomendar"):
    # Últimos filmes
    st.subheader("🎥 Últimos filmes que você avaliou")
    ultimos = ultimos_filmes(usuario_id)
    st.table(ultimos)

    # Recomendações
    resultados = recomendar_filmes(usuario_id, n)
    st.subheader("🍿 Filmes recomendados para você")

    # Layout em cards
    cols = st.columns(min(n,5))
    for i, (_, row) in enumerate(resultados.iterrows()):
        with cols[i % 5]:
            st.image(row['poster_url'], width=120)
            st.markdown(f"**{row['titulo']}**")
            st.markdown(f"Nota prevista: {row['nota_prevista']:.2f}")
            st.markdown(f"_Baseado em usuários: {row['usuarios_similares']}_")
