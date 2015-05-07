import parametros as P
ListaBercosClasses = []


def montaPrioridadeBercos():
    global ListaBercosClasses
    
    for i in range(len(P.classesNavio)):
        tempList =[]
        for j in range(len(P.BercosPrioridades[i])):
            if [P.BercosPrioridades[i][j]] == 1:
                tempList.append(P.BercosRequests[j])
        ListaBercosClasses.append(tempList)
    print(ListaBercosClasses)
