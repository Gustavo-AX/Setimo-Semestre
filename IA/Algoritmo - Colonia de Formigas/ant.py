import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt

def ler_matriz_distancias(caminho_csv):
    df = pd.read_csv(caminho_csv, header=None)
    return df.values


# Inicializa a matriz de feromônio 
def inicializar_feromonio(n_cidades, feromonio_inicial):
    # Cria uma matriz preenchida com o valor inicial do feromônio
    return np.full((n_cidades, n_cidades), feromonio_inicial)


# Calcula a atratividade entre as cidades (quanto menor a distância, mais atrativa)
def calcular_atratividade(matriz_distancias):
    # Cria uma matriz de zeros com o mesmo formato da matriz de distâncias
    atratividade = np.zeros_like(matriz_distancias, dtype=float)

    for i in range(len(matriz_distancias)):
        for j in range(len(matriz_distancias)):

            if i != j and matriz_distancias[i][j] != 0:
                atratividade[i][j] = 1.0 / matriz_distancias[i][j]
            else:
                # Se for a mesma cidade ou distância zero, a atratividade é zero
                atratividade[i][j] = 0.0

    return atratividade


# Calcula as probabilidades de transição
def calcular_probabilidades_transicao(feromonio, atratividade, visitadas, alfa=1, beta=5):
    # Cria um vetor de probabilidades zerado
    probabilidades = np.zeros(len(feromonio))

    for j in range(len(feromonio)):

        if not visitadas[j]:
            # Fórmula da probabilidade com base no feromônio e atratividade
            probabilidades[j] = (feromonio[j] ** alfa) * (atratividade[j] ** beta)

    soma = np.sum(probabilidades)
    # Normaliza os valores para formar uma distribuição de probabilidade
    return probabilidades / soma if soma != 0 else probabilidades


# Escolhe aleatoriamente a próxima cidade com base nas probabilidades
def escolher_proxima_cidade(probabilidades):
    # Usa uma escolha aleatória ponderada pelas probabilidades
    return np.random.choice(len(probabilidades), p=probabilidades)

# Constrói um caminho completo para uma formiga
def construir_solucao(matriz_feromonio, atratividade, matriz_distancias):

    n = len(matriz_distancias)
    # Lista que armazena o caminho da formiga
    caminho = []
    # Vetor que marca as cidades já visitadas
    visitadas = [False] * n

    atual = random.randint(0, n - 1)

    caminho.append(atual)

    visitadas[atual] = True

    # Enquanto não visitar todas as cidades
    for _ in range(n - 1):

        probabilidades = calcular_probabilidades_transicao(
            matriz_feromonio[atual], atratividade[atual], visitadas
        )

        # Escolhe a próxima cidade com base nas probabilidades
        proxima = escolher_proxima_cidade(probabilidades)

        caminho.append(proxima)

        visitadas[proxima] = True

        atual = proxima

    caminho.append(caminho[0])

    return caminho


# Calcula o comprimento total do caminho (soma das distâncias)
def calcular_comprimento_caminho(caminho, matriz_distancias):
    return sum(matriz_distancias[caminho[i], caminho[i+1]] for i in range(len(caminho) - 1))


# Função que atualiza a matriz de feromônio com base nos caminhos percorridos
def atualizar_feromonios(matriz_feromonio, todos_os_caminhos, matriz_distancias, evaporacao, Q):

    matriz_feromonio *= (1 - evaporacao)

    # Para cada caminho construído pelas formigas
    for caminho in todos_os_caminhos:

        comprimento = calcular_comprimento_caminho(caminho, matriz_distancias)

        for i in range(len(caminho) - 1):
            a, b = caminho[i], caminho[i+1]
            # Calcula o quanto de feromônio será depositado
            deposito = Q / comprimento

            matriz_feromonio[a][b] += deposito
            matriz_feromonio[b][a] += deposito


# Algoritmo
def otimizacao_colonia_formigas(matriz_distancias, n_formigas=20, n_iteracoes=100, alfa=1, beta=5, evaporacao=0.5, Q=100):

    n = len(matriz_distancias)
    #Começa com 1
    matriz_feromonio = inicializar_feromonio(n, feromonio_inicial=1.0)
    # Atratividade
    atratividade = calcular_atratividade(matriz_distancias)

    melhor_caminho = None
    melhor_comprimento = float('inf')
    melhores_comprimentos = []

    for _ in range(n_iteracoes):

        todos_os_caminhos = []

        # Cada formiga constrói um caminho
        for _ in range(n_formigas):
            # Constrói o caminho
            caminho = construir_solucao(matriz_feromonio, atratividade, matriz_distancias)
            # Adiciona o caminho à lista
            todos_os_caminhos.append(caminho)

            # Calcula o comprimento do caminho
            comprimento = calcular_comprimento_caminho(caminho, matriz_distancias)

            # Verifica se este é o melhor caminho encontrado até agora
            if comprimento < melhor_comprimento:
                melhor_comprimento = comprimento
                melhor_caminho = caminho

        melhores_comprimentos.append(melhor_comprimento)

        # Atualiza os feromônios com base nos caminhos encontrados
        atualizar_feromonios(matriz_feromonio, todos_os_caminhos, matriz_distancias, evaporacao, Q)

    # Plot do gráfico de convergência
    plt.plot(melhores_comprimentos)
    plt.xlabel("Iteração")
    plt.ylabel("Melhor distância")
    plt.title("Convergência da Colônia de Formigas")
    plt.grid(True)
    plt.show()

    # Retorna o melhor caminho e seu comprimento
    return melhor_caminho, melhor_comprimento


def main():

    caminho_csv = "distancia_matrix.csv"

    matriz_distancias = ler_matriz_distancias(caminho_csv)

    melhor_caminho, melhor_comprimento = otimizacao_colonia_formigas(matriz_distancias)

    print("Melhor caminho encontrado:", melhor_caminho)
    print("Comprimento do caminho:", melhor_comprimento)


if __name__ == "__main__":
    main()
