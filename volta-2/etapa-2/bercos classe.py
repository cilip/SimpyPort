import simpy

numBercos = 2

def statusMare(env):
    horaAtual = env.now % 24
    if horaAtual < 8.0:
        return 0
    elif horaAtual > 18:
        return 0
    else:
        return 1
    
def statusMareCape(env):
    horaAtual = env.now % 24.0
    print (horaAtual)
    
    if horaAtual < 8.0:
        return (8-horaAtual)
    elif horaAtual > 18.0:
        return (24-horaAtual+8)
 
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
       
    


def navio(env, bercosStore, classe):

    berco = yield bercosStore.get(lambda berco: berco.classes[classe] == True)
    print ("Navio classe:", classe, "pegou o berço: ", berco.number, " em ", env.now)
    berco.ocupa()
    if classe == 1:
        tempoMare = statusMareCape(env)
        yield env.timeout(tempoMare)
        print ("Cape aguardou mare ", tempoMare)
    print ('Atracou no berço: ',berco.number, " em: ", env.now)
    
    yield env.timeout(20)
    print ('Desatracou no berço: ', berco.number, " em: ", env.now) 
    berco.desocupa()
    yield bercosStore.put(berco)

env = simpy.Environment()

bercosStore = simpy.FilterStore(env, capacity=numBercos)
bercosStore.items = [Bercos(env, number=i) for i in range(numBercos)]

bercosStore.items[0].carregaClassesAtendidas([1,0,0])
bercosStore.items[1].carregaClassesAtendidas([1,1,0])

for i in range(100):
    env.process(navio(env, bercosStore, 1))
    env.process(navio(env, bercosStore, 0))


env.run(until=24)

for berco in bercosStore.items:
    print(berco.number, berco.usages, berco.tempoOcupado)