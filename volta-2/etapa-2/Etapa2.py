# -*- coding: utf-8 -*-

"""Etapa 2: recepção marítima

Existem dois berços de atracação;
O berço 1 atende no máximo Panamax e o berço 2 qualquer embarcação;
Para atracar, além dos tempos de atracação (volta anterior), o navio deve aguardar as condições de maré favoráveis para Capesizes, que só atracam e desatracam entre 8 e 18h de cada dia;
Parâmetros de saída: tempo aguardando maré;"""

import itertools # count automatico
import random
import simpy
import numpy as np
import helper_functions_SimpyPort as helper
import parametros as P
import bercos_classe as B

ListaBercosClasses=[]

def montaPrioridadeBercos():
    global ListaBercosClasses
    
    for i in range(len(classesNavio)):
        tempList =[]
        for j in range(len(BercosPrioridades[i])):
            if [BercosPrioridades[i][j]] == 1:
                tempList.append(BercosRequests[j])
        ListaBercosClasses.append(tempList)    

class Navio(object):
    import bercos_classe as B
        
    def __init__(self, env, name):
        global cargaTotal
        
        self.env = env
        self.name = name
        self.classe = helper.discreteDist(P.classesNavio, P.distClasses)
        self.carga = helper.cargaNavio(P.classesNavio.index(self.classe), P.cargaClasses)
        P.cargaTotal += self.carga
        self.process = env.process(self.B.atracacao(env, B.bercosStore, self.classe))
        if P.debug:
            print(self.classe, self.carga)
        
    def berco(self, env):
        env.process(B.navio(env, B.bercosStore, self.classe))

        
        
def geraNavio(env):
  
    while True:
        for i in itertools.count():
            yield env.timeout(random.expovariate(1.0/P.TEMPO_CHEGADA_NAVIO))           
            a = Navio(env, 'Navio %d' %i)
            if P.debug:
                print(a)
    
    
print('Simulacao - Volta 2')   
montaPrioridadeBercos

for i in range(P.NUM_REPLICACOES):
    # Create environment and start processes
    env = simpy.Environment()
    berco1 = simpy.Resource(env, 1) # atende no maximo panamax
    berco2 = simpy.Resource(env, 1) # atende qualquer embarcacao
    env.process(geraNavio(env))
    env.run(until=P.SIM_TIME)
    print('A carga total entregue no ano foi %d' %((P.cargaTotal)))
    P.cargaTotal = 0

