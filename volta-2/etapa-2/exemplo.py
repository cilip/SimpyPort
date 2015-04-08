
numClasses = 6
bercos = [simpy.Resource(env, 1) for i in range(numBercos)] #berco[0] ...

prefBercoClasse = [[0,1], [0,1], [0],[0],[0],[0] ]
bercoCandidatoClasse = []
for j in range(numClasses):
    bercoCandidatoClasse.append([bercos[i].request for in prefBercoClasse[j]])
    
with servidor.request() as req:
    yield req



