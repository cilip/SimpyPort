"""

    Guindastes estao organizados em uma lista Store, conforme sao "pegos" e usados nos navios, saem da lista. Quando terminam de ser usados,
voltam para a lista e ficam disponiveis para a proxima embarcacao.
    


"""


import simpy

env = simpy.Environment()

guindaste1 = simpy.PreemptiveResource(env, capacity = 1)
guindaste2 = simpy.PreemptiveResource(env, capacity = 1)
guindaste3 = simpy.PreemptiveResource(env, capacity = 1)

#os guindastes existentes estao organizados em uma lista
guindastesStore = simpy.Store(env, capacity=3)
guindastesStore.items = [guindaste1, guindaste2, guindaste3]

num_guindastes = 0

#funcao que calcula quantos guindastes estao discponiveis naquele momento para a embarcacao em questao
def guindastes_disponiveis(env, guindastesStore):
    num_guindastes_disponiveis = len(guindastesStore.items)
    print("numero ", num_guindastes_disponiveis)
    return num_guindastes_disponiveis    
    
    
#pega todos os guindastes disponiveis no momento em questao
def pega_guindaste(env, navio, guindastesStore):
    num = guindastes_disponiveis(env, guindastesStore)
    for i in range(num):
        item = yield guindastesStore.get()
        with item.request(priority = 2) as req:
            yield req        
        i+=1
    return 
    

#processo no qual a velocidade eh calculada e a carga eh transferida ate que o numero de guindastes relacionados a embarcacao em questao mude
#provavelmente sera um process
def descarregamento(env, navio, num_guindastes):
    global velocidade
    while num = num_guindastes:
        start = env.now
        tempo = num_guindastes*(self.carga/velocidade)
    pause = env.now
    carga_transferida = 


#verifificar situacao do guindaste (quebras e transferencia para outra embarcacao)
def monitor(env, guindaste):
    
    while True:
        
        
        yield env.timeout(5)
        
        
#funcao com o objetivo de promover quebras nos guindastes
#funcao em processo durante todo o tempo de simulacao
#**ideia** criar variavel global para 
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
                tempoQuebraGuindaste += t
                
                broken=False
        
        
def navio(env, guindastesStore):
    for i in range(guindastes_disponiveis(env, guindastesStore)):
        guindaste = yield guindastesStore.get()
        num_guindastes +=1
        print("NUMERO GUINDASTES = %d" %num_guindastes)

for i in range(2):
    env.process(navio(env, guindastesStore))
env.run()