import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
import random
import matplotlib.pyplot as plt

# Carregar e preparar dados
iris = pd.read_csv("https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data", header=None)
iris.columns = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'class']
X = iris.iloc[:, :-1].values
y = LabelEncoder().fit_transform(iris['class'])

# Normalizar os dados
scaler = StandardScaler()
X = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

class Individuo:
    def __init__(self, pesos=None):
        # Agora com pesos para cada classe (4 features × 3 classes)
        if pesos is None:
            self.pesos = np.random.uniform(-1, 1, (4, 3))
        else:
            self.pesos = pesos
        self.valor_fitness = 0

    def avaliar(self, X, y):
        acertos = 0
        for xi, yi in zip(X, y):
            # Calcula scores para cada classe
            scores = np.dot(xi, self.pesos)
            pred = np.argmax(scores)  # Classe com maior score
            if pred == yi:
                acertos += 1
        self.valor_fitness = acertos / len(y)
        return self.valor_fitness

    def fitness(self):
        return self.valor_fitness

    def mutar(self, mutationRate):
        novos_pesos = self.pesos.copy()
        for i in range(novos_pesos.shape[0]):
            for j in range(novos_pesos.shape[1]):
                if random.random() < mutationRate:
                    novos_pesos[i,j] += random.uniform(-0.5, 0.5)
        return Individuo(novos_pesos)

    def clone(self):
        return Individuo(self.pesos.copy())

def inicialização(sizePopulation):
    return [Individuo() for _ in range(sizePopulation)]

def avaliarAptidao(population, X, y):
    for individuo in population:
        individuo.avaliar(X, y)
    return population

def selecao(population, sizeSelecao):
    melhores = sorted(population, key=lambda ind: ind.valor_fitness, reverse=True)
    return melhores[:sizeSelecao]

def clonagem(melhores, clonagem_total):
    clones = []
    soma_fitness = sum(ind.valor_fitness for ind in melhores)
    
    if soma_fitness == 0:
        clones_por_ind = [clonagem_total // len(melhores)] * len(melhores)
        clones_por_ind[0] += clonagem_total % len(melhores)
    else:
        clones_por_ind = [round((ind.valor_fitness / soma_fitness) * clonagem_total) for ind in melhores]
        diferenca = clonagem_total - sum(clones_por_ind)
        clones_por_ind[0] += diferenca
    
    for i, num_clones in enumerate(clones_por_ind):
        clones.extend([melhores[i].clone() for _ in range(num_clones)])
    return clones

def hipermutacao(clones, fator, X, y):
    hipermutados = []
    for clone in clones:
        max_fitness = max(c.valor_fitness for c in clones) if clones else 1
        taxaHip = (1 - (clone.valor_fitness / max_fitness)) * fator
        hipermutados.append(clone.mutar(taxaHip))
    return hipermutados

def main():
    sizePopulation = 30
    sizeSelecao = 5
    sizeNovosIndividuos = 5
    generations = 100
    beta = 0.5  # fator clonal
    
    population = inicialização(sizePopulation)
    population = avaliarAptidao(population, X_train, y_train)
    
    historico_fitness = []
    melhor_individuo = None
    melhor_fitness = 0

    for i in range(generations):
        population = avaliarAptidao(population, X_train, y_train)
        melhores = selecao(population, sizeSelecao)
        clones = clonagem(melhores, sizePopulation - sizeNovosIndividuos)
        avaliarAptidao(clones, X_train, y_train)
        hipermutados = hipermutacao(clones, beta, X_train, y_train)
        novosIndividuos = inicialização(sizeNovosIndividuos)
        novosIndividuos = avaliarAptidao(novosIndividuos, X_train, y_train)
        
        population = hipermutados + novosIndividuos
        population = avaliarAptidao(population, X_train, y_train)
        
        melhor_atual = max(population, key=lambda ind: ind.valor_fitness)
        if melhor_atual.valor_fitness > melhor_fitness:
            melhor_fitness = melhor_atual.valor_fitness
            melhor_individuo = melhor_atual
        
        historico_fitness.append(melhor_fitness)
        print(f"Geração {i}: Melhor fitness = {melhor_fitness:.4f}")

    # Avaliação final
    acuracia_teste = melhor_individuo.avaliar(X_test, y_test)
    print("\nResultados Finais:")
    print(f"Acurácia no treino: {melhor_fitness:.4f}")
    print(f"Acurácia no teste: {acuracia_teste:.4f}")
    
    # Plot do histórico de fitness
    plt.plot(historico_fitness)
    plt.title('Evolução do Melhor Fitness')
    plt.xlabel('Geração')
    plt.ylabel('Acurácia')
    plt.show()

if __name__ == "__main__":
    main()