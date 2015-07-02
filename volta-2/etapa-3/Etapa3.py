"""
Etapa 3: operação

Existem três guindastes para operação;
O navio Panamax opera com no máximo 2 guindastes e o Capesize 3 guindastes;
Quando um atraca, ele solicita o máximo de guindastes livres;
Os guindastes entram em manutenção preventiva 10% do tempo no ano (nunca de modo simultâneo), por 3 h, constantes;
Os guindastes quebram em intervalos exponenciais de 6h, com duração de 1h cada quebra, também exponenciais.
A taxa nominal de operação dos guindastes é de 1.000 tph;
O modelo deve fornecer o tempo ocupado, livre, em mp e mc dos guindastes e a taxa comercial do berço para cada tipo de navio;
"""
import itertools # count automatico
import simpy

import pandas as pd
import numpy as np
from scipy.stats import t

from bercos_classe import Bercos, statusMareCape
from guindaste import Guindaste
from guindaste import guindastes_disponiveis
from guindaste import checar_quebra
import helper_functions_SimpyPort as helper
import parametros as P
from parametros import guindasteBerco
import distribuicoes as dist



numGuindastes = 3
constante_velocidade = 10000 #exemplo em tph
numBercos = 2
#checar_quebra = [0, 0, 0] #0 corresponde a funcionamento e 1 a quebra
janelaClasse = [[[8.0,12.0], [18.0,22.0]],[[8.0,12.0], [18.0,22.0]],[[8.0,12.0], [18.0,22.0]],[[8.0,12.0], [18.0,22.0]],[[8.0,12.0], [18.0,22.0]],[[8.0,12.0], [18.0,22.0]],[[8.0,12.0], [18.0,22.0]]]
naviosFila = 0
CAPACIDADE = 1000000 #capacidade armazem


