"""

    Guindastes estao organizados em uma lista Store, conforme sao "pegos" e usados nos navios, saem da lista. Quando terminam de ser usados,
voltam para a lista e ficam disponiveis para a proxima embarcacao.
    


"""
import simpy
import parametros as P
import random
from parametros import guindasteBerco

checar_quebra = [0,0,0]

env = simpy.Environment()


TEMPO_QUEBRA_GUINDASTE = 10 #exmeplo de valor
tempoQuebraGuindaste = 0
TEMPO_MEDIO_CONSERTO = 1.0 #exemplo de valor

class Guindaste(object):
    def __init__(self, env, number):
        self.number = number
        self.resource =  simpy.PreemptiveResource(env, capacity = 1)
        self.broken = False
        self.start = env.now
        self.navioAtual = ''

       
    def quebraGuindaste(self, env, guindastes_navio):
        #guindastes_navio e a variavel que conta quantos guindastes ha
        global tempoQuebraGuindaste
        global checar_guindaste
        
        while True:
            yield env.timeout(random.expovariate(1.0/TEMPO_QUEBRA_GUINDASTE))
            if not self.broken:
                with self.resource.request(priority = 1) as req:
                    yield req
                    #if P.debug:
                        #print('Guindaste QUEBROU em %.1f horas.' % (env.now))
                    t1 = env.now
                    self.broken=True
                    
                    checar_quebra[guindasteBerco[self.number]] = 1
                    guindastes_navio -= 1
                    
                    yield env.timeout(random.expovariate(1.0/TEMPO_MEDIO_CONSERTO))
                    guindastes_navio += 1
                    if P.debug:
                        print('Guindaste ', self.number,' LIBERADO em %.1f horas.' % (env.now))
                    t2 = env.now
                    t = t2 - t1
                    tempoQuebraGuindaste += t
                    
                    self.broken = False
                    checar_quebra[self.number] = 0
                    

    def getNumber(self):
        return self.number
    
    def getRequest(self):
        return self.resource.request(priority = 2)    
    
    def ocupa(self, env, name_navio):
        self.start = env.now
        self.navioAtual = name_navio
        return self.resource.request(priority = 2) #(priority = 2)
          
    def desocupa(self, env):
        self.resource.release(self.req)
         
        
    def checar_navio(self, env):
        return self.navioAtual
            

        
 

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

        
    lista_guindastes = []
    for i in range (num_guindastes_disponiveis):
        lista_guindastes.append(guindastesStore.items[i])

    return num_guindastes_disponiveis
    

    