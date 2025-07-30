"""
1. Inicialização: criar uma população inicial de anticorpos (P).
2. Avaliação de aptidão: determinar a aptidão de cada elemento de P.
3. Seleção e expansão clonal: selecionar os n1 elementos de maior aptidão de P e gerar clones
desses anticorpos proporcionalmente à sua aptidão: quanto maior a aptidão, maior o número de
cópias, e vice-versa.
4. Maturação por afinidade: mutar todas essas cópias com uma taxa que é inversamente
proporcional à sua aptidão: quanto maior a aptidão, menor a taxa de mutação, e vice-versa.
Adicionar esses indivíduos mutados à população P.
5. Metadinâmica: substituir um número n2 de indivíduos de baixa aptidão por novos indivíduos
(gerados aleatoriamente).
6. Ciclo: repetir os Passos 2 a 5 até que um certo critério de parada seja atingido.
"""

import random
import math
import matplotlib.pyplot as plt

class Individuo:
    def __init__(self, x1=None, x2=None):
        self.x1 = x1 if x1 is not None else random.uniform(0, 10)
        self.x2 = x2 if x2 is not None else random.uniform(0, 10)
        self.valor_fitness = self.fitness()

    def fitness(self):
        return math.sqrt(self.x1) * math.sin(self.x1) * math.sqrt(self.x2) * math.sin(self.x2)

    def mutar(self, mutationRate):
        x1 = self.x1
        x2 = self.x2
        if random.random() < mutationRate:
            x1 = random.uniform(0, 10)
        if random.random() < mutationRate:
            x2 = random.uniform(0, 10)
        self.valor_fitness = self.fitness()
        return Individuo(x1, x2)

    def clone(self):
        self.valor_fitness = self.fitness()
        return Individuo(self.x1, self.x2)

def inicialização(sizePopulation):
    return [Individuo() for _ in range(sizePopulation)]

def avaliarAptidao(population):
    for individuo in population:
        individuo.valor_fitness = individuo.fitness()
    return population

def selecao(population, sizeSelecao):
    """bests_ones = []
    melhores = sorted(population, key=lambda ind: ind.valor_fitness, reverse=True)
    bests_ones.append(melhores[0])
    for i in range(len(melhores)):
        if(i>0):
            if (melhores[i].valor_fitness != melhores[i-1].valor_fitness):
                bests_ones.append(melhores[i])
    if(len(bests_ones) < sizeSelecao):
        for i in range((sizeSelecao - len(bests_ones))):
            bests_ones.append(melhores[i])
    
    bests_ones = sorted(bests_ones, key=lambda ind: ind.valor_fitness, reverse=True)
    #for i in bests_ones:
    #    print(f"bests_one = {i.valor_fitness}")
    return bests_ones[:sizeSelecao]"""

    melhores = sorted(population, key=lambda ind: ind.valor_fitness, reverse=True)
    return melhores[:sizeSelecao]


#Realiza a clonagem (diretamente proporcional a afinidade)
#clonagem: quantidade total de indivíduos que serão clonados.
#melhores: melhores indivíduos
def clonagem(melhores, clonagem):
    #Gera clones proporcionalmente ao fitness de cada indivíduo
    clones = []
    
    # Calcula fitness total para normalização
    soma_fitness = 0
    for i in melhores:
        soma_fitness += i.valor_fitness
    
    clonagens = [round((c/soma_fitness)*clonagem) for c in [i.valor_fitness for i in melhores]]
    cont = 0

    #NOTA: Devido a arredondamentos, a quantidade total de clones pode ser diferente
    #do total que queremos, nesse caso, adicionarei a diferença ao de melhor fitness
    totalClones = 0
    for i in clonagens:
        totalClones += i
    
    if(clonagem<totalClones):
        clonagens[0] -= totalClones - clonagem
    elif (clonagem>totalClones):
        clonagens[0] += clonagem - totalClones
    
    #print("Quantidade de clones para indivíduo", clonagens)
        
    while cont < len(clonagens):
        #realiza a clonagem
        for i in range(clonagens[cont]):
            clones.append(melhores[cont].clone())
        cont += 1
    return clones
    

