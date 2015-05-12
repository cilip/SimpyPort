
#Parametros da simulacao
RANDOM_SEED = 42 # semente do gerador de numeros aleatorios
SIM_TIME = 100 # tempo de simulacao
NUM_REPLICACOES = 1 # numero de replicacoes
debug = True

#Parametros de entrada
TEMPO_CHEGADA_NAVIO = 24.0 #um navio chega a cada 24 horas, em media
classesNavio = [0, 1, 2, 3, 4, 5] #['Handymax','Panamax', 'Babe Cape', 'Capesize', 'VLOC', 'Valemax']
distClasses = [0.0, 0.6, 0.0, 0.4, 0.0, 0.0]
cargaClasses = [(60000, 70000, 80000), (80000, 100000, 120000),(120000, 170000, 180000), (200000, 221000, 250000),(250000, 280000, 300000), (370000, 390000, 400000)] # faixas de Carga de cada classe
cargaTotal = 0 #carga total entregue no ano
BercosPrioridades = [[1,1], [1,1], [0,1], [0,1], [0,1], [0,1]]


ListaBercosClasses = []
