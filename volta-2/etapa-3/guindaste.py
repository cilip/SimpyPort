"""

    Guindastes estao organizados em uma lista Store, conforme sao "pegos" e usados nos navios, saem da lista. Quando terminam de ser usados,
voltam para a lista e ficam disponiveis para a proxima embarcacao.
    


"""
import simpy

env = simpy.Environment()

numGuindastes = 3

guindastesStore = simpy.FilterStore(env, capacity=numGuindastes)
guindastesStore.items = [Guindaste(env, number=i) for i in range(numGuidnastes)]

class Guindaste(object):
    def __init__(self, env, number):
        self.number = number
        self.resource =  simpy.Resource(env, 1)
        self.req = self.resource.request()
        self.broken = False
 
       
    def quebraGuindaste(env, self, guindastes_navio):
        global tempoQuebraGuindaste
        while True:
            yield env.timeout(random.expovariate(1.0/TEMPO_QUEBRA_GUINDASTE))
            if not self.broken:
                with guindaste.request(priority=1) as req:
                    yield req
                    if debug:
                        print('Guindaste QUEBROU em %.1f horas.' % (env.now))
                    t1 = env.now
                    self.broken=True
                    guindastes_navio -= 1
                    yield env.timeout(random.expovariate(1.0/TEMPO_MEDIO_CONCERTO))
                    if debug:
                        print('Guindaste ' self.number' LIBERADO em %.1f horas.' % (env.now))
                    t2 = env.now
                    t = t2 - t1
                    tempoQuebraGuindaste += t
                    
                    self.broken = False
                    

    def getNumber(self):
        return self.number
    
    def getRequest(self):
        return self.req    
    
    def ocupa(self, env, name_navio):
        self.start = env.now
        self.navioAtual = name_navio
        return self.req(priority = 2)
        
    def monitor(self, guindastes_navio):
        if self.broken == True:
            self.navioAtual = None
            guindastes_navio -= 1
            
            yield(5)
            

        
 

#funcao que calcula quantos guindastes estao discponiveis naquele momento para a embarcacao em 
#se o numero de guindastes possiveis para o tipo de embarcacao for menor do que o numero de guindastes disponiveis, o return sera do num de guindastes possiveis (menor valor)
def guindastes_disponiveis(env, guindastesStore, classe_navio):
    if classe_navio == 1: #Panamax
        num_maximo_guindastes = 2
    if classe_navio == 3: #Capesize
        num_maximo_guindastes = 3
    num_guindastes_disponiveis = len(guindastesStore.items)
    
    if num_max_guindastes < num_guindastes_disponiveis:
        num_guindastes_disponiveis = num_max_guindastes 
        
    if debug:
        print("numero ", num_guindastes_disponiveis)
    return num_guindastes_disponiveis 
    
   

#processo no qual a velocidade eh calculada e a carga eh transferida ate que o numero de guindastes relacionados a embarcacao em questao mude
#provavelmente sera um process
def descarregamento(env, navio, num_guindastes, velocidade):
    #monitor atualiza numero de guindastes em cada navio (num)
    while num == num_guindastes:
        start = env.now
        tempo = num_guindastes*(self.carga/velocidade)
    pause = env.now
    carga_transferida = velocidade*(pause-start)


#verifificar situacao do guindaste (quebras e transferencia para outra embarcacao)
#atualizar carga existente na embarcacao e no armazem
def monitor(env, guindaste):    
    while True:
        if 
            #verifica em que navio se encontra este guindaste e muda a velocidade de transferencia de carga
            
        #verifica guindastes quebrados e atualiza velocidade de descarregamento
        
        
        if #numero de guindastes muda, repete o processo de descarregamento daquele navio
            descarregamento(env, navio, num_guindastes, velocidade)
        yield env.timeout(5)
        
    return 
        
#funcao com o objetivo de promover quebras nos guindastes
#funcao em processo durante todo o tempo de simulacao
#havera 3 'broken's, um para cada guindaste


#realocar guindastes que quebraram e foram concertados ou que terminaram descarregamento
def realocar_guindaste(env, navio, guindaste):
    
    