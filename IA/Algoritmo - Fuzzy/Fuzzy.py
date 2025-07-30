import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#pip install networkx
# #! pip install scikit-fuzzy

# Cria os antecedentes com o universo de discurso.
comida = ctrl.Antecedent(np.linspace(0, 1, 51), 'comida')
servico = ctrl.Antecedent(np.linspace(0, 1, 51), 'servico')
gorjeta = ctrl.Consequent(np.linspace(0, 20, 51), 'gorjeta')

######### FUNÇÕES DE PERTINÊNCIA #########
# comida
comida['ruim'] = fuzz.trimf(comida.universe, [0.0, 0.0, 0.5])       #Maior grau de pertinencia em 0
comida['boa'] = fuzz.trimf(comida.universe, [0.0, 0.5, 1.0])        # "" em 0.5
comida['saborosa'] = fuzz.trimf(comida.universe, [0.5, 1.0, 1.0])   # "" em 1

# serviço
servico['ruim'] = fuzz.trimf(servico.universe, [0.0, 0.0, 0.5])
servico['aceitavel'] = fuzz.trimf(servico.universe, [0.0, 0.5, 1.0])
servico['otima'] = fuzz.trimf(servico.universe, [0.5, 1.0, 1.0])


# gorjeta
gorjeta['baixa'] = fuzz.trimf(gorjeta.universe, [0, 0, 10]) 
gorjeta['media'] = fuzz.trimf(gorjeta.universe, [5, 10, 15])
gorjeta['alta'] = fuzz.trimf(gorjeta.universe, [10, 20, 20])


######### REGRAS #########
rule1 = ctrl.Rule(comida['ruim'] & servico['ruim'], gorjeta['baixa'])
rule2 = ctrl.Rule(comida['ruim'] & servico['aceitavel'], gorjeta['baixa'])
rule3 = ctrl.Rule(comida['ruim'] & servico['otima'], gorjeta['media'])

rule4 = ctrl.Rule(comida['boa'] & servico['ruim'], gorjeta['baixa'])
rule5 = ctrl.Rule(comida['boa'] & servico['aceitavel'], gorjeta['media'])
rule6 = ctrl.Rule(comida['boa'] & servico['otima'], gorjeta['alta'])

rule7 = ctrl.Rule(comida['saborosa'] & servico['ruim'], gorjeta['baixa'])
rule8 = ctrl.Rule(comida['saborosa'] & servico['aceitavel'], gorjeta['alta'])
rule9 = ctrl.Rule(comida['saborosa'] & servico['otima'], gorjeta['alta'])

#define o sistema de controle
gorjeta_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9 ])
gorjeta_simulation = ctrl.ControlSystemSimulation(gorjeta_ctrl)


# Input values
#gorjeta_simulation.input['comida'] = 1.0  # Example 
#gorjeta_simulation.input['servico'] = 1.0   # Example

#Realiza a simulação
#gorjeta_simulation.compute()

#print(gorjeta_simulation.output['gorjeta'])

gorjeta.view(sim = gorjeta_simulation)

# Cria a malha com valores de comida e serviço de 0 a 1
x_comida = np.linspace(0, 1, 51)
y_servico = np.linspace(0, 1, 51)
x, y = np.meshgrid(x_comida, y_servico)

# Cria um array vazio para armazenar os resultados de gorjeta
z = np.zeros_like(x)

# Para cada par (comida, servico), calcula a gorjeta com o sistema fuzzy
valor_maximo = 0
valor_minimo = 20

for i in range(51):
    for j in range(51):
        gorjeta_simulation.input['comida'] = x[i, j]
        gorjeta_simulation.input['servico'] = y[i, j]
        gorjeta_simulation.compute()
        z[i, j] = gorjeta_simulation.output['gorjeta']
        if(z[i,j] > valor_maximo):
            valor_maximo = z[i,j]
        if(z[i,j] < valor_minimo):
            valor_minimo = z[i,j]

print("valor maximo =", valor_maximo, ", valor minimo = ", valor_minimo)
# Cria a figura 3D
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Plota a superfície
surf = ax.plot_surface(x, y, z, cmap='viridis')

# Labels e título
ax.set_xlabel('Comida')
ax.set_ylabel('Serviço')
ax.set_zlabel('Gorjeta (%)')
ax.set_title('Superfície fuzzy: comida vs serviço vs gorjeta')

# Barra de cores
fig.colorbar(surf, shrink=0.5, aspect=5)

# Mostra o gráfico
plt.show()