class Gondolas_Centrais:
    def __init__(self, num_conjuntos, num_modulos, comprimento, profundidade, base, altura):
        self.num_conjuntos = num_conjuntos
        self.num_modulos = num_modulos
        self.comprimento = comprimento
        self.profundidade = profundidade
        self.base = base
        self.altura = altura

        if self.altura not in [1350, 1650, 1950]:
            raise ValueError("Altura inválida. Use 1350, 1650 ou 1950.")

    def blanc_componentes(self):
        return {
            'coluna': {
                'comprimento': self.altura,
                'largura': 140,
                'peso_m2': 16
            },
            'base_coluna': {
                'comprimento': self.profundidade + 10,
                'largura': 196,
                'peso_m2': 16
            },
            'fech_base': {
                'comprimento': self.profundidade + 35,
                'largura': 113,
                'peso_m2': 16
            },
            'painel': {
                'comprimento': self.comprimento + 38,
                'largura': 351,
                'peso_m2': 3.6
            },
            'prateleira_920x300': {
                'comprimento': self.comprimento + 57,
                'largura': self.profundidade + 85,
                'peso_m2': 4.8
            },
            'prateleira_base': {
                'comprimento': self.comprimento + 54,
                'largura': self.base + 85,
                'peso_m2': 4.8
            },
            'reforço': {
                'comprimento': self.comprimento - 10,
                'largura': 100
            },
            'consoles': {
                'comprimento': self.profundidade + 53,
                'largura': 133,
                'peso_m2': 12.2
            }
        }

    def qtd_componentes(self):
        altura_para_paineis_prateleiras = {
            1950: {'painel': 12, 'prateleira': 10},
            1650: {'painel': 10, 'prateleira': 8},
            1350: {'painel': 8,  'prateleira': 6}
        }

        qtd = altura_para_paineis_prateleiras[self.altura]

        return {
            'coluna_central': (self.num_modulos + 1) * self.num_conjuntos,
            'painel_910x300': self.num_modulos * qtd['painel'] * self.num_conjuntos,
            'prateleira_920x300': self.num_modulos * qtd['prateleira'] * self.num_conjuntos,
            'prateleira_base_920x420': self.num_modulos * 2 * self.num_conjuntos,
            'consoles': self.num_modulos * qtd['prateleira'] * self.num_conjuntos
        }

def main():
    print("--- Configuração da Gôndola ---")
    num_conjuntos = int(input("Número de conjuntos: "))
    num_modulos = int(input("Número de módulos: "))
    comprimento = int(input("Comprimento: "))
    profundidade = int(input("Profundidade: "))
    base = int(input("Base: "))
    altura = int(input("Altura (1350, 1650, 1950): "))

    gondola = Gondolas_Centrais(num_conjuntos, num_modulos, comprimento, profundidade, base, altura)

    componentes = gondola.blanc_componentes()
    qtd_componentes = gondola.qtd_componentes()

    print("\n--- Componentes ---")
    for componente, specs in componentes.items():
        print(f"{componente}: {specs}")

    print("\n--- Quantidade de Componentes ---")
    for componente, quantidade in qtd_componentes.items():
        print(f"{componente}: {quantidade}")

if __name__ == "__main__":
    main()