#clones: contém os clones dos melhores anticorpos
#fator: fator de clonagem
def hipermutacao(clones,fator):
    #retorna um vetor de hipermutados.
    hipermutados = []

    for i in clones: #para cada anticorpo
        #Calcula a taxa de mutação
        #Quanto maior a afinidade, menor a taxa de mutação
        max_fitness = max(clone.valor_fitness for clone in clones)
        taxaHip = (1 - (i.valor_fitness / max_fitness)) * fator
        #taxaHip = max(((1 - (i.valor_fitness / max_fitness)) * fator) , 0.1)
        #Muta os indivíduos
        rand = random.random() 

        hipermutado = i.mutar(taxaHip)
            
        hipermutados.append(hipermutado)

    return hipermutados 

def main():
    sizePopulation = 30
    sizeSelecao = 5
    sizeNovosIndividuos = 5
    generations = 100
    numClones = 25
    beta = 0.5 #fator clonal
    #inicial, não precisa chamar os fitness.
    population = inicialização(sizePopulation)
    """for i in population:
            print(i.x1, i.x2, i.valor_fitness)"""
    #par printar:
    primeiros = []
    plt.ion()  # Modo interativo

    for i in range(generations):
        #print(f"Geração {i}")
        melhor_individuo = None
        melhor_fitness = -100
        """print("Melhores Escolhidos")
        for i in melhores:
                    print(i.x1, i.x2, i.valor_fitness)"""
        population = avaliarAptidao(population)
        melhores = selecao(population, sizeSelecao)
        """print("Melhores Escolhidos:")
        for j in melhores:
            print(j.x1, j.x2, j.valor_fitness)"""
        clones = clonagem(melhores, sizePopulation - sizeNovosIndividuos)

        """print("clones:")
        for i in clones:
            print(i.x1, i.x2, i.valor_fitness)"""
        hipermutados = hipermutacao(clones, beta)
        """print("Hipermutados:")
        for i in hipermutados:
            print(i.x1, i.x2, i.valor_fitness)"""
        novosIndividuos = inicialização(sizeNovosIndividuos)
        """print("Novos indivíduos:")
        for i in novosIndividuos:
            print(i.x1, i.x2, i.valor_fitness)"""
        #hipermutados.extend(novosIndividuos)
        nova_populacao = hipermutados + novosIndividuos
            
        population = nova_populacao

        population = avaliarAptidao(population)

        melhor_atual = max(population, key=lambda ind: ind.valor_fitness)
        if melhor_atual.valor_fitness > melhor_fitness:
            melhor_fitness = melhor_atual.valor_fitness
            melhor_individuo = melhor_atual

        primeiros.append(melhor_individuo)

        plt.clf()
        plt.xlim(0, 10)
        plt.ylim(0, 10)
        x_vals = [ind.x1 for ind in population]
        y_vals = [ind.x2 for ind in population]
        plt.scatter(x_vals, y_vals, color='blue', label='População')
        plt.scatter(melhor_atual.x1, melhor_atual.x2, color='red', label='Melhor')
        plt.title(f"Geração {i}")
        plt.xlabel("x1")
        plt.ylabel("x2")
        plt.legend()
        plt.pause(0.1)

        print(f"Geração {i}: Melhor indivíoduo: x1 = {melhor_individuo.x1} x2 = {melhor_individuo.x2} fitness = {melhor_fitness:.4f}")
        
    print("\nMelhor indivíduo encontrado:")
    print(f"x1 = {melhor_individuo.x1:.4f}, x2 = {melhor_individuo.x2:.4f}, fitness = {melhor_fitness:.4f}")
    
    plt.ioff()
    #plt.plot([i.valor_fitness for i in primeiros])
    #plt.title('Afinidade (x/121)')
    plt.show()

if __name__ == "__main__":
    main()