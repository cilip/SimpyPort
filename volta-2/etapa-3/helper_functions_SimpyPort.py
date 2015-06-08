import numpy as np
import random
 

import win32com.client as win32 # carrega o módulo python for windows extension https://github.com/pythonexcels/examples


# bilbioteca de funções auxiliares para o SimPort

def abreExcel():
    # abre o excel (caso ainda não esteja aberto)
    excel = win32.gencache.EnsureDispatch('Excel.Application')
    excel.Visible = True
    return excel
 
def abrePlanilhaExcel(excel, path, arq):
    # seleciona e abre uma planilha xlsx
    for i in range(1,excel.Workbooks.Count):
        if excel.Workbooks(i).Name == arq:
            return excel.Workbooks(i)
    return excel.Workbooks.Open(path+arq) #retorna um workbook

def selecionaPastaExcel(workbook, pasta):
    # seleciona e retorna a pasta do excel
    return workbook.Worksheets(pasta) # retorna um worksheet

def preencheCelulaExcel(worksheet, linha, coluna, value):
    #preenche uma célula do excel
    worksheet.Cells(linha,coluna).Value = value
    
def preencheRangeExcel(worksheet, celula1, celula2, valuesLista):
    # preenche um range do excel com valores de uma lista
    worksheet.Range(worksheet.Cells(celula1[0],celula1[1]),worksheet.Cells(celula2[0],celula2[1])).Value = valuesLista

def preencheRangeStrExcel(worksheet, rangeStr, valuesLista):
    # preenche um range do excel com valores de uma lista
    worksheet.Range(rangeStr).Value = valuesLista

def salvaPlanilhaExcel(workbook):
    #salva uma planilha excel
    workbook.Save()

def fechaExcel(excel):
    # fecha o excel
    excel.Application.Quit()

def defineSeedNumpy(seed):
    np.random.seed(seed)
    
def discreteDist(values, probabilities):
    # retorna um dos elementos da array values segundo uma distribuição de probabilidades fornecida
    try:
        values = np.array(values)
        bins = np.add.accumulate(np.array(probabilities))
        result = values[np.digitize(np.random.random_sample(1), bins)]
        #print(result)
        return result[0]
    except:
        print('ERROR: discreteDist')

def cargaNavio(index, cargaClasses):
    # retorna uma capacidade de carga a partir da carga min, média e máxima da classe
    try:
        rangeCarga = cargaClasses[index]
        moda = (rangeCarga[1]-(rangeCarga[2]+rangeCarga[0])*0.5)/3+(rangeCarga[2]+rangeCarga[0])*0.5
        return int(random.triangular (rangeCarga[0],rangeCarga[2], moda))
    except:
        print('ERROR: cargaNavio')

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
    
def monitor(env, logFila, valor, freq=1):
    global naviosFila
    while True:
        # collect statistics 
        logFila.append(valor)
        yield env.timeout(freq)


    
    
    
# teste todas as funções da biblioteca
# testaBib()


    




