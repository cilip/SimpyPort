import numpy as np
import random



# bilbioteca de funções auxiliares para o SimPort


def discreteDist(values, probabilities):
    # retorna um dos elementos da array values segundo uma distribuição de probabilidades fornecida
    values = np.array(values)
    bins = np.add.accumulate(np.array(probabilities))
    result = values[np.digitize(np.random.random_sample(1), bins)]
    #print(result)
    return result[0]

def cargaNavio(index, cargaClasses):
    # retorna uma capacidade de carga a partir da carga min, média e máxima da classe
    
    rangeCarga = cargaClasses[index]
    moda = (rangeCarga[1]-(rangeCarga[2]+rangeCarga[0])*0.5)/3+(rangeCarga[2]+rangeCarga[0])*0.5
    return int(random.triangular (rangeCarga[0],rangeCarga[2], moda))

def testaBib():
    classesNavio = [0, 1, 2, 3, 4, 5] #['Handymax','Panamax', 'Babe Cape', 'Capesize', 'VLOC', 'Valemax']
    distClasses = [0.0, 0.6, 0.0, 0.4, 0.0, 0.0]
    cargaClasses = [(60000, 70000, 80000), (80000, 100000, 120000),(120000, 170000, 180000), (200000, 221000, 250000),(250000, 280000, 300000), (370000, 390000, 400000)] # faixas de Carga de cada classe
    
    
    contaPanamax = 0
    n = 1000
    for i in range(n):
        x = discreteDist(classesNavio, distClasses)
        carga = cargaNavio(classesNavio.index(x), cargaClasses)
        print (x, carga)
        if x == 'Panamax':
            contaPanamax += 1
            
    print ('Panamax gerados: ', contaPanamax/n)


    
    
    
# teste todas as funções da biblioteca
# testaBib()


    




