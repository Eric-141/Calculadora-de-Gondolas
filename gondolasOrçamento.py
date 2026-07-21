import pandas as pd
import streamlit as st

# Constante para o nome do arquivo de imagem local
NOME_IMAGEM = "PackageShelving by E-Z Shelving Systems.png"

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
        
        # Quantidade de prateleiras padrão
        qtd_prateleiras = self.num_modulos * qtd["prateleira"] * self.num_conjuntos
        
        return {
            "Coluna Central": (self.num_modulos + 1) * self.num_conjuntos,
            "Painel 910x300": (
                self.num_modulos * qtd["painel"] * self.num_conjuntos
            ),
            "Prateleira 920x300": qtd_prateleiras,
            "Prateleira Base 920x420": self.num_modulos * 2 * self.num_conjuntos,
            # Regra: Consoles devem ser exatamente o dobro da quantidade de prateleiras
            "Consoles": qtd_prateleiras * 2,
        }


# Configuração da página com imagem real como favicon
try:
    st.set_page_config(
        page_title="Calculadora de Gôndolas",
        page_icon=NOME_IMAGEM,
        layout="centered"
    )
except FileNotFoundError:
    st.warning(f"Arquivo de imagem '{NOME_IMAGEM}' não encontrado para o favicon.")
    st.set_page_config(page_title="Calculadora de Gôndolas", layout="centered")

# Cabeçalho com imagem destacada
try:
    st.image(NOME_IMAGEM, width=300, caption="Gôndola Central Amapá Flex Kit")
except FileNotFoundError:
    st.error(f"Erro: A imagem '{NOME_IMAGEM}' não foi encontrada. Certifique-se de que ela está na mesma pasta do script.")

st.title("Calculadora de Gôndolas Centrais")
st.write("Insira os parâmetros abaixo para calcular os componentes e orçamentos.")

st.sidebar.header("Parâmetros de Entrada")
num_conjuntos = st.sidebar.number_input(
    "Número de Conjuntos", min_value=1, value=3
)
num_modulos = st.sidebar.number_input("Número de Módulos", min_value=1, value=8)
comprimento = st.sidebar.number_input("Comprimento", value=920.0)
profundidade = st.sidebar.number_input("Profundidade", value=300.0)
base = st.sidebar.number_input("Base", value=420.0)
altura = st.sidebar.selectbox("Altura (mm)", [1350, 1650, 1950], index=2)

# Seção de Tabela de Preços Unitários na Barra Lateral
st.sidebar.markdown("---")
st.sidebar.header("Tabela de Preços (R$ Unitário)")
preco_coluna = st.sidebar.number_input("Coluna Central", value=45.00, step=1.0)
preco_painel = st.sidebar.number_input("Painel 910x300", value=30.00, step=1.0)
preco_prat = st.sidebar.number_input("Prateleira 920x300", value=25.00, step=1.0)
preco_base = st.sidebar.number_input("Prateleira Base 920x420", value=35.00, step=1.0)
preco_consoles = st.sidebar.number_input("Consoles", value=12.00, step=1.0)

precos_dict = {
    "Coluna Central": preco_coluna,
    "Painel 910x300": preco_painel,
    "Prateleira 920x300": preco_prat,
    "Prateleira Base 920x420": preco_base,
    "Consoles": preco_consoles,
}

if st.button("Calcular Componentes e Orçamento", type="primary"):
  try:
    gondola = Gondolas_Centrais(
        num_conjuntos, num_modulos, comprimento, profundidade, base, altura
    )
    resultados = gondola.qtd_componentes()

    st.success("Cálculo realizado com sucesso!")
    st.subheader("Resultados e Orçamento Detalhado:")

    # Montagem dos dados combinando quantidade e valores unitários/totais
    dados_tabela = []
    orcamento_total = 0.0

    for componente, qtd in resultados.items():
        v_unitario = precos_dict.get(componente, 0.0)
        v_total = qtd * v_unitario
        orcamento_total += v_total
        dados_tabela.append({
            "Componente": componente,
            "Quantidade": qtd,
            "Valor Unitário (R$)": f"R$ {v_unitario:.2f}",
            "Valor Total (R$)": f"R$ {v_total:.2f}"
        })

    df = pd.DataFrame(dados_tabela)
    st.dataframe(df, use_container_width=True)

    # Exibição do valor total geral do orçamento
    st.metric(label="Orçamento Total da Estrutura", value=f"R$ {orcamento_total:.2f}")

  except Exception as e:
    st.error(f"Erro ao calcular: {e}")