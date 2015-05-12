
import simpy

debug = True


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
    try:
        horaAtual = env.now % 24.0
        if debug:
            print ("Testando maré em %.1f para a janela" % horaAtual, janela[0][0], janela[0][1], janela[1][0], janela[1][1])
        
        if horaAtual < janela[0][0]:
            return (janela[0][0]-horaAtual)
        elif horaAtual > janela[0][1]:
            if horaAtual < janela[1][0]:
                return (janela[1][0]-horaAtual)
            elif horaAtual > janela[1][1]:
                return (24-horaAtual+janela[0][0])
            else:
                return 0
        else:
            return 0
    except:
        print('ERROR: statusMareCape', horaAtual, janela[0][0], janela[0][1], janela[1][0], janela[1][1])
     
class Bercos (object):
    def __init__(self, env, number):
        self.number = number
        self.usages = 0
        self.start = 0.0
        self.tempoOcupado = 0.0
        self.resource =  simpy.Resource(env, 1)
        self.req = self.resource.request()
        self.classes = []
        self.tempoMare = [0.0, 0.0]
        self.contaMare = [0, 0]
        
    def ocupa(self, env, classe):
        self.start = env.now
        self.classeAtual = classe
        return self.req

    def desocupa(self, env):
        self.resource.release(self.req)
        self.usages += 1
        self.tempoOcupado += env.now-self.start
        self.classeAtual = 0
    
    def mare(self, tempo, tipo):
        # tipo 0 atracação, 1 desatracação
        self.tempoMare[tipo] += tempo
        if tempo > 0:
            self.contaMare[tipo] += 1
    
    def getNumber(self):
        return self.number
    
    def getRequest(self):
        return self.req
    
    def carregaClassesAtendidas(self,value):
        self.classes = value
        if debug:
            print('Berço %i atende às classes' %self.number, self.classes)
    
