import pandas as pd
import streamlit as st


class Gondolas_Centrais:

  def __init__(
      self, num_conjuntos, num_modulos, comprimento, profundidade, base, altura
  ):
    self.num_conjuntos = int(num_conjuntos)
    self.num_modulos = int(num_modulos)
    self.comprimento = float(comprimento)
    self.profundidade = float(profundidade)
    self.base = float(base)
    self.altura = int(altura)

    if self.altura not in [1350, 1650, 1950]:
      raise ValueError("Altura inválida. Use 1350, 1650 ou 1950.")

  def blanc_componentes(self):
    return {
        "coluna": {
            "comprimento": self.altura,
            "largura": 140,
            "peso_m2": 16,
        },
        "base_coluna": {
            "comprimento": self.profundidade + 10,
            "largura": 196,
            "peso_m2": 16,
        },
        "fech_base": {
            "comprimento": self.profundidade + 35,
            "largura": 113,
            "peso_m2": 16,
        },
        "painel": {
            "comprimento": self.comprimento + 38,
            "largura": 351,
            "peso_m2": 3.6,
        },
        "prateleira_920x300": {
            "comprimento": self.comprimento + 57,
            "largura": self.profundidade + 85,
            "peso_m2": 4.8,
        },
        "prateleira_base": {
            "comprimento": self.comprimento + 54,
            "largura": self.base + 85,
            "peso_m2": 4.8,
        },
        "reforço": {"comprimento": self.comprimento - 10, "largura": 100},
        "consoles": {
            "comprimento": self.profundidade + 53,
            "largura": 133,
            "peso_m2": 12.2,
        },
    }

  def qtd_componentes(self):
    altura_para_paineis_prateleiras = {
        1950: {"painel": 12, "prateleira": 10},
        1650: {"painel": 10, "prateleira": 8},
        1350: {"painel": 8, "prateleira": 6},
    }
    qtd = altura_para_paineis_prateleiras[self.altura]
    return {
        "Coluna Central": (self.num_modulos + 1) * self.num_conjuntos,
        "Painel 910x300": (
            self.num_modulos * qtd["painel"] * self.num_conjuntos
        ),
        "Prateleira 920x300": (
            self.num_modulos * qtd["prateleira"] * self.num_conjuntos
        ),
        "Prateleira Base 920x420": self.num_modulos * 2 * self.num_conjuntos,
        "Consoles": self.num_modulos * qtd["prateleira"] * self.num_conjuntos,
    }


st.set_page_config(
    page_title="Calculadora de Gôndolas", page_icon="🛒", layout="centered"
)

st.title("🛒 Calculadora de Gôndolas Centrais")
st.write("Insira os parâmetros abaixo para calcular os componentes.")

st.sidebar.header("Parâmetros de Entrada")
num_conjuntos = st.sidebar.number_input(
    "Número de Conjuntos", min_value=1, value=3
)
num_modulos = st.sidebar.number_input("Número de Módulos", min_value=1, value=8)
comprimento = st.sidebar.number_input("Comprimento", value=920.0)
profundidade = st.sidebar.number_input("Profundidade", value=300.0)
base = st.sidebar.number_input("Base", value=420.0)
altura = st.sidebar.selectbox("Altura (mm)", [1350, 1650, 1950], index=2)

if st.button("Calcular Componentes", type="primary"):
  try:
    gondola = Gondolas_Centrais(
        num_conjuntos, num_modulos, comprimento, profundidade, base, altura
    )
    resultados = gondola.qtd_componentes()

    st.success("Cálculo realizado com sucesso!")
    st.subheader("Resultados:")

    df = pd.DataFrame(
        list(resultados.items()),
        columns=["Componente", "Quantidade Necessária"],
    )
    st.dataframe(df, use_container_width=True)

  except Exception as e:
    st.error(f"Erro ao calcular: {e}")