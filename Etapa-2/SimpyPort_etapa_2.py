import itertools # count automático
import random
import simpy
import numpy
import matplotlib.pyplot as plt
from scipy.stats import t

# parametros da simulacao
RANDOM_SEED = 42 # semente do gerador de numeros aleatorios
SIM_TIME = 8760 # tempo de simulacao
NUM_REPLICACOES = 10 # numero de replicacoes

# parâmetros de entrada do modelo
INTERVALO_CHEGADA = 24.0 # intervalo (h) médio entre chegadas sucessivas de navios
TEMPO_OPERACAO_MODA = 20.0 # moda da taxa de operacao no berco (tph)
TEMPO_OPERACAO_MAX = 12.0 # maior valor da taxa de operacao no berco (tph)
TEMPO_OPERACAO_MIN = 5.0 # maior valor da taxa de operacao no berco (tph)
TEMPO_ATRACACAO_MIN = 0.8
TEMPO_ATRACACAO_MEDIO = 1.0
TEMPO_ATRACACAO_MAX = 2.0
TEMPO_DESCARREGAMENTO_MEDIO = 12.0
TEMPO_DESATRACACAO_MIN = 0.9
TEMPO_DESATRACACAO_MEDIO = 1.2
TEMPO_DESATRACACAO_MAX = 3.0
TEMPO_QUEBRA_GUINDASTE = 10.0
TEMPO_MEDIO_CONCERTO = 1.0

CARGA_NAVIO = 100 # carga (t) do navio
 

# variáveis globais
naviosFila = 0.0 # numero de navios em fila
tempoBercoOcupado = 0.0 # tempo total de ocupacao do berco
numNaviosAtendidos = 0 # numero total de navios atendidos
cargaEntregue = 0.0 # carga (t) total entregue
tempoFila = []
tempoQuebraGuindaste = []
broken = False
debug = True

def amplitudeConfianca(n, desvio):
    if n < 2:
        return 0.0
    else:
        return t.ppf(0.975,n-1)*desvio/numpy.sqrt(n)

def monitor(env, logFila, freq=1):
    global naviosFila
    while True:
        # collect statistics 
        logFila.append(naviosFila)
        yield env.timeout(freq)
        
def navio(nome, env, berco, guindaste):
    """Um navio chega ao porto para carregamento.
    Ele solicita um berço de atracação.
    """
    global tempoBercoOcupado
    global numNaviosAtendidos
    global naviosFila
    global cargaEntregue
    global debug
    global broken
    global tempoFila
    
    
    if debug:
        print('%s chega ao porto em %.1f' % (nome, env.now))
    naviosFila += 1
    with berco.request() as req: 
        start_berco = env.now
        # Request um dos bercos
        yield req
        tempoFila.append(env.now - start_berco)
        naviosFila -= 1
        start = env.now   
        if debug:
            print('%s atraca em %.1f horas.' % (nome, env.now))
        # Tempo atracacao
        yield env.timeout(random.triangular(TEMPO_ATRACACAO_MIN, TEMPO_ATRACACAO_MEDIO, TEMPO_ATRACACAO_MAX))
        
        # Tempo de descarregamento
        tempo_descarregamento = random.expovariate(1/TEMPO_DESCARREGAMENTO_MEDIO)
        with guindaste.request(priority = 2) as req:
            yield req
            
            while tempo_descarregamento:
                try:
                    if debug:
                        print('%s inicia carregamento em %.1f horas.' % (nome, env.now))  

                    start = env.now
                    yield env.timeout(tempo_descarregamento)

                    if debug:
                        print('%s termina carregamento em %.1f horas.' % (nome, env.now))  

                    tempo_descarregamento = 0
                except simpy.Interrupt:
                    if debug:
                        print('%s sofre quebra de guindaste em %.1f horas.' % (nome, env.now))  

                    tempo_descarregamento -= env.now - start
                   
                    
                    if debug:
                        print('%s guindaste operante em %.1f horas.' % (nome, env.now))  


        # Tempo de desatracacao
        yield env.timeout(random.triangular(TEMPO_DESATRACACAO_MIN, TEMPO_DESATRACACAO_MEDIO, TEMPO_DESATRACACAO_MAX))
        
        if debug:
            print('%s deixa o porto em %.1f horas.' % (nome, env.now))  

        if debug:
            print('%s tempo de carregamento: %.1f horas.' % (nome, env.now - start))
        tempoBercoOcupado=tempoBercoOcupado+env.now-start
        numNaviosAtendidos += 1
        cargaEntregue += CARGA_NAVIO


def gera_navio(env, berco, logFila,guindaste):
    """Gera um novo navio para o berco"""
    for i in itertools.count():
        yield env.timeout(random.expovariate(1/INTERVALO_CHEGADA))
        env.process(navio('Navio %d' % i, env, berco, guindaste))
        
def quebraGuindaste(env,guindaste):
    global broken
    global tempoQuebraGuindaste
    while True:
        yield env.timeout(random.expovariate(1.0/TEMPO_QUEBRA_GUINDASTE))
        if not broken:
            with guindaste.request(priority=1) as req:
                yield req
                if debug:
                    print('Guindaste QUEBROU em %.1f horas.' % (env.now))
                    t1 = env.now
                broken=True
                yield env.timeout(random.expovariate(1.0/TEMPO_MEDIO_CONCERTO))
                if debug:
                    print('Guindaste LIBERADO em %.1f horas.' % (env.now))
                    t2 = env.now
                t = t2 - t1
                tempoQuebraGuindaste.append(t)
                
                broken=False

        
        
# Setup and start the simulation
print('Simulação do Porto')

#random.seed(RANDOM_SEED)
logFila = []

# Create environment and start processes
env = simpy.Environment()
berco = simpy.Resource(env, 1)
guindaste = simpy.PreemptiveResource(env, capacity=1)
env.process(gera_navio(env, berco, logFila,guindaste))
env.process(monitor(env,logFila))
env.process(quebraGuindaste(env,guindaste))

# Execute!
ocupacaoList = []
listcargaEntregue = []
listTempoMedioFila = []
tempoInicial = 0.0


for i in range(NUM_REPLICACOES):
    env.run(until=SIM_TIME + tempoInicial)
    print('Replicacao %i Ocupação berço: %.2f' % (i+1, tempoBercoOcupado/(SIM_TIME)))
    ocupacaoList.append(tempoBercoOcupado/SIM_TIME)
    print("Total de carga entregue: ", cargaEntregue)
    listcargaEntregue.append(cargaEntregue)

    if debug:
        print('Replicacao %i Número de navios atendidos %i' % (i + 1,numNaviosAtendidos))
    tempoInicial += SIM_TIME
    tempoBercoOcupado = 0
    numNaviosAtendidos = 0
    cargaEntregue = 0
plt.plot(logFila)
plt.show    
    
print('Média de ocupacao das replicações: %.2f IC: %.2f' % (numpy.mean(ocupacaoList), amplitudeConfianca(NUM_REPLICACOES, numpy.std(ocupacaoList))))
print('Tempo médio de espera em fila: %.2f horas' % numpy.mean(tempoFila))
print("Media total de cargas entregues: %.f IC: %.f" % (numpy.mean(listcargaEntregue), amplitudeConfianca(NUM_REPLICACOES, numpy.std(ocupacaoList))))
print('Tempo média quebra guindaste %.2f' %(numpy.mean(tempoQuebraGuindaste)))
