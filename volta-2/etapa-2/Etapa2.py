"""Etapa 2: recep��o mar�tima

Existem dois ber�os de atraca��o;
O ber�o 1 atende no m�ximo Panamax e o ber�o 2 qualquer embarca��o;
Para atracar, al�m dos tempos de atraca��o (volta anterior), o navio deve aguardar as condi��es de mar� favor�veis para Capesizes, que s� atracam e desatracam entre 8 e 18h de cada dia;
Par�metros de sa�da: tempo aguardando mar�;"""

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
        self.process = env.process(self.atracacao(env))
        if P.debug:
            print(self.classe, self.carga)
        
    def atracacao(self, env):
        for i in range(len(P.classesNavio)):
            if self.classe == P.classesNavio[i]:
                self.bercos = [P.ListaBercosClasses[i]]
        start = env.now
        self.result = yield env.any_of(self.bercos)
        intervalo_tempo = env.now - start
        print(intervalo_tempo)
        
        
        request.release(self.result)


       
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
    berco1 = simpy.Resource(env, 1) #atende no maximo panamax
    berco2 = simpy.Resource(env, 1) #atende qualquer embarcacao
    env.process(geraNavio(env))
    env.run(until=P.SIM_TIME)
    print('A carga total entregue no ano foi %d' %((P.cargaTotal)))
    P.cargaTotal = 0

