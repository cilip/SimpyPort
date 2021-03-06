# -*- coding: utf-8 -*-

"""Etapa 2: recepção marítima

 - Existem dois berços de atracação;
 - O berço 1 atende no máximo Panamax e o berço 2 qualquer embarcação;
 - Para atracar, além dos tempos de atracação (volta anterior), o navio deve
   aguardar as condições de maré favoráveis para Capesizes, que só atracam e 
   desatracam entre 8 e 18h de cada dia;
 - Parâmetros de saída: tempo aguardando maré;"""

import itertools # count automatico
import simpy
import helper_functions_SimpyPort as helper
import parametros as P
import distribuicoes as dist
from bercos_classe import Bercos, statusMareCape
import pandas as pd
import numpy as np
from scipy.stats import t

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
            
    def desatraca(self, env, berco):
        # rotina de desatracação
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
    
    # monta lista de bercos para a estatística final
    for berco in bercosStore.items:
        bercosList.append(berco)
        
    # Create environment and start processe
    env.process(helper.monitor(env,logFila, naviosFila))
    env.process(geraNavio(env))
    env.run(until=P.SIM_TIME)
    df_resultados.ix[i]['Carga entregue'] = P.cargaTotal
    
    for berco in bercosList:
        df_resultados.ix[i]['Atracações '+str(berco.number+1)] = berco.usages
        df_resultados.ix[i]['Tempo ocupado '+str(berco.number+1)] = berco.tempoOcupado
        #df_resultados.ix[i][]
         
    logFila = []
    naviosFila = 0
    P.cargaTotal =0
    
medias = df_resultados.mean()
desvios = df_resultados.std()
IC = t.ppf(0.975,P.NUM_REPLICACOES-1)*desvios/np.sqrt(P.NUM_REPLICACOES)
df_resultados.loc['Média'] = medias
df_resultados.loc['Desvio padrão'] = desvios
df_resultados.loc['IC inf @ 95%'] = medias - IC
df_resultados.loc['IC sup @ 95%'] = medias + IC
print(df_resultados)


excel = helper.abreExcel()
wb = helper.abrePlanilhaExcel(excel,P.pathInterface,P.arqInterface)
ws = helper.selecionaPastaExcel(wb,'Plan1')
# preenche df no Excel
helper.preencheRangeExcel(ws,(1,2),(1,6),['Atracações berço 1', 'Tempo ocupado berço 1 (h)', 'Atracações berço 2', 'Tempo ocupado berço 2 (h)', 'Total embarcado (t)'])
helper.preencheCelulaExcel(ws,2,1,'Média')
helper.preencheCelulaExcel(ws,3,1,'IC inf @ 95%')
helper.preencheCelulaExcel(ws,4,1,'IC sup @ 95%')
helper.preencheRangeExcel(ws,(2,2),(2,6),df_resultados.loc['Média',:].values.tolist())
helper.preencheRangeExcel(ws,(3,2),(3,6),df_resultados.loc['IC inf @ 95%',:].values.tolist())
helper.preencheRangeExcel(ws,(4,2),(4,6),df_resultados.loc['IC sup @ 95%',:].values.tolist())
helper.salvaPlanilhaExcel(wb)