class Navio(object):
    #from bercos_classe import atracacao     
    def __init__(self, env, name):
        global cargaTotal
        
        self.env = env
        self.name = name
        self.berco = 0
        self.classe = helper.discreteDist(P.classesNavio, P.distClasses)
        self.carga = helper.cargaNavio(P.classesNavio.index(self.classe), P.cargaClasses)
        self.carga_total_transferida = 0
        self.guindastes = 0
        self.velocidade = 0
        self.set_guindastes = set()
        self.quebra_pausa = False
        self.tempo_restante = 0
        if P.debug:
            print('%s classe %i chega em %.2f' %(self.name,self.classe, env.now))
        
        env.process(self.linhaTempo(env))
        
    def linhaTempo(self, env):
        # atraca
        # note o yield garantindo que só após o termino da operação, o controle volta para a linha seguinte!
        berco = yield env.process(self.atraca(env))
        
        # opera
        yield env.process(self.opera(env)) 

        # desatraca        
        yield env.process(self.desatraca(env, berco))
        
    def atraca(self, env):
        
        global naviosFila
        
        naviosFila += 1
        if P.debug:
            print('%s classe %i entra em fila em: %.2f Navios em fila: %d' % (self.name, self.classe, env.now, naviosFila))
        
        berco = yield bercosStore.get(lambda berco: berco.classes[self.classe] == True)
        self.berco = berco.number
        naviosFila -= 1
        
        if P.debug:
            print ("%s classe %i inicia atracação no berço %i em %.2f" % (self.name, self.classe, self.berco, env.now))
        
        yield berco.ocupa(env, self.classe)
        
        tempoMare = yield env.process(self.mare(env))
        berco.mare(tempoMare,0)
        
        if P.debug:
            print ('%s classe %i atracou no berço %i em %.2f' %(self.name, self.classe, self.berco, env.now))
        return berco
      

    def opera(self, env):
        
        #pega o numero de guindastes disponiveis
        if P.debug:
            print("> %s inicia operação" %self.name)

        self.guindastes = guindastes_disponiveis(env, guindastesStore, self.classe) #lista/numero
        if self.guindastes == 0:
            while len(guindastesStore.items) == 0:
                yield(3)
            self.guindastes = len(guindastesStore.items) #=1

        if P.debug:
            print("> %s tem %i guindastes à diposição" %(self.name, self.guindastes))       
        
        #navio pega todos os guindastes disponiveis na Store
        for i in range(self.guindastes):
            #numero_guindaste = Guindaste.getNumber(self.guindastes[i])

            guindaste_pego = yield guindastesStore.get() #escolher qualquer guindaste que esteja na lista de self.guindastes do navio em questao
            numero_guindaste = Guindaste.getNumber(guindaste_pego)
            guindasteBerco[numero_guindaste] = self.berco # armazena dicionário para saber onde esta o guindaste
            self.set_guindastes.add(guindaste_pego)             


            
            if P.debug:
                print("> %s ocupou o guindaste %i" %(self.name, numero_guindaste))  
            #env.process(guindaste_pego.quebraGuindaste(env, self.guindastes)) 

            #velocidade difere conforme numero de guindastes difere (quebra)

            while self.carga_total_transferida < self.carga:
                try:
                    yield env.process(self.monitor(env, guindaste_pego, constante_velocidade))
                except simpy.Interrupt:
                    if P.debug:
                        print('Guindaste sofre quebra em %.1f horas.' % (env.now)) 
               
            if P.debug:
                    print ('> %s classe %i termina operação no berço %i em %.2f' %(self.name, self.classe, self.berco, env.now))




            #processa todos os guindastes atuantes no navio e atualiza velocidade e carga transportada
            #no fim, da um yield com um tempo pequeno
      
    def monitor(self, env, guindaste, constante_velocidade):
        
        global armazem
        debugMonitor = True
        
        if P.debug:
            print("> %s inicializa o monitor" %self.name)
           #altera informacoes para cada guindaste
            yield (guindaste.ocupa(env, self.name)) ########
            
        start = env.now
        self.velocidade = constante_velocidade*self.guindastes
        self.tempo_restante = (self.carga - self.carga_total_transferida)/self.velocidade
                    
        while self.tempo_restante > 0:
            if debugMonitor:
                print(">> %s carga faltante %d, velocidade %d, tempo esperado %.2f" %(self.name,(self.carga - self.carga_total_transferida), self.velocidade, self.tempo_restante))

            yield env.timeout(5)
            self.velocidade = constante_velocidade * self.guindastes
            tempo = env.now - start
            carga_transferida = self.velocidade*tempo
            self.carga_total_transferida += carga_transferida
            armazem.put(carga_transferida)
            self.tempo_restante = (self.carga - self.carga_total_transferida)/self.velocidade
 
 
    def desatraca(self, env, berco):
        
        # rotina de desatracação
        for guindaste in self.set_guindastes:
            yield guindaste.desocupa(env)
            yield guindastesStore.put(guindaste)
            if P.debug:
                print("Guindaste %i desocupado" %Guindaste.getNumber(self.guindastes[i]))
                
        tempoMare = yield env.process(self.mare(env))
        berco.mare(tempoMare,1)        
        berco.desocupa(env)
        bercosStore.put(berco)
        
        if P.debug:
            print ('%s classe %i desatracou do berço %i em %.2f tempo total ocupado: %.1f h' %(self.name, self.classe, self.berco, env.now, berco.tempoOcupado))
        
    def mare(self, env):
        # rotina de controle de maré
        tempoMare = 0
        if self.classe == 3:
            tempoMare = statusMareCape(env, janelaClasse[self.classe])
            if tempoMare > 0:
                yield env.timeout(tempoMare)
                if P.debug:
                    print ("%s classe cape aguardou mare por %.1f horas" %(self.name, tempoMare))
        return tempoMare
        
    def funcao_quebra(self, env):
        global checar_quebra
        while True:
            for i in range(len(self.set_guindastes)):
                if checar_quebra[self.set_guindastes[i]] == 1:
                    while checar_quebra[i]==1:
                        self.quebra_pausa = True
                    self.quebra_pausa = False
        
def geraNavio(env):
    while 1:
        for i in itertools.count(1):
            yield env.timeout(dist.chegadas())           
            Navio(env, "Navio %d" %i)
             
      

print('Simulacao > Etapa 3 - Volta 2')
dist.defineSeed(P.RANDOM_SEED)
helper.defineSeedNumpy(P.RANDOM_SEED)
columns = ['Atracações 1', 'Tempo ocupado 1', 'Atracações 2', 'Tempo ocupado 2', 'Carga entregue']
df_resultados = pd.DataFrame(columns=columns, index=['Replicação ' + str(i) for i in range(P.NUM_REPLICACOES)])

for i in range(P.NUM_REPLICACOES):
    env = simpy.Environment()
    logFila = []
    bercosList = []
    bercosStore = simpy.FilterStore(env, capacity=numBercos)
    bercosStore.items = [Bercos(env, number=j) for j in range(numBercos)]

    bercosStore.items[0].carregaClassesAtendidas([1 ,1 ,0, 0, 0, 0])
    bercosStore.items[1].carregaClassesAtendidas([1 ,1 , 1, 1, 1, 1])
    
    guindastesStore = simpy.FilterStore(env, capacity=numGuindastes)
    guindastesStore.items = [Guindaste(env, number=j) for j in range(numGuindastes)]

    
    # monta lista de bercos para a estatística final
    for berco in bercosStore.items:
        bercosList.append(berco)
        
    # Create environment and start processe

    env.process(helper.monitor(env,logFila, naviosFila))
    env.process(geraNavio(env))
    armazem = simpy.Container(env, CAPACIDADE, init=0)
    env.run(until=P.SIM_TIME)
