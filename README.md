# 🎬 Sistema de Recomendação de Filmes

Este projeto implementa um **sistema de recomendação baseado em usuários** utilizando o dataset [MovieLens 100k](https://grouplens.org/datasets/movielens/100k/).  
A aplicação foi desenvolvida em **Python** e disponibilizada em uma interface interativa com **Streamlit**.

---

## 🚀 Funcionalidades
- Exibir os **últimos filmes avaliados** por um usuário.
- Recomendar novos filmes utilizando **similaridade de usuários** (Collaborative Filtering).
- Exibir recomendações em **cards com título, nota prevista e pôster**.
- Interface simples e intuitiva feita com **Streamlit**.

---

## 🛠️ Tecnologias Utilizadas
- [Python 3](https://www.python.org/)
- [Pandas](https://pandas.pydata.org/)
- [NumPy](https://numpy.org/)
- [scikit-learn](https://scikit-learn.org/)
- [Streamlit](https://streamlit.io/)

---

## 📂 Estrutura do Projeto
├── ml-100k/
│ ├── u.data # Avaliações dos usuários
│ ├── u.item # Lista de filmes
├── recomendador_filmes.py # Código principal
└── README.md


Criar e ativar um ambiente virtual (opcional, mas recomendado)

python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate


Instalar as dependências

pip install -r requirements.txt


(caso não tenha o requirements.txt, instale manualmente:)

pip install pandas numpy scikit-learn streamlit


Rodar a aplicação

streamlit run recomendador_filmes.py


Abra no navegador o endereço:

http://localhost:8501


1. Clone este repositório:

```bash
git clone https://github.com/Math0707/sistema-recomendacao-filmes.git
cd sistema-recomendacao-filmes
