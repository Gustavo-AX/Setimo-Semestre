import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Função
def funcao(x):
    return 10 * 2 + (x[0]**2 - 10 * np.cos(2 * np.pi * x[0])) + (x[1]**2 - 10 * np.cos(2 * np.pi * x[1]))

# Particula
class Particula:
    def __init__(self, lim_inf, lim_sup):
        # Começa com uma posição aleatória -> vetor de 2 posições
        self.posicao = np.random.uniform(lim_inf, lim_sup, 2)
        # Velocidade nula -> vetor de 2 posições nula
        #self.velocidade = np.zeros(2)
        self.velocidade = np.array([1.0, 1.0])  # ✅ ainda é um np.array
        # A melhor posição começa com a posição inicial
        self.pbest = self.posicao.copy()
        # Assim como para os fitness
        self.fitness_atual = funcao(self.posicao)
        self.fitness_pbest = self.fitness_atual

    def atualizar_fitness(self):
        self.fitness_atual = funcao(self.posicao)
        # Se for melhor que o melhor, atualiza o fitness
        if self.fitness_atual < self.fitness_pbest:
            self.pbest = self.posicao.copy()
            self.fitness_pbest = self.fitness_atual

    def mover(self, gbest, w, c1, c2):
        # Vetor de numeros randomicos entre 0 e 1
        r1 = np.random.rand(len(self.posicao))
        r2 = np.random.rand(len(self.posicao))

        # Atualiza a velocidade
        self.velocidade = (
            w * self.velocidade +
            c1 * r1 * (self.pbest - self.posicao) +
            c2 * r2 * (gbest - self.posicao)
        )

        # Atualiza a posição
        self.posicao += self.velocidade




def main():

    # iterações
    # Parâmetros
    # n = 2
    # A = 10

    numero_particulas = 30
    limite = 5.12
    iteracoes = 100
    w = 0.7
    c1 = 1
    c2 = 1

    # inicializa partículas
    populacao = [Particula(-limite, limite) for _ in range(numero_particulas)]

    # Melhor global:
    gbest = min(populacao, key=lambda p: p.fitness_pbest)
    gbest_pos = gbest.pbest.copy()
    gbest_val = gbest.fitness_pbest

    for i in range(iteracoes):

        # Atualiza os valores de todas partículas
        for particula in populacao:

            particula.atualizar_fitness()
            
            # Se for melhor que o global
            if particula.fitness_pbest < gbest_val:
                gbest_pos = particula.pbest.copy()
                gbest_val = particula.fitness_pbest

        # Detalhe, tem que ser dois fors para que não mude o sentido das outras no meio de uma iteração.
        for particula in populacao:
            particula.mover(gbest_pos, w, c1, c2)

        # Atualiza a posição dos pontos no gráfico
        posicoes = np.array([p.posicao for p in populacao])
        plt.clf()
        plt.xlim(-limite, limite)
        plt.ylim(-limite, limite)
        x_vals = [p[0] for p in posicoes]
        y_vals = [p[1] for p in posicoes]
        plt.scatter(x_vals, y_vals, color='blue', label='Particula')
        plt.scatter(gbest_pos[0], gbest_pos[1], color='red', label='Melhor')
        plt.title(f"Iteração{i}")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.legend()
        plt.pause(0.1)

if __name__ == "__main__":
    main()
