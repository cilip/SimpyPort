# -*- coding: utf-8 -*-
"""
Created on Mon May 11 07:53:36 2015

@author: medina

Programa de carregamento de parâmetros da interface para o programa principal

São utilizados dois módulos:
   1) openpyxl: quando a informação buscada na planilha está em uma célula especifica (definida
       pelo seu "name" ou endereço column-row)
   2) pandas: quanda a informação está em forma tabular e o objetivo é transformá-la em lista
   
"""
 
from parametros import * # importa os parâmetros do modelo
import openpyxl
import pandas as pd
debug = True


def abreExcel(path, arqName):
    # abre uma planilha Excel fornecida
    # retorna o arquivo Excel aberto no pandas
    return pd.ExcelFile(path+arqName)
    
def fechaExcel(xlsFile):
    # fecha uma planilha Excel fornecida
    xlsFile.close()
    
def carregaDFPasta(df, xlsFile, pastaStr):
    # salva dataframe em uma pasta do arqExcel
    df.pd.to_excel(xlsFile, sheet_name = pastaStr) 
    
    # fecha e salva o arquivo excel do pandas
    arqExcel.save()
    
def carregaPastaDF(xlsFile, xlsSheet):
    # carrega a xlsSheet da planilha xlsFile em um dataframe
    # retorna um dataframe
    return xlsFile.parse(xlsSheet)
    
def converteColunaDFemLista(df, coluna):
    # converte uma coluna do dataframe em uma lista
    # retorna uma lista com os elementos sem repetição
    return list(set(df[coluna]))
    
def carregaPastaLista(xlsFile, xlsSheet):
    # monta lista a partir da pasta xlsSheet da planilha xlsFile do Excel
    df = carregaPastaDF(xlsFile, xlsSheet)
    return df.values.tolist()

def carregaValorRangeName (workbook,name):
    nr = workbook.get_named_range(name)
    if nr is None:
        raise Exception("Erro: range não encontrado")
    else:
        ws = nr.destinations[0][0]
        cell = ws.range(nr.destinations[0][1])
        if type(cell) is not openpyxl.cell.Cell:
            raise Exception("A função 'read_value_from_named_range' só pode ser utilizada para ranges de uma única célula")
        else:
            return cell.value
    
def carregaParametros(path,arqName):
    # carrega parâmetros do modelo da pasta Parâmetros do xlsFile
    wb = openpyxl.load_workbook(filename = path+arqName)
    global timeHorizon
    timeHorizon = carregaValorRangeName(wb,paramListInterface[0])
    
def itemKey(item):
    return item[0]
    
class Tarefa(object):
    def __init__(self, trem, data, produto, patio, rota, pilha):
        self.trem = trem
        self.data = data
        self.produto = produto
        self.patio = patio
        self.rota = rota
        self.pilha = pilha

class Pilha(object):
    def __init__(self, patio, produto, balInicio, balFim, produtividade):
        self.produto = produto
        self.patio = patio
        self.balizas = balFim - balInicio + 1
        self.balizaInicio = balInicio
        self.balFim = balFim
        self.produtividade = produtividade
        self.capacidade = self.defineCapacidade()
        self.carga = 0
        
    def defineCapacidade(self):
        # define a capacidade inicial da pilha
        return self.balizas*self.produtividade
    
    def descarga(self, lote):
        # descarrega na pilha a quantidade lote
        self.carga += lote
        return self.carga
    
    def cargaInicial(self, carga):
        # define a carga inicial da pilha (para as pilhas já existentes na planilha)
        self.carga = carga
        
    def embarque(self, lote):
        # embarca (esvazia) da pilha a quantidade lote
        self.carga -= lote
        return self.carga
        
class Patio(object):
    def __init__(self,name,numPatio, numBalizas):
        self.name = name
        self.number = numPatio
        self.balizas = numBalizas
        self.statusBaliza = []
        for baliza in range(numBalizas+1):
            self.statusBaliza.append(0)
        self.pilhas = []
        self.produtividade = defaultProdutividadeBaliza
    
    def alteraProdutividade(self, df):
        for produto in range(1,maxProdutos):
            self.produtividade[produto] = df['Produto '+str(produto) + ' (kt/baliza)']
    
    def retornaProdutividade(self, produto):
        return self.produtividade[produto]
        
    def criaPilha(self, produto, balInicio, balFim): 
        for baliza in range(balInicio,balFim):
            self.statusBaliza[baliza] = 1
        self.pilhas.append(Pilha(self.number, produto, balInicio, balFim, self.produtividade[produto]))
        
    def liberaPilha(self, number):
        for baliza in range(balInicio,balFim):
            self.statusBaliza[baliza] = 0
        self.pilhas.pop(number)
        
    

        
# programa principal (em teste)
carregaParametros(pathInterface, arqInterface)
xlsFile = abreExcel(pathInterface, arqInterface)
if debug:
    print('Horizonte de tempo da simulação: %d dias' % timeHorizon)

"""
     monta Pátios e Pilhas
"""
df_patios = carregaPastaDF(xlsFile, sheetListInterface[2])
df_pilhas = carregaPastaDF(xlsFile, sheetListInterface[8])

patiosList = []
codigoPatio = {} # dicionario para localizar um patio da CSN no programa
contaPatio = 0

# cria lista de pátios a partir da df_patios
for patio in list(df_patios.columns.values):
    patiosList.append(Patio(patio, numPatio = df_patios[patio]['Número do pátio'], numBalizas = df_patios[patio]['Número de balizas']))
    codigoPatio[df_patios[patio]['Número do pátio']] = contaPatio    
    patiosList[contaPatio].alteraProdutividade(df_patios[patio])
    contaPatio += 1

# cria lista de pilhas para cada pátio a partir da df_pilhas
for pilha in range(len(df_pilhas)):
    patiosList[codigoPatio[df_pilhas.ix[pilha]['Pátio']]].criaPilha(df_pilhas.ix[pilha]['Produto'],df_pilhas.ix[pilha]['Baliza inicial'],df_pilhas.ix[pilha]['Baliza final'])

"""
     monta lista de trens
"""
listaTrens = carregaPastaLista(xlsFile, sheetListInterface[3])
listaTrens = sorted(listaTrens, key = itemKey) # ordena lista de trens por data de atendimento
if debug:
    print('Número de trens carregados: %d' % len(listaTrens) )
    
"""
     monta lista de navios
"""

listaNavios = carregaPastaLista(xlsFile, sheetListInterface[4])
if debug:
    print('Número de navios carregados: %d' % len(listaNavios) )
    
"""
     monta lista de equipamentos
"""
    
listaEquipamentos = carregaPastaLista(xlsFile, sheetListInterface[5])
if debug:
    print('Número de equipamentos carregados: %d' % len(listaEquipamentos) )   

fechaExcel(xlsFile) # fecha a planilha do excel

"""
     descarrega trem na pilha
"""
listaEventos = [] # lista de enventos

for trem in listaTrens:
    trem[0]