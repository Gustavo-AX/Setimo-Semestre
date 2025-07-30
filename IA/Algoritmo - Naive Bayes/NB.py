import matplotlib.pyplot as plt

dados = [
    ['Chuvoso', 'Quente', 'Alta', 'Fraco', 'Nao'],
    ['Chuvoso', 'Quente', 'Alta', 'Forte', 'Nao'],
    ['Nublado', 'Quente', 'Alta', 'Fraco', 'Sim'],
    ['Ensolarado', 'Ameno', 'Alta', 'Fraco', 'Sim'],
    ['Ensolarado', 'Frio', 'Normal', 'Fraco', 'Sim'],
    ['Ensolarado', 'Frio', 'Normal', 'Forte', 'Nao'],
    ['Nublado', 'Frio', 'Normal', 'Forte', 'Sim'],
    ['Chuvoso', 'Ameno', 'Alta', 'Fraco', 'Nao'],
    ['Chuvoso', 'Frio', 'Normal', 'Fraco', 'Sim'], 
    ['Ensolarado', 'Ameno', 'Normal', 'Fraco', 'Sim'],
    ['Chuvoso', 'Ameno', 'Normal', 'Forte', 'Sim'],
    ['Nublado', 'Ameno', 'Alta', 'Forte', 'Sim'],
    ['Nublado', 'Quente', 'Normal', 'Fraco', 'Sim'],
    ['Ensolarado', 'Ameno', 'Alta', 'Forte', 'Nao']
]

atributos = ['Tempo', 'Temperatura', 'Umidade', 'Vento']

class Histograma:
    def __init__(self):
        # Probabilidades de sim ou não
        self.p_sim = 0.0
        self.p_nao = 0.0
        
        # Totais de sim ou não
        self.total_sim = 0
        self.total_nao = 0
        
        # Frequências de cada atributo
        self.freq_sim = {}
        self.freq_nao = {}

    def print_Histograma(self):
        print("=== HISTOGRAMA DO MODELO ===")
        print(f"P(Sim): {self.p_sim}")
        print(f"P(Nao): {self.p_nao}")
        print(f"Total Sim: {self.total_sim}")
        print(f"Total Nao: {self.total_nao}")
        print("\nFrequências por atributo (Sim):")
        for atributo, valores in self.freq_sim.items():
            print(f"{atributo}: {valores}")
        print("\nFrequências por atributo (Nao):")
        for atributo, valores in self.freq_nao.items():
            print(f"{atributo}: {valores}")

    def plot_Histograma(self):
        # Para cada atributo, plota a frequência dos valores para Sim e Nao
        for atributo in self.freq_sim:
            # Junta todos os valores possíveis dos dois dicionários
            valores = set(self.freq_sim[atributo].keys()).union(self.freq_nao[atributo].keys())
            valores = sorted(valores)  # ordena os valores para consistência

            # Frequências em ordem dos valores
            freq_sim = [self.freq_sim[atributo].get(v, 0) for v in valores]
            freq_nao = [self.freq_nao[atributo].get(v, 0) for v in valores]

            # Posição das barras no eixo x
            x = range(len(valores))

            # Cria o gráfico de barras
            plt.figure(figsize=(6, 4))
            plt.bar(x, freq_sim, width=0.4, label='Sim', align='center', color='green')
            plt.bar([i + 0.4 for i in x], freq_nao, width=0.4, label='Não', align='center', color='red')

            plt.xticks([i + 0.2 for i in x], valores)
            plt.title(f'Frequências do atributo: {atributo}')
            plt.xlabel(atributo)
            plt.ylabel('Frequência')
            plt.legend()
            plt.tight_layout()
            plt.grid(axis='y', linestyle='--', alpha=0.5)
            plt.show()

def gerar_Histograma(dados):

    hist = Histograma()
    total = len(dados)

    # Conta os totais de sim ou não
    hist.total_sim = sum(1 for d in dados if d[-1] == 'Sim')
    hist.total_nao = total - hist.total_sim

    # Probabilidades de sim ou não
    hist.p_sim = hist.total_sim / total
    hist.p_nao = hist.total_nao / total

    for i, atributo in enumerate(atributos):
        hist.freq_sim[atributo] = {}
        hist.freq_nao[atributo] = {}

        for d in dados:
            valor = d[i]
            classe = d[-1]
            if classe == 'Sim':
                hist.freq_sim[atributo][valor] = hist.freq_sim[atributo].get(valor, 0) + 1
            else:
                hist.freq_nao[atributo][valor] = hist.freq_nao[atributo].get(valor, 0) + 1
    return hist

def jogar(teste, hist: Histograma):
    prob_sim = hist.p_sim
    prob_nao = hist.p_nao

    for i, atributo in enumerate(atributos):
        valor = teste[i]

        # Faz a probabilidade e soma um para resolver o problema do zero
        prob_sim *= (hist.freq_sim[atributo].get(valor, 0) + 1) / (hist.total_sim + len(hist.freq_sim[atributo]))
        prob_nao *= (hist.freq_nao[atributo].get(valor, 0) + 1) / (hist.total_nao + len(hist.freq_nao[atributo]))

    # Normaliza
    total_prob = prob_sim + prob_nao
    prob_sim_norm = prob_sim / total_prob
    prob_nao_norm = prob_nao / total_prob

    return prob_sim_norm, prob_nao_norm


def main():

    teste = ['Ensolarado', 'Frio', 'Alta', 'Fraco']

    modelo = gerar_Histograma(dados)

    modelo.print_Histograma()
    modelo.plot_Histograma()

    prob_sim, prob_nao = jogar(teste, modelo)

    # Exibe o resultado
    print(f'\nProbabilidade de Jogar: {prob_sim:.4f}')
    print(f'Probabilidade de Não Jogar: {prob_nao:.4f}')


if __name__ == "__main__":
    main()
