# -*- coding: utf-8 -*-

"""Etapa 2: recepção marítima

Existem dois berços de atracação;
O berço 1 atende no máximo Panamax e o berço 2 qualquer embarcação;
Para atracar, além dos tempos de atracação (volta anterior), o navio deve aguardar as condições de maré favoráveis para Capesizes, que só atracam e desatracam entre 8 e 18h de cada dia;
Parâmetros de saída: tempo aguardando maré;"""

import itertools # count automatico
import random
import simpy
#import numpy as np
import helper_functions_SimpyPort as helper
import parametros as P
#import bercos_classe as B
from bercos_classe import Bercos

ListaBercosClasses=[]
debug = True
numBercos = 2
janelaClasse = [[0,8], [8,18]]

def montaPrioridadeBercos():
    global ListaBercosClasses
    
    for i in range(len(P.classesNavio)):
        tempList =[]
        for j in range(len(P.BercosPrioridades[i])):
            if [P.BercosPrioridades[i][j]] == 1:
                tempList.append(P.BercosRequests[j])
        ListaBercosClasses.append(tempList)
    print(ListaBercosClasses)



class Navio(object):
    #from bercos_classe import atracacao     
    def __init__(self, env, name):
        global cargaTotal
        
        self.env = env
        self.name = name
        self.classe = helper.discreteDist(P.classesNavio, P.distClasses)
        self.carga = helper.cargaNavio(P.classesNavio.index(self.classe), P.cargaClasses)
        P.cargaTotal += self.carga
        env.process(self.atraca(env))
        
    def atraca(self, env):
        print("teste1", env.now)
        while True:
            yield env.timeout(10)
            self.process = env.process(atracacao(self.env, bercosStore, self.classe))
        print("teste2", env.now)
        if P.debug:
            print(self.classe, self.carga) 
        print("teste2", env.now)
        
        

        
        
def geraNavio(env):
    while 1:
        for i in itertools.count():
            yield env.timeout(random.expovariate(1.0/P.TEMPO_CHEGADA_NAVIO))           
            a = Navio(env, "Navio %d" %i)
            print("correct")
            #b = a.Run()
            #print(b)
            print("b ok")
            if P.debug:
                print(a)
    
    
print('Simulacao - Volta 2')


for i in range(P.NUM_REPLICACOES):
    env = simpy.Environment()

    bercosStore = simpy.FilterStore(env, capacity=numBercos)
    bercosStore.items = [Bercos(env, number=i) for i in range(numBercos)]

    bercosStore.items[0].carregaClassesAtendidas([1 ,1 ,0, 0, 0, 0])
    bercosStore.items[1].carregaClassesAtendidas([1 ,1 , 1, 1, 1, 1])

    for berco in bercosStore.items:
        if debug:
            print(berco.number, berco.usages, berco.tempoOcupado)
        
        
    montaPrioridadeBercos

    # Create environment and start processes
        
    berco1 = simpy.Resource(env, 1) # atende no maximo panamax
    berco2 = simpy.Resource(env, 1) # atende qualquer embarcacao
    env.process(geraNavio(env))
    env.run(until=P.SIM_TIME)
    print('A carga total entregue no ano foi %d' %((P.cargaTotal)))
    P.cargaTotal = 0

