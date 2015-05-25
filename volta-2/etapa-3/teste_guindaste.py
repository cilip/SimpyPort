import simpy

env = simpy.Environment()

guindaste1 = simpy.PreemptiveResource(env, capacity = 1)
guindaste2 = simpy.PreemptiveResource(env, capacity = 1)
guindaste3 = simpy.PreemptiveResource(env, capacity = 1)


guindastesStore = simpy.Store(env, capacity=3)
guindastesStore.items = [guindaste1, guindaste2, guindaste3]

num_guindastes = 0

def guindastes_disponiveis(env, guindastesStore):
    num_guindastes_disponiveis = len(guindastesStore.items)
    print("numero ", num_guindastes_disponiveis)
    return num_guindastes_disponiveis    


def navio(env, guindastesStore):
    for i in range(guindastes_disponiveis(env, guindastesStore)):
        guindaste = yield guindastesStore.get()
        num_guindastes +=1
        print("NUMERO GUINDASTES = %d" %num_guindastes)

for i in range(2):
    env.process(navio(env, guindastesStore))
env.run()