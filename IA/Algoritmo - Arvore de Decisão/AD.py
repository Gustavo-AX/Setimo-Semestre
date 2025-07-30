# Importa bibliotecas para manipulação de dados, machine learning e visualização
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt

# ===============================
# ETAPA 1 - Carregamento dos dados
# ===============================

# Lê o arquivo CSV com os dados dos pacientes
df = pd.read_csv("heart.csv")  # Substitua pelo nome correto do arquivo

# ===============================
# ETAPA 2 - Pré-processamento
# ===============================

# Lista com os nomes das colunas categóricas que precisam ser convertidas em números
categoricas = ['Sex', 'ChestPainType', 'RestingECG', 'ExerciseAngina', 'ST_Slope']

# Aplica o LabelEncoder para converter strings em números inteiros
df[categoricas] = df[categoricas].apply(LabelEncoder().fit_transform)

# ===============================
# ETAPA 3 - Separação de variáveis
# ===============================

# X = dados de entrada (todas as colunas, menos a de saída)
X = df.drop(columns=['HeartDisease'])

# y = variável de saída (classe: tem ou não doença cardíaca)
y = df['HeartDisease']

# ===============================
# ETAPA 4 - Função para avaliar modelos
# ===============================

# Essa função roda o modelo 30 vezes com diferentes divisões aleatórias dos dados
def avaliar_modelo(modelo, X, y, n_execucoes=30):
    acuracias = []  # Lista para armazenar a acurácia de cada execução

    for _ in range(n_execucoes):
        # Divide os dados em treino (80%) e teste (20%)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, stratify=y
        )

        # Treina o modelo com os dados de treino
        modelo.fit(X_train, y_train)

        # Realiza predições com os dados de teste
        y_pred = modelo.predict(X_test)

        # Calcula a acurácia e adiciona à lista
        acuracias.append(accuracy_score(y_test, y_pred))

    # Retorna a média e o desvio padrão das acurácias
    return np.mean(acuracias), np.std(acuracias)

# ===============================
# ETAPA 5 - Avaliação: Árvore de Decisão
# ===============================

# Cria o classificador de árvore de decisão com entropia
dt = DecisionTreeClassifier(criterion="entropy", random_state=0)

# Avalia o modelo 30 vezes
media_dt, std_dt = avaliar_modelo(dt, X, y)

# Mostra os resultados
print(f"Árvore de Decisão - Acurácia média: {media_dt:.2f}, Desvio padrão: {std_dt:.2f}")

# ===============================
# ETAPA 6 - Avaliação: Floresta Aleatória
# ===============================

# Cria o classificador de floresta aleatória com 100 árvores e entropia
rf = RandomForestClassifier(criterion="entropy", n_estimators=100, random_state=0)

# Avalia o modelo 30 vezes
media_rf, std_rf = avaliar_modelo(rf, X, y)

# Mostra os resultados
print(f"Floresta Aleatória - Acurácia média: {media_rf:.2f}, Desvio padrão: {std_rf:.2f}")

# ===============================
# ETAPA 7 - Análise da Profundidade na Random Forest
# ===============================

# Lista de profundidades máximas a testar (de 1 até o número de colunas de X)
max_depths = list(range(1, X.shape[1] + 1))

# Listas para armazenar os resultados
medias = []
stds = []

# Para cada profundidade, cria um modelo e avalia seu desempenho
for d in max_depths:
    # Cria modelo com profundidade limitada
    rf = RandomForestClassifier(criterion="entropy", n_estimators=100, max_depth=d, random_state=0)

    # Avalia o modelo com 30 execuções
    media, std = avaliar_modelo(rf, X, y)
    medias.append(media)
    stds.append(std)

# ===============================
# ETAPA 8 - Gráfico: Acurácia vs Profundidade
# ===============================

# Cria gráfico de linha com barra de erro (desvio padrão)
plt.figure(figsize=(10, 6))
plt.plot(max_depths, medias, marker='o')
plt.xlabel('Profundidade Máxima das Árvores')
plt.ylabel('Acurácia Média')
plt.title('Desempenho da Floresta Aleatória por Profundidade Máxima')
plt.grid(True)
plt.show()