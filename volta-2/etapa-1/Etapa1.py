import itertools # count automatico
import random
import simpy
import numpy as np
import helper_functions_SimpyPort as helper
import parametros as P


           
class Navio(object):
     
    
    def __init__(self, env, name):
        global cargaTotal
        
        self.env = env
        self.name = name
        self.classe = helper.discreteDist(P.classesNavio, P.distClasses)
        self.carga = helper.cargaNavio(P.classesNavio.index(self.classe), P.cargaClasses)
        P.cargaTotal += self.carga
      
        if P.debug:
            print(self.classe, self.carga)

       
def geraNavio(env):
    while True:
        for i in itertools.count():
            yield env.timeout(random.expovariate(1.0/P.TEMPO_CHEGADA_NAVIO))           
            a = Navio(env, 'Navio %d' %i)
            if P.debug:
                print(a)
    
    
print('Simulacao - Volta 2')   
    
for i in range(P.NUM_REPLICACOES):
    # Create environment and start processes
    env = simpy.Environment()
    env.process(geraNavio(env))
    env.run(until=P.SIM_TIME)
    print('A carga total entregue no ano foi %d' %((P.cargaTotal)))
    P.cargaTotal = 0

