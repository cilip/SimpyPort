# -*- coding: utf-8 -*-

"""Etapa 2: recepção marítima

 - Existem dois berços de atracação;
 - O berço 1 atende no máximo Panamax e o berço 2 qualquer embarcação;
 - Para atracar, além dos tempos de atracação (volta anterior), o navio deve
   aguardar as condições de maré favoráveis para Capesizes, que só atracam e 
   desatracam entre 8 e 18h de cada dia;
 - Parâmetros de saída: tempo aguardando maré;"""

import itertools # count automatico
import random
import simpy
import helper_functions_SimpyPort as helper
import parametros as P
import distribuicoes as dist
from bercos_classe import Bercos, statusMareCape


debug = True
numBercos = 2
janelaClasse = [[[8.0,12.0], [18.0,22.0]],[[8.0,12.0], [18.0,22.0]],[[8.0,12.0], [18.0,22.0]],[[8.0,12.0], [18.0,22.0]],[[8.0,12.0], [18.0,22.0]],[[8.0,12.0], [18.0,22.0]],[[8.0,12.0], [18.0,22.0]]]
naviosFila = 0

class Navio(object):
    #from bercos_classe import atracacao     
    def __init__(self, env, name):
        global cargaTotal
        self.env = env
        self.name = name
        self.berco = 0
        self.classe = helper.discreteDist(P.classesNavio, P.distClasses)
        self.carga = helper.cargaNavio(P.classesNavio.index(self.classe), P.cargaClasses)
        if P.debug:
            print('%s classe %i chega em %.2f' %(self.name,self.classe, env.now))
        
        env.process(self.linhaTempo(env))
        
    def linhaTempo(self, env):
        # atraca
        yield env.process(self.atraca(env))
        
        # opera
        # note o yield garantindo que só após o termino da operação, o controle volta para a linha seguinte!
        yield env.process(self.opera(env)) 

        # desatraca        
        yield env.process(self.desatraca(env))
        
    def atraca(self, env):
        
        global naviosFila
        
        naviosFila += 1
        if P.debug:
            print('%s classe %i entra em fila em: %.2f Navios em fila: %d' % (self.name, self.classe, env.now, naviosFila))
        
        berco = yield bercosStore.get(lambda berco: berco.classes[self.classe] == True)
        self.berco = berco.number
        if debug:
            print ("%s classe %i inicia atracação no berço %i em %.2f" % (self.name, self.classe, self.berco, env.now))

        berco.ocupa(env)
        
        yield env.process(self.mare(env))
        
        if P.debug:
            print ('%s classe %i atracou no berço %i em %.2f' %(self.name, self.classe, self.berco, env.now))
        return berco
            
    def desatraca(self, env):
        berco.desocupa(env)
        
        if P.debug:
            print ('%s classe %i desatracou do berço %i em %.2f' %(self.name, self.classe, self.berco, env.now))
        yield bercosStore.put(berco)
        
    def mare(self, env):
        # rotina de controle de maré
        if self.classe == 3:
            tempoMare = statusMareCape(env, janelaClasse[self.classe])
            if tempoMare > 0:
                yield self.env.timeout(tempoMare)
                if debug:
                    print ("%s classe cape aguardou mare por %.1f horas" %(self.name, tempoMare))  
        
    def opera(self, env):
        # apenas para teste, colocar aqui a lógica de opeação
        if P.debug:
            print ('%s classe %i inicia operação no berço %i em %.2f' %(self.name, self.classe, self.berco, env.now))
        yield self.env.timeout(dist.carregamento())
        if P.debug:
            print ('%s classe %i termina operação no berço %i em %.2f' %(self.name, self.classe, self.berco, env.now))
        P.cargaTotal += self.carga

        
        
        
def geraNavio(env):
    while 1:
        for i in itertools.count(1):
            yield env.timeout(dist.chegadas())           
            Navio(env, "Navio %d" %i)
    
    
print('Simulacao - Volta 2')

random.seed = P.RANDOM_SEED

for i in range(P.NUM_REPLICACOES):
    env = simpy.Environment()

    bercosStore = simpy.FilterStore(env, capacity=numBercos)
    bercosStore.items = [Bercos(env, number=i) for i in range(numBercos)]

    bercosStore.items[0].carregaClassesAtendidas([1 ,1 ,0, 0, 0, 0])
    bercosStore.items[1].carregaClassesAtendidas([1 ,1 , 1, 1, 1, 1])
       
        
    #montaPrioridadeBercos()

    # Create environment and start processes
        
    berco1 = simpy.Resource(env, 1) # atende no maximo panamax
    berco2 = simpy.Resource(env, 1) # atende qualquer embarcacao
    env.process(geraNavio(env))
    env.run(until=P.SIM_TIME)
    print('A carga total entregue no ano foi %d' %(P.cargaTotal))
    
    for berco in bercosStore.items:
        if debug:
            print("Berço %i atendeu %d navios e ficou ocupado por %.f horas" % (berco.number, berco.usages, berco.tempoOcupado))