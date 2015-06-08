"""

    Guindastes estao organizados em uma lista Store, conforme sao "pegos" e usados nos navios, saem da lista. Quando terminam de ser usados,
voltam para a lista e ficam disponiveis para a proxima embarcacao.
    


"""
import simpy
import parametros as P
import random

env = simpy.Environment()

numGuindastes = 3
TEMPO_QUEBRA_GUINDASTE = 10 #exmeplo de valor
tempoQuebraGuindaste = 0
TEMPO_MEDIO_CONSERTO = 1.0 #exemplo de valor

class Guindaste(object):
    def __init__(self, env, number):
        self.number = number
        self.resource =  simpy.Resource(env, 1)
        self.req = self.resource.request()
        self.broken = False
 
       
    def quebraGuindaste(env, self, guindastes_navio):
        #guindastes_navio e a variavel que conta quantos guindastes ha
        global tempoQuebraGuindaste
        while True:
            yield env.timeout(random.expovariate(1.0/TEMPO_QUEBRA_GUINDASTE))
            if not self.broken:
                with self.request(priority=1) as req:
                    yield req
                    if P.debug:
                        print('Guindaste QUEBROU em %.1f horas.' % (env.now))
                    t1 = env.now
                    self.broken=True
                    guindastes_navio -= 1
                    yield env.timeout(random.expovariate(1.0/TEMPO_MEDIO_CONSERTO))
                    guindastes_navio += 1
                    if P.debug:
                        print('Guindaste ', self.number,' LIBERADO em %.1f horas.' % (env.now))
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
    
   
            

        
 

#funcao que calcula quantos guindastes estao discponiveis naquele momento para a embarcacao em 
#se o numero de guindastes possiveis para o tipo de embarcacao for menor do que o numero de guindastes disponiveis, o return sera do num de guindastes possiveis (menor valor)
def guindastes_disponiveis(env, guindastesStore, classe_navio):
    if classe_navio == 1: #Panamax
        num_maximo_guindastes = 2
    if classe_navio == 3: #Capesize
        num_maximo_guindastes = 3
    num_guindastes_disponiveis = len(guindastesStore.items)
    
    if num_maximo_guindastes < num_guindastes_disponiveis:
        num_guindastes_disponiveis = num_maximo_guindastes 
        
    if P.debug:
        print("numero ", num_guindastes_disponiveis)
    return num_guindastes_disponiveis 
    

guindastesStore = simpy.FilterStore(env, capacity=numGuindastes)
guindastesStore.items = [Guindaste(env, number=i) for i in range(numGuindastes)]
    