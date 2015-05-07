
import simpy
debug = True

numBercos = 2
janelaClasse = [[0,8], [8,18]]

def statusMare(env):
    horaAtual = env.now % 24
    if horaAtual < 8.0:
        return 0
    elif horaAtual > 18:
        return 0
    else:
        return 1
    
def statusMareCape(env, janela):
# retorna o tempo de espera por mare favoravel
    horaAtual = env.now % 24.0
    if debug:
        print (horaAtual)
    
    if horaAtual < janela[0]:
        return (janela[0]-horaAtual)
    elif horaAtual > janela[1]:
        return (24-horaAtual+janela[0])
    else:
        return 0
 
class Bercos (object):
    def __init__(self, env, number):
        self.number = number
        self.usages = 0
        self.start = 0.0
        self.tempoOcupado = 0.0
        self.resource =  simpy.Resource(env, 1)
        self.req = self.resource.request()
        self.classes = []
        
    def ocupa(self):
        yield self.req
        self.start = env.now

    def desocupa(self):
        self.resource.release(self.req)
        self.usages += 1
        self.tempoOcupado += env.now-self.start
    
    def getNumber(self):
        return self.number
    
    def getRequest(self):
        return self.req
    
    def carregaClassesAtendidas(self,value):
        self.classes = value
       
    


def atracacao(env, bercosStore, classe):
    
    berco = yield bercosStore.get(lambda berco: berco.classes[classe] == True)
    if debug:
        print ("Navio classe:", classe, "pegou o berco: ", berco.number, " em ", env.now)
    
    berco.ocupa()

    if classe == 3:
        tempoMare = statusMareCape(env, janelaClasse[classe])
        if tempoMare > 0:
            yield env.timeout(tempoMare)
            if debug:
                print ("Cape aguardou mare ", tempoMare)
    print ('Atracou no berco: ', berco.number, " em: ", env.now) 
    berco.desocupa()
    yield bercosStore.put(berco)

