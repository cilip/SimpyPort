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
import helper_functions_SimpyPort as helper
import parametros as P
import distribuicoes as dist
from bercos_classe import Bercos, statusMareCape
import pandas as pd
import numpy as np
from scipy.stats import t
from guindaste import Guindaste

numGuindastes = 3
constante_velocidade = 5 #exemplo
numBercos = 2
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
      
      
    #processa todos os guindastes atuantes no navio e atualiza velocidade e carga transportada
    #no fim, da um yield com um tempo pequeno
      
    def monitor(self, constante_velocidade):
        global armazem
        start = env.now
        num_guindastes = self.guindastes
        while num_guindastes == self.guindastes:
            velocidade = constante_velocidade * num_guindastes
        tempo = env.now - start
        carga_transferida = velocidade*tempo
        self.carga_total_transferida += carga_transferida
        armazem.put(carga_transferida)
        
        yield(5)
        
        
            
    def opera(self, env):
        #pega o numero de guindastes disponiveis
        print("opera")
        self.guindastes = guindaste.guindastes_disponiveis(env, guindastesStore, self.classe) #lista/numero
        print("opera 2")
        #navio pega todos os guindastes disponiveis na Store
        for i in range(len(self.guindastes)):
            print("opera 3")
            guindaste_pego = yield guindastesStore.get() #escolher qualquer guindaste que esteja na lista de self.guindastes do navio em questao
            print("Pegou guindaste",guindaste_pego)
            #altera informacoes para cada guindaste
            
            yield guindaste_pego.ocupa(env, self.name) #request
            env.process(guindaste_pego.quebraGuindaste(env, guindaste_pego)) 
            
        #tempo de desatracacao
        #velocidade difere conforme numero de guindastes difere (quebra)
        while self.carga_total_transferida != self.carga:
            yield env.process(self.monitor(constante_velocidade))
        
       
        if P.debug:
            print ('%s classe %i termina operação no berço %i em %.2f' %(self.name, self.classe, self.berco, env.now))

    

    def desatraca(self, env, berco):
        # rotina de desatracação
        for i in range (self.guindastes):
            yield self.guindaste[i].desocupa(env)
            yield guindastesStore.put(self.guindaste[i])
            
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
                yield self.env.timeout(tempoMare)
                if P.debug:
                    print ("%s classe cape aguardou mare por %.1f horas" %(self.name, tempoMare))
        return tempoMare
        
      
        
def geraNavio(env):
    while 1:
        for i in itertools.count(1):
            yield env.timeout(dist.chegadas())           
            Navio(env, "Navio %d" %i)
            
 

print('Simulacao > Etapa 2 - Volta 2')
dist.defineSeed(P.RANDOM_SEED)
helper.defineSeedNumpy(P.RANDOM_SEED)
columns = ['Atracações 1', 'Tempo ocupado 1', 'Atracações 2', 'Tempo ocupado 2', 'Carga entregue']
df_resultados = pd.DataFrame(columns=columns, index=['Replicação ' + str(i) for i in range(P.NUM_REPLICACOES)])

for i in range(P.NUM_REPLICACOES):
    env = simpy.Environment()
    logFila = []
    bercosList = []
    bercosStore = simpy.FilterStore(env, capacity=numBercos)
    bercosStore.items = [Bercos(env, number=i) for i in range(numBercos)]

    bercosStore.items[0].carregaClassesAtendidas([1 ,1 ,0, 0, 0, 0])
    bercosStore.items[1].carregaClassesAtendidas([1 ,1 , 1, 1, 1, 1])
    
    guindastesStore = simpy.FilterStore(env, capacity=numGuindastes)
    guindastesStore.items = [Guindaste(env, number=i) for i in range(numGuindastes)]

    
    # monta lista de bercos para a estatística final
    for berco in bercosStore.items:
        bercosList.append(berco)
        
    # Create environment and start processe

    env.process(helper.monitor(env,logFila, naviosFila))
    env.process(geraNavio(env))
    armazem = simpy.Container(env, CAPACIDADE, init=0)
    env.run(until=P.SIM_TIME)
