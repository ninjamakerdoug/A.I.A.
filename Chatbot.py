# -*- coding: utf-8 -*-

import json, time, os, sys, random
import subprocess as s
import numpy as np
#from pygame import mixer
import pandas as pd
from time import strftime
from datetime import datetime, timedelta
import pendulum as pl
from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt
from fpdf import FPDF


class Chatbot():
    def __init__(self, nome):
        try:
            memoria = open(nome+'.json','r')
        except FileNotFoundError:
            with open(nome+'.json','w') as memoria:
                memoria.write('[["Douglas"],{"tchau":"tchau","vendidos":{"data":[],"codigo":[],"item":[],"total_vendas":[]},"card_items":{"codigo":[],"item":[],"valor":[],"estoque":[]},"balanco":{"data":[],"num_mesa":[],"cartao":[],"dinheiro":[]},"abast_estoque":{"data":[],"item":[],"quantidade":[]}}]')
            memoria = open(nome+'.json','r')
        self.nome = nome
        self.conhecidos, self.frases = json.load(memoria)
        memoria.close()
        self.historico = [None,]



    def escuta(self,frase=None):
        if frase == None:
            frase = input('>: ')
        frase = str(frase)

        if 'executar ' in frase:
            return frase
        frase = frase.lower()
        #frase = frase.replace('é','eh')
        return frase



    def pensa(self,frase):
        for a in self.frases:
                if 'cnpj' in self.frases[a]:
                    self.nome_empresa = str(a)
                    self.cnpj = self.frases[a]['cnpj']
                    self.endereco = self.frases[a]['endereco']
                    self.bairro = self.frases[a]['bairro']
                    self.cidade = self.frases[a]['cidade']
                    self.tel = self.frases[a]['tel']

        with open('autorizados.json', 'r') as autorizados:
                    lista = json.loads(autorizados.read())
                    for i in lista:
                        if 'gerencia' in lista[i]:
                            self.c_gerencia = i
                        if 'garcom1' in lista[i]:
                            self.garcom_1 = i
                        if 'garcom2' in lista[i]:
                            self.garcom_2 = i
                        if 'garcom3' in lista[i]:
                            self.garcom_3 = i
                        if 'garcom4' in lista[i]:
                            self.garcom_4 = i
                        if 'garcom5' in lista[i]:
                            self.garcom_5 = i

        '''
        for b in self.frases[str(self.nome_empresa)]['ids']:
            if 'gerencia' in self.frases[str(self.nome_empresa)]['ids'][b]:
                self.c_gerencia = b
            if 'garcom1' in self.frases[str(self.nome_empresa)]['ids'][b]:
                self.garcom_1 = b
            if 'garcom2' in self.frases[str(self.nome_empresa)]['ids'][b]:
                self.garcom_2 = b
            if 'garcom3' in self.frases[str(self.nome_empresa)]['ids'][b]:
                self.garcom_3 = b
            if 'garcom4' in self.frases[str(self.nome_empresa)]['ids'][b]:
                self.garcom_4 = b
            if 'garcom5' in self.frases[str(self.nome_empresa)]['ids'][b]:
                self.garcom_5 = b
        '''

        lista = ['Em que posso ajudá-lo?','Pois não?','E aí, o que manda?']
        dataEhora = datetime.now()
        ano = str(dataEhora.year)
        mes = str(dataEhora.month)
        dia = str(dataEhora.day)
        hora_atual = str(strftime('%H'))
        hora_atual = int(hora_atual)
        minuto_atual = str(strftime('%M'))
        hora = str(strftime('%H:%M'))
        senha = 'doug777'
        ultimaFrase = self.historico[-1]
        saudacoes = ['oi','olá']
        
        #############################################
        
        if frase in saudacoes:
          return 'Olá, qual o seu nome?'
        if ultimaFrase == 'Olá, qual o seu nome?':
          nome = self.pegaNome(frase)
          frase = self.respondeNome(nome)
          return frase

        #############################################
        elif frase == '/abastecer':
          return 'Informe o código do produto'
        elif ultimaFrase == 'Informe o código do produto':
          if frase.isnumeric():
            if frase in self.frases['card_items']['codigo']:
              self.codg = frase
              list_card1 = {}
              for position, code in enumerate(self.frases['card_items']['codigo']):
                  list_card1[str(code)] = int(position)
              if str(self.codg) in list_card1:
                self.posicao_q = list_card1[self.codg]
              return 'Qual a quantidade que será abastecida?'
            else:
                return 'Valores informados inválidos!'
          else:
            return 'Valores informados inválidos!'
        elif ultimaFrase == 'Qual a quantidade que será abastecida?':
          if frase.isnumeric():
            qtdd = int(frase)
            estqe = self.frases['card_items']['estoque'][int(self.posicao_q)]
            if estqe == 'x':
              estqe = 0
            item = self.frases['card_items']['item'][int(self.posicao_q)]
            estoque_atual = int(estqe) + qtdd
            del self.frases['card_items']['estoque'][int(self.posicao_q)]
            self.frases['card_items']['estoque'].insert(int(self.posicao_q), estoque_atual)
            self.frases["abast_estoque"]["data"].append(f'{dia}/{mes}/{ano}')
            self.frases["abast_estoque"]["item"].append(f'{item}')
            self.frases["abast_estoque"]["quantidade"].append(f'{qtdd}')
            self.gravaMemoria()
            return f'Ítem {self.codg} abastecido'
          else:
            return 'Valores informados inválidos!'            


        elif frase == '/add_cardapio':
            return 'Qual será o código do item?'
        elif ultimaFrase == 'Qual será o código do item?':
            if frase.isnumeric():
                if frase in self.frases['card_items']['codigo']:
                    self.codigo = frase
                    return 'Este produto já está cadastrado, deseja alterá-lo?'
                else:
                    self.codigo = frase
                    return 'Qual é o ítem? Se possível, faça uma abreviação.'
            else:
                'Valores informados inválidos!'
        elif ultimaFrase == 'Este produto já está cadastrado, deseja alterá-lo?':
            frase = frase.lower()
            sims = ['sim','s']
            if frase in sims:
              self.alt = str(frase)
              list_card1 = {}
              for position, code in enumerate(self.frases['card_items']['codigo']):
                  list_card1[str(code)] = int(position)            
              if str(self.codigo) in list_card1:
                self.posicao = list_card1[self.codigo]
                del self.frases['card_items']['codigo'][int(list_card1[self.codigo])]
                del self.frases['card_items']['item'][int(list_card1[self.codigo])]
                del self.frases['card_items']['valor'][int(list_card1[self.codigo])]
                del self.frases['card_items']['estoque'][int(list_card1[self.codigo])]
                self.gravaMemoria()                
                return 'Qual é o ítem? Se possível, faça uma abreviação.'
                
            else:
                return 'Operação cancelada!'
        elif ultimaFrase == 'Qual é o ítem? Se possível, faça uma abreviação.':
            self.item = frase
            return 'Qual o valor?'
        elif ultimaFrase == 'Qual o valor?':
            if frase.isnumeric():
                self.valor = float(frase)
                return 'Qual é o estoque? (Digite qualquer letra caso não queira numerar o ítem)'
        elif ultimaFrase == 'Qual é o estoque? (Digite qualquer letra caso não queira numerar o ítem)':
            if frase.isnumeric():
              self.estoque = int(frase)
              try:
                if self.alt == 'sim' or self.alt == 's':
                  self.frases['card_items']['codigo'].insert(int(self.posicao), self.codigo)
                  self.frases['card_items']['item'].insert(int(self.posicao), self.item)
                  self.frases['card_items']['valor'].insert(int(self.posicao), self.valor)
                  self.frases['card_items']['estoque'].insert(int(self.posicao), self.estoque)
                  self.frases["abast_estoque"]["data"].append(f'{dia}/{mes}/{ano}')
                  self.frases["abast_estoque"]["item"].append(f'{self.item}')
                  self.frases["abast_estoque"]["quantidade"].append(f'{self.estoque}')
              except:
                self.frases['card_items']['codigo'].append(self.codigo)
                self.frases['card_items']['item'].append(self.item)
                self.frases['card_items']['valor'].append(self.valor)
                self.frases['card_items']['estoque'].append(self.estoque)
                self.frases["abast_estoque"]["data"].append(f'{dia}/{mes}/{ano}')
                self.frases["abast_estoque"]["item"].append(f'{self.item}')
                self.frases["abast_estoque"]["quantidade"].append(f'{self.estoque}')
              self.gravaMemoria()
              return 'Ítem salvo com sucesso!'
            else:
              self.estoque = 'x'
              try:
                if self.alt == 's' or self.alt == 'sim':
                  self.frases['card_items']['codigo'].insert(int(self.posicao), self.codigo)
                  self.frases['card_items']['item'].insert(int(self.posicao), self.item)
                  self.frases['card_items']['valor'].insert(int(self.posicao), self.valor)
                  self.frases['card_items']['estoque'].insert(int(self.posicao), self.estoque)
                  self.frases["abast_estoque"]["data"].append(f'{dia}/{mes}/{ano}')
                  self.frases["abast_estoque"]["item"].append(f'{self.item}')
                  self.frases["abast_estoque"]["quantidade"].append(f'{self.estoque}')
              except:
                self.frases['card_items']['codigo'].append(self.codigo)
                self.frases['card_items']['item'].append(self.item)
                self.frases['card_items']['valor'].append(self.valor)
                self.frases['card_items']['estoque'].append(self.estoque)
                self.frases["abast_estoque"]["data"].append(f'{dia}/{mes}/{ano}')
                self.frases["abast_estoque"]["item"].append(f'{self.item}')
                self.frases["abast_estoque"]["quantidade"].append(f'{self.estoque}')
              self.gravaMemoria()
              return 'Ítem salvo com sucesso!'

        elif frase == '/apg_cardapio':
            return 'Qual o código do ítem que será apagado?'
        elif ultimaFrase == 'Qual o código do ítem que será apagado?':
            list_card = {}
            for posicao, codigo in enumerate(self.frases['card_items']['codigo']):
              list_card[str(codigo)] = int(posicao)

            list_card2 = {}
            for posicao2, codigo2 in enumerate(self.frases['abast_estoque']['item']):
              list_card2[str(codigo2)] = int(posicao2)
            
            if str(frase) in list_card:
                apaga_item = str(self.frases['card_items']['item'][int(list_card[frase])])
                if str(apaga_item) in list_card2:
                  del self.frases["abast_estoque"]["data"][int(list_card2[apaga_item])]
                  del self.frases["abast_estoque"]["item"][int(list_card2[apaga_item])]
                  del self.frases["abast_estoque"]["quantidade"][int(list_card2[apaga_item])]

                del self.frases['card_items']['codigo'][int(list_card[frase])]
                del self.frases['card_items']['item'][int(list_card[frase])]
                del self.frases['card_items']['valor'][int(list_card[frase])]
                del self.frases['card_items']['estoque'][int(list_card[frase])]
                self.gravaMemoria()
                return f'Ítem {frase} apagado do cardápio!'
            else:
                return 'Valores informados inválidos!'
            

        elif frase == '/cardapio':
            def add_row(bold_1,text_1,bold_2,text_2):
                        pdf.set_font('arial','',12)
                        pdf.cell(22,10,bold_1,0,0)

                        pdf.set_font('arial','',12)
                        pdf.cell(71,10,text_1,0,0,align='C')

                        pdf.set_font('arial','',12)
                        pdf.cell(41,10,bold_2,0,0)

                        pdf.set_font('arial','',12)
                        pdf.cell(41,10,text_2,0,0,align='C')

                        pdf.cell(60,5,'',0,1)
                        pdf.cell(60,5,'',0,1)


            def add_row2(bold_1,text_1,bold_2,text_2):
                        pdf.set_font('arial','B',12)
                        pdf.cell(22,10,bold_1,0,0)

                        pdf.set_font('arial','B',12)
                        pdf.cell(71,10,text_1,0,0,align='C')

                        pdf.set_font('arial','B',12)
                        pdf.cell(41,10,bold_2,0,0)

                        pdf.set_font('arial','B',12)
                        pdf.cell(41,10,text_2,0,0,align='C')

                        pdf.cell(60,5,'',0,1)
                        pdf.cell(60,5,'',0,1)


            largura = 210 #mm
            altura = 297 #mm
            margem = 10 #mm

            pdf = FPDF('P','mm','A4')
            pdf.add_page()
            pdf.set_font('arial','B',18)
            pdf.set_auto_page_break(auto=bool,margin=margem)

            df = pd.DataFrame(self.frases['card_items'])
            df = df.sort_values(by=['codigo'],ascending=[True])
            maximo = len(self.frases['card_items']['codigo'])

            js = df.to_dict()
            pdf.cell(60,5,'',0,1)
            add_row2('CÓDIGO','ÍTEM','VALOR','ESTOQUE')
            pdf.cell(60,5,'',0,1)
            pdf.cell(60,5,'',0,1)
           
            contando = 0

            while True:
                if int(contando) == int(maximo):
                    break
                else:
                    if contando in js['codigo']:
                        codigo = js['codigo'][int(contando)]
                        item = js['item'][int(contando)]
                        valor = js['valor'][int(contando)]
                        estoque = js['estoque'][int(contando)]
                        add_row(f'  {codigo}',f'{item}',f'  {valor:.2f}',f'{estoque}')
                    else:
                        pass
                    contando += 1

            pdf.output('cardapio.pdf')
            return 'Cardápio!'
        
        #########################################################

        elif frase == '/transferir_mesa':
          return 'Digite conforme o exemplo:\n\n2 p 10\n\nO primeiro número refere-se ao número da mesa e o segundo número refere-se a transferência.'
        elif ultimaFrase == 'Digite conforme o exemplo:\n\n2 p 10\n\nO primeiro número refere-se ao número da mesa e o segundo número refere-se a transferência.':
          transferir_mesa = frase.split()
          mesa = transferir_mesa[0]
          mesa2 = transferir_mesa[2]
          if transferir_mesa[1].rstrip().lstrip() == 'p':
            if mesa.isnumeric():
              if mesa in self.frases:
                if 'responsavel' in self.frases[mesa]:
                  if mesa2.isnumeric():
                    if mesa2 in self.frases:
                      if 'responsavel' in self.frases[mesa2]:
                        return f'A mesa {mesa2} está ocupada.'
                    else:
                      self.chave = mesa2
                      self.frases[mesa]['mesa'] = str(self.chave)
                      resp = self.frases[mesa]
                      self.frases[self.chave] = resp
                      del self.frases[mesa]
                      self.gravaMemoria()
                      return f'Mesa {mesa} transferida para mesa {mesa2}!'              

        ###########################################################

        elif frase == '/mesas_abertas':
            try:
                def add_row(bold_1,text_1,bold_2,text_2):
                        pdf.set_font('arial','B',12)
                        pdf.cell(22,10,bold_1,0,0)

                        pdf.set_font('arial','',12)
                        pdf.cell(71,10,text_1,0,0,align='C')

                        pdf.set_font('arial','B',12)
                        pdf.cell(41,10,bold_2,0,0)

                        pdf.set_font('arial','',12)
                        pdf.cell(41,10,text_2,0,0,align='C')

                        pdf.cell(60,5,'',0,1)
                        pdf.cell(60,5,'',0,1)


                largura = 210 #mm
                altura = 297 #mm
                margem = 10 #mm

                pdf = FPDF('P','mm','A4')
                pdf.add_page()
                pdf.set_font('arial','B',18)
                pdf.set_auto_page_break(auto=bool,margin=margem)

                mesa = []
                for i in self.frases:
                    if i.isnumeric():
                        if 'responsavel' in self.frases[i]:
                            mesa.append(self.frases[i])
                df = pd.DataFrame(mesa)
                df = df[['mesa','total']]

                df1 = df.sort_values(by='mesa',ascending=True)
                df1 = df1.copy()


                df1 = df1.sort_values(by=['mesa'],ascending=[True])

                js = df1.to_dict()
                pdf.cell(60,5,'',0,1)
                pdf.cell(60,5,'',0,1)
            
                maximo = len(js['mesa'])
           
                contando = 0

                while True:
                    if int(contando) == int(maximo):
                        break
                    else:
                        if contando in js['mesa']:
                            mesa = js['mesa'][int(contando)]
                            total = float(js['total'][int(contando)])
                            add_row('Mesa:',f'{mesa}','Total:',f'{total:.2f}')
                        else:
                            pass
                        contando += 1

                pdf.output('mesas abertas.pdf')
                return f'Mesas abertas!'

            except KeyError:
                return 'Nenhuma mesa aberta.'

        ###########################################################

        elif frase == '/novo_cliente':
            return 'Qual será a mesa?'
        elif ultimaFrase == 'Qual será a mesa?':
            if frase.isnumeric():
                    if frase in self.frases:
                        self.mesa = frase
                        return 'Esta mesa já está ocupada, deseja alterá-la?'
                    else:
                        self.mesa = frase
                        return 'Qual o nome do responsável pela mesa?'
            else:
                'Valores informados inválidos!'
        elif ultimaFrase == 'Esta mesa já está ocupada, deseja alterá-la?':
            frase = frase.lower()
            sims = ['sim','s']
            if frase in sims:
                return 'Qual o nome do responsável pela mesa?'
            else:
                return 'Operação cancelada!'
        elif ultimaFrase == 'Qual o nome do responsável pela mesa?':
            self.responsavel = frase
            self.total = 0
            self.frases[self.mesa] = {"mesa":str(self.mesa),"responsavel":str(self.responsavel),"consumo": {"item":[],"qtd":[],"valor_venda":[]},"total":0}
            self.gravaMemoria()
            return 'Mesa cadastrada com sucesso!'

        ##################################################

        elif frase == '/venda' or frase == '/canc_venda':
            self.comando = frase
            if self.comando == '/canc_venda':
                return 'Quem fez a venda? Digite:\n\n1 para Garçom 1\n2 para Garçom 2\n3 para Garçom 3\n4 para Garçom 4\n5 para Garçom 5\n6 para Balcão'
            else:
                return 'Qual o número da mesa?'
        elif ultimaFrase == 'Quem fez a venda? Digite:\n\n1 para Garçom 1\n2 para Garçom 2\n3 para Garçom 3\n4 para Garçom 4\n5 para Garçom 5\n6 para Balcão':
            if frase == '1':
                self.desconta = self.garcom_1
            if frase == '2':
                self.desconta = self.garcom_2
            if frase == '3':
                self.desconta = self.garcom_3
            if frase == '4':
                self.desconta = self.garcom_4
            if frase == '5':
                self.desconta = self.garcom_5
            if frase == '6':
                self.desconta = self.c_gerencia
            return 'Qual o número da mesa?'

        elif ultimaFrase == 'Qual o número da mesa?':
            if frase.isnumeric():
                    if frase in self.frases:
                        self.mesa = frase
                        return 'Qual o código do ítem?'
                    else:
                        self.mesa = frase
                        return 'Não há cadastro nessa mesa'
            else:
                'Valores informados inválidos!'
        elif ultimaFrase == 'Qual o código do ítem?':
            list_card = {}
            for posicao, codigo in enumerate(self.frases['card_items']['codigo']):
              list_card[str(codigo)] = int(posicao)
  
            if str(frase) in list_card:
                self.codigo = self.frases['card_items']['codigo'][int(list_card[frase])]
                self.item = self.frases['card_items']['item'][int(list_card[frase])]
                self.valor = self.frases['card_items']['valor'][int(list_card[frase])]
                self.estoque = self.frases['card_items']['estoque'][int(list_card[frase])]
                return 'Quantidade?'
            else:
                return 'Ítem não encontrado!'
        
        elif ultimaFrase == 'Quantidade?':
            if frase.isnumeric():
                self.quantidade = int(frase)
                self.valor_venda = float(self.valor) * self.quantidade

                soma = self.frases[self.mesa]['total']
     
                if self.comando == '/canc_venda':
                  try:         
                    self.atualiza_estoque = self.estoque+self.quantidade
                    self.estoque = self.atualiza_estoque
                  except:
                    self.atualiza_estoque = 'x'
                  
                  self.total = soma - self.valor_venda
                  self.frases[self.mesa]['consumo']['item'].remove(self.item)
                  self.frases[self.mesa]['consumo']['qtd'].remove(self.quantidade)
                  self.frases[self.mesa]['consumo']['valor_venda'].remove(self.valor_venda)


                
                  if f'{dia}/{mes}/{ano}' in self.frases[self.nome_empresa]['ids'][str(self.desconta)]['data'][-1]:
                    ranking = float(self.frases[self.nome_empresa]['ids'][str(self.desconta)]['total'][-1])
                    self.total_ranking = ranking - float(self.valor_venda)
                    self.frases[self.nome_empresa]['ids'][str(self.desconta)]['total'][-1] = float(self.total_ranking)

                  self.frases['vendidos']['data'].remove(f'{dia}/{mes}/{ano}')
                  self.frases['vendidos']['codigo'].remove(self.codigo)
                  self.frases['vendidos']['item'].remove(self.item)
                  self.frases['vendidos']['total_vendas'].remove(self.quantidade)

                elif self.comando == '/venda':
                  if self.estoque == 'x':
                    self.atualiza_estoque = 'x'
                  else:                  
                    self.atualiza_estoque = self.estoque-self.quantidade
                  self.estoque = self.atualiza_estoque

                  self.total = soma + self.valor_venda
                  self.frases[self.mesa]['consumo']['item'].append(self.item)
                  self.frases[self.mesa]['consumo']['qtd'].append(self.quantidade)
                  self.frases[self.mesa]['consumo']['valor_venda'].append(self.valor_venda)

                  self.frases['vendidos']['data'].append(f'{dia}/{mes}/{ano}')
                  self.frases['vendidos']['codigo'].append(self.codigo)
                  self.frases['vendidos']['item'].append(self.item)
                  self.frases['vendidos']['total_vendas'].append(self.quantidade)
                  
                  if f'{dia}/{mes}/{ano}' in self.frases[str(self.nome_empresa)]['ids'][str(self.c_gerencia)]['data'][-1]:
                    self.total_ranking = float(self.frases[str(self.nome_empresa)]['ids'][str(self.c_gerencia)]['total'][-1]) + self.valor_venda
                    self.frases[str(self.nome_empresa)]['ids'][str(self.c_gerencia)]['total'][-1] = float(self.total_ranking)
                  else:
                    if f'{dia}/{mes}/{ano}' not in self.frases[str(self.nome_empresa)]['ids'][str(self.garcom_1)]['data'][-1]:
                        self.frases[str(self.nome_empresa)]['ids'][str(self.garcom_1)]['id'].append(str(self.garcom_1))
                        self.frases[str(self.nome_empresa)]['ids'][str(self.garcom_1)]['data'].append(f'{dia}/{mes}/{ano}')
                        self.frases[str(self.nome_empresa)]['ids'][str(self.garcom_1)]['total'].append(0)
                    if f'{dia}/{mes}/{ano}' not in self.frases[str(self.nome_empresa)]['ids'][str(self.garcom_2)]['data'][-1]:
                        self.frases[str(self.nome_empresa)]['ids'][str(self.garcom_2)]['id'].append(str(self.garcom_2))
                        self.frases[str(self.nome_empresa)]['ids'][str(self.garcom_2)]['data'].append(f'{dia}/{mes}/{ano}')
                        self.frases[str(self.nome_empresa)]['ids'][str(self.garcom_2)]['total'].append(0)
                    if f'{dia}/{mes}/{ano}' not in self.frases[str(self.nome_empresa)]['ids'][str(self.garcom_3)]['data'][-1]:
                        self.frases[str(self.nome_empresa)]['ids'][str(self.garcom_3)]['id'].append(str(self.garcom_3))
                        self.frases[str(self.nome_empresa)]['ids'][str(self.garcom_3)]['data'].append(f'{dia}/{mes}/{ano}')
                        self.frases[str(self.nome_empresa)]['ids'][str(self.garcom_3)]['total'].append(0)
                    if f'{dia}/{mes}/{ano}' not in self.frases[str(self.nome_empresa)]['ids'][str(self.garcom_4)]['data'][-1]:
                        self.frases[str(self.nome_empresa)]['ids'][str(self.garcom_4)]['id'].append(str(self.garcom_4))
                        self.frases[str(self.nome_empresa)]['ids'][str(self.garcom_4)]['data'].append(f'{dia}/{mes}/{ano}')
                        self.frases[str(self.nome_empresa)]['ids'][str(self.garcom_4)]['total'].append(0)
                    if f'{dia}/{mes}/{ano}' not in self.frases[str(self.nome_empresa)]['ids'][str(self.garcom_5)]['data'][-1]:
                        self.frases[str(self.nome_empresa)]['ids'][str(self.garcom_5)]['id'].append(str(self.garcom_5))
                        self.frases[str(self.nome_empresa)]['ids'][str(self.garcom_5)]['data'].append(f'{dia}/{mes}/{ano}')
                        self.frases[str(self.nome_empresa)]['ids'][str(self.garcom_5)]['total'].append(0)


                    self.frases[str(self.nome_empresa)]['ids'][str(self.c_gerencia)]['id'].append(str(self.c_gerencia))
                    self.frases[str(self.nome_empresa)]['ids'][str(self.c_gerencia)]['data'].append(f'{dia}/{mes}/{ano}')
                    self.frases[str(self.nome_empresa)]['ids'][str(self.c_gerencia)]['total'].append(float(self.valor_venda))


                list_card = {}
                for posicao, codigo in enumerate(self.frases['card_items']['codigo']):
                  list_card[str(codigo)] = int(posicao)            
            
                if str(self.codigo) in list_card:
                  if self.frases['card_items']['estoque'][int(list_card[self.codigo])] == 'x':
                    self.frases['card_items']['estoque'][int(list_card[self.codigo])] = 'x'
                  else:
                    self.frases['card_items']['estoque'][int(list_card[self.codigo])] = self.atualiza_estoque

                self.frases[self.mesa]['total'] = float(self.total)

                self.gravaMemoria()
                if self.comando == '/canc_venda':
                    return 'Venda cancelada!'
                if self.comando == '/venda':
                    pedido = f'Mesa: {self.mesa}\nPedido: {self.item}\nQuantidade: {self.quantidade}'
                    return f'{pedido}\n\nVenda realizada com sucesso'
            else:
                return 'Valores informados inválidos!'

        ###############################################

        elif frase == '/fechar_conta':
            return 'De qual mesa?'
        elif ultimaFrase == 'De qual mesa?':
            if frase in self.frases and frase.isnumeric():
                if 'total' in self.frases[frase]:
                    
                    def add_row2(bold_1,text_1,bold_2,text_2):
                        pdf.set_font('arial','B',12)
                        pdf.cell(22,10,bold_1,0,0)

                        pdf.set_font('arial','',12)
                        pdf.cell(75,10,text_1,0,0,align='C')

                        pdf.set_font('arial','B',12)
                        pdf.cell(21,10,bold_2,0,0)

                        pdf.set_font('arial','',12)
                        pdf.cell(75,10,text_2,0,0,align='C')
                        
                        pdf.cell(60,5,'',0,1)


                    def add_row(bold_1,text_1,bold_2,text_2,bold_3,text_3):
                        pdf.set_font('arial','B',12)
                        pdf.cell(22,10,bold_1,0,0)

                        pdf.set_font('arial','',12)
                        pdf.cell(41,10,text_1,0,0,align='C')

                        pdf.set_font('arial','B',12)
                        pdf.cell(21,10,bold_2,0,0)

                        pdf.set_font('arial','',12)
                        pdf.cell(41,10,text_2,0,0,align='C')

                        pdf.set_font('arial','B',12)
                        pdf.cell(21,10,bold_3,0,0)

                        pdf.set_font('arial','',12)
                        pdf.cell(41,10,text_3,0,0,align='C')
                        
                        pdf.cell(60,5,'',0,1)

                    
                    largura = 210 #mm
                    altura = 297 #mm
                    margem = 10 #mm

                    #########  Set Configuration do pdf   #########
                    pdf = FPDF('P','mm','A4')
                    pdf.add_page()
                    pdf.set_font('arial','B',18)
                    pdf.set_auto_page_break(auto=bool,margin=margem)
                    ##########  Inserir Titulo  ###################
                    company = ' A . I . A                            Artificial Intelligence Analyzes'
                    company_rodape = 'A.I.A.'
                    pdf.cell(largura-2*margem,60,f'{company}',border=0,ln=1,align='L')
                    
                    self.apaga_mesa = frase
                    
                    self.total = float(self.frases[self.apaga_mesa]["total"])
                    self.comissao = float(self.total / 10)
                    self.total_e_comissao = float(self.total + self.comissao)
                    pdf.cell(60,5,'',0,1)
                    add_row2('Mesa:',f'{self.apaga_mesa}','Responsável:',f'{self.frases[self.apaga_mesa]["responsavel"]}')
                    add_row2('Data:',f'{dia}/{mes}/{ano}_{hora_atual}:{minuto_atual}','Consumo:',f'R$ {self.total:.2f}')
                    add_row2('10% garçom (opcional):',f'R$ {self.comissao:.2f}','Total:',f'R$ {self.total_e_comissao:.2f}')
                    pdf.cell(60,5,'',0,1)
                    pdf.cell(60,5,'',0,1)

                    maximo = len(self.frases[self.apaga_mesa]['consumo']['item'])
                    contando = 0

                    while True:
                        if contando == int(maximo):
                            break
                        else:
                            item = self.frases[self.apaga_mesa]['consumo']['item'][int(contando)]
                            qtd = self.frases[self.apaga_mesa]['consumo']['qtd'][int(contando)]
                            consumo = self.frases[self.apaga_mesa]['consumo']['valor_venda'][int(contando)]
                            add_row('      Ítem:',f'{item}','Quantidade:',f'{qtd}','Venda:',f'R$ {consumo:.2f}')
                            contando += 1
                            

                    pdf.set_font('arial','',8)
                    now = datetime.now().strftime("%d-%m-%Y")
                    nota_rodape = f'{company_rodape}, Ciência de Dados | Conta fechada em {now} _ {hora_atual}:{minuto_atual}.'
                    pdf.text(x=largura - len(nota_rodape)*1.5 - margem,y=altura - margem/2,txt=nota_rodape)

                    ### Salvar o pdf ##################
                    try:
                        pdf.output('Contas/' + str(self.apaga_mesa) + ' ' + str(now) + '.pdf','F')
                        pass
                    except:
                        pass
                    pdf.output('conta.pdf','F')

                    return 'Forma de pagamento: digite "c" para cartão, "d" para dinheiro, "e" para dividir.'
                else:
                  'Valores informados inválidos!'
            else:
              return 'Valores informados inválidos!'


        elif 'Forma de pagamento: digite "c" para cartão, "d" para dinheiro, "e" para dividir.' in str(ultimaFrase):
              if frase == 'c' or frase == 'd':
                self.pagamento = str(frase)
                return f'Confirma o fechamento da mesa {self.apaga_mesa}?'
              elif frase == 'e':
                self.pagamento = str(frase.lower()).lstrip().rstrip()
                return 'Dividindo o pagamento\nSe o total da conta for R$ 100,00 e será pago 70,00 em cartão e 30,00 em dinheiro, digite "70 + 30".\nO 1° valor refere- se ao cartão e o 2° em dinheiro. (Não esqueça dos espaços entre os números)'
              else:
                return 'Erro! Operação cancelada.'

        elif ultimaFrase == 'Dividindo o pagamento\nSe o total da conta for R$ 100,00 e será pago 70,00 em cartão e 30,00 em dinheiro, digite "70 + 30".\nO 1° valor refere- se ao cartão e o 2° em dinheiro. (Não esqueça dos espaços entre os números)':
          result = eval(frase)
          if float(result) == float(self.total):
            self.pag_div = str(frase)
            return f"Confirma o fechamento da mesa {self.apaga_mesa}?"
          elif float(result) == float(self.total_e_comissao):
            div = frase.split()
            tira_comissao = float(div[2]) - float(self.comissao)
            if float(tira_comissao) < 0:
              tira_comissao = float(div[0]) - float(self.comissao)
              self.pag_div = f'{tira_comissao} + {div[2]}'
              return f"Confirma o fechamento da mesa {self.apaga_mesa}?"
            else:
              self.pag_div = f'{div[0]} + {tira_comissao}'
              return f"Confirma o fechamento da mesa {self.apaga_mesa}?"
          else:
            return 'Valores inválidos. Operação cancelada!'

        elif "Confirma o fechamento da mesa " in str(ultimaFrase):
            sims = ['s','sim']
            if frase in sims:
                data = f'{dia}/{mes}/{ano}'
                mesa = self.apaga_mesa
                total = self.frases[self.apaga_mesa]['total']
                
                if self.pagamento == 'c':
                    self.frases['balanco']['cartao'].append(total)
                    self.frases['balanco']['dinheiro'].append(0)
                elif self.pagamento == 'd':
                    self.frases['balanco']['dinheiro'].append(total)
                    self.frases['balanco']['cartao'].append(0)
                elif self.pagamento == 'e':
                    pag = self.pag_div.split()
                    cart = pag[0].rstrip().lstrip()
                    din = pag[2].rstrip().lstrip()
                    self.frases['balanco']['dinheiro'].append(float(din))
                    self.frases['balanco']['cartao'].append(float(cart))
                            
                self.frases['balanco']['data'].append(data)
                self.frases['balanco']['num_mesa'].append(mesa)
                del self.frases[self.apaga_mesa]
                self.gravaMemoria()
                return f'Conta da mesa {self.apaga_mesa} fechada!'
            else:
                return 'Operação cancelada!'

        #######################################################

        elif frase == 'cadastrar empresa':
            return 'Digite a senha de administrador'

        elif ultimaFrase == 'Digite a senha de administrador':
            if frase == senha:
                return 'Digite o nome da empresa.'
            else:
                return 'Senha inválida'
        elif ultimaFrase == 'Digite o nome da empresa.':
            self.nome_empresa = str(frase)
            return 'Digite o CNPJ da empresa.'
        elif ultimaFrase == 'Digite o CNPJ da empresa.':
            if frase.isnumeric():
                self.cnpj = str(frase)
                return 'Digite o nome da rua e o número da empresa.'
            else:
                return 'Valores inválidos'
        elif ultimaFrase == 'Digite o nome da rua e o número da empresa.':
            self.endereco = str(frase)
            return 'Qual o bairro?'
        elif ultimaFrase == 'Qual o bairro?':
            self.bairro = str(frase)
            return 'Digite a cidade em seguida a sigla do estado. Ex:\n\nSão Paulo - SP'
        elif ultimaFrase == 'Digite a cidade em seguida a sigla do estado. Ex:\n\nSão Paulo - SP':
            self.cidade = str(frase)
            return 'Digite um contato da empresa.'
        elif ultimaFrase == 'Digite um contato da empresa.':
            self.tel = str(frase)
            return 'Digite o id da cozinha'
        elif ultimaFrase == 'Digite o id da cozinha':
            self.id_cozinha = str(frase)
            return 'Digite o id do barman'
        elif ultimaFrase == 'Digite o id do barman':
            self.id_barman = str(frase)
            return 'Digite o id da gerência'
        elif ultimaFrase == 'Digite o id da gerência':
            self.gerencia = str(frase)
            return 'Agora digite o id do garçom 1'
        elif ultimaFrase == 'Agora digite o id do garçom 1':
            self.garcom1 = str(frase)
            return 'O id do garçom 2'
        elif ultimaFrase == 'O id do garçom 2':
            self.garcom2 = str(frase)
            return 'Id do garçom 3'
        elif ultimaFrase == 'Id do garçom 3':
            self.garcom3 = str(frase)
            return 'Qual o id do garçom 4?'
        elif ultimaFrase == 'Qual o id do garçom 4?':
            self.garcom4 = str(frase)
            return 'Por último, digite o id do garçom 5'
        elif ultimaFrase == 'Por último, digite o id do garçom 5':
            self.garcom5 = str(frase)
            self.frases[self.nome_empresa] = {'nome':self.nome_empresa,'cnpj':self.cnpj,'endereco':self.endereco,'bairro':self.bairro,'cidade':self.cidade,'tel':self.tel,'id_cozinha':self.id_cozinha,'id_barman':self.id_barman,'ids':{self.gerencia:{'id':[str(self.gerencia)],'data':['0/0/0'],'total':[0]},self.garcom1:{'id':[str(self.garcom1)],'data':['0/0/0'],'total':[0]},self.garcom2:{'id':[str(self.garcom2)],'data':['0/0/0'],'total':[0]},self.garcom3:{'id':[str(self.garcom3)],'data':['0/0/0'],'total':[0]},self.garcom4:{'id':[str(self.garcom4)],'data':['0/0/0'],'total':[0]},self.garcom5:{'id':[str(self.garcom5)],'data':['0/0/0'],'total':[0]}}}
            self.gravaMemoria()

            lista = dict()
            lista[self.gerencia] = 'gerencia'
            lista[self.garcom1] = 'garcom1'
            lista[self.garcom2] = 'garcom2'
            lista[self.garcom3] = 'garcom3'
            lista[self.garcom4] = 'garcom4'
            lista[self.garcom5] = 'garcom5'
            open('autorizados.json','w').write(json.dumps(lista))
            return 'Cadastro Realizado com Sucesso!'


        ##############################################
        elif frase == 'teste':
          df = pd.DataFrame({'Data':['08/09','08/09','10/09','08/09','10/09'],'Fruit':['Apple','Apple','Apple','Banana','Banana'],'Sale': [300,100,200,80,350],'Lucro': [30,10,20,8,35]})

          df = pd.DataFrame(df.groupby(['Data','Fruit'])['Sale','Lucro'].sum())
          df = df.reset_index()
        
          fig = plt.figure(figsize=(9,5))
          ax = plt.subplot(111)
          ax.axis('off')
          ax.table(cellText=df.values, colLabels=df.columns, bbox=[0,0,1,1])
          plt.savefig('teste.jpg')
        
          return 'teste plot'

        #######################################################

        elif frase == '/relatorio':
          return 'Informe a data conforme o exemplo abaixo:\nPara um dia, ex: "9/7/2021"\nPara um mês, ex: "2/2021"'
        #elif ultimaFrase == 'Informe a data conforme o exemplo abaixo:\nPara um dia, ex: "9/7/2021"\nPara um mês, ex: "2/2021"':
        elif '/' in str(frase) and ultimaFrase == 'Informe a data conforme o exemplo abaixo:\nPara um dia, ex: "9/7/2021"\nPara um mês, ex: "2/2021"':
          
          def estq():
            df = pd.DataFrame(self.frases['card_items'])
            df1 = df.copy()
            maximo = len(self.frases['card_items']['codigo'])

            conte = 0            
            while True:
              e = str(df1.loc[conte, 'estoque'])
              if conte == (int(maximo) - 1):
                if e == 'x':
                  df1 = df1.drop(int(conte))
                  df1.sort_values(by='estoque', ascending = False)
                  df1 = df1.reset_index()
                  break
                else:
                  df1.sort_values(by='estoque', ascending = False)
                  df1 = df1.reset_index()
                  break
              else:
                if e == 'x':
                  df1 = df1.drop(int(conte))
                  conte += 1
                else:
                  conte += 1

            largura = 0.35
            plt.rcParams.update({'font.size':12})
            x = np.arange(len(df1.codigo))
            fig, ax = plt.subplots(figsize =(20, 15))
            estoque = ax.bar(x, df1.estoque, largura, label = 'Estoque')
            ax.set_title(f'{date}')
            ax.legend()
            #ax.set_ylim([0,120])
            ax.set_xticks(x)
            ax.set_xticklabels(df1.item, rotation=75)
            for i in estoque:
              h = i.get_height()
              ax.annotate('{}'.format(h),xy=(i.get_x()+i.get_width()/2,h),xytext=(0,3),textcoords='offset points',ha='center')
            plt.savefig('estoque.jpg')


          def analise():              
            largura = 0.35
            plt.rcParams.update({'font.size':12})
            x = np.arange(len(df.data))
            fig, ax = plt.subplots(figsize =(13, 10))
            di_nheiro = ax.bar(x - largura/2, df.dinheiro, largura, label = 'Dinheiro', color = 'lime')
            car_tao = ax.bar(x + largura/2, df.cartao, largura, label = 'Cartão', color = 'cyan')
            ax.set_title(f'{date}')
            ax.set_ylabel('Valor em R$')
            ax.legend()
            ax.set_xticks(x)
            ax.set_xticklabels(df.data, rotation=75)
            plt.savefig('grafico.jpg')
    

          def analise2():
            fig = plt.figure(figsize=(9,5))
            ax = plt.subplot(111)
            ax.axis('on')
            plt.title(f'{date}', fontsize=28, color='green')
            plt.bar(df.num_mesa, df.cartao, 0.4, label='Cartão', color='cyan')
            plt.bar(df.num_mesa, df.dinheiro, 0.2, label='Dinheiro', color='lime')
            plt.legend()
            plt.xticks(df.num_mesa)
            plt.ylabel('Valor em R$', fontsize=16)
            plt.xlabel('Número da Mesa', fontsize=16)
            plt.savefig('grafico.jpg')

          

          def analise3():
            largura = 0.35
            plt.rcParams.update({'font.size':12})
            x = np.arange(len(df3.data))
            fig, ax = plt.subplots(figsize =(20, 15))
            vendas = ax.bar(x, df3.total_vendas, largura, label = 'Total de Vendas', color = 'lime')
            ax.set_title(f'{date}')
            ax.legend()
            #ax.set_ylim([0,120])
            ax.set_xticks(x)
            ax.set_xticklabels(df3.item, rotation=75)
            for i in vendas:
              h = i.get_height()
              ax.annotate('{}'.format(h),xy=(i.get_x()+i.get_width()/2,h),xytext=(0,3),textcoords='offset points',ha='center')
            plt.savefig('+vendidos.jpg')


          def analise5():
            try:
                os.remove('+vendidos.jpg')
            except:
                pass
            largura = 0.35
            plt.rcParams.update({'font.size':12})
            x = np.arange(len(df4.codigo))
            fig, ax = plt.subplots(figsize =(20, 15))
            vendas = ax.bar(x, df4.total_vendas, largura, label = 'Total de Vendas', color = 'lime')
            ax.set_title(f'{date}')
            ax.legend()
            #ax.set_ylim([0,120]) 
            ax.set_xticks(x)
            ax.set_xticklabels(df4.item, rotation=75)
            for i in vendas:
              h = i.get_height()
              ax.annotate('{}'.format(h),xy=(i.get_x()+i.get_width()/2,h),xytext=(0,3),textcoords='offset points',ha='center')
            plt.savefig('+vendidos.jpg')


          def dtFrame2():
            fig = plt.figure(figsize=(5,5))
            ax = plt.subplot(111)
            ax.axis('off')
            ax.table(cellText=df7.values, colLabels=df7.columns, bbox=[0,0,1,1])
            plt.savefig('abastecimento.jpg')
            
            

          def dtFrame():
            fig = plt.figure(figsize=(5,5))
            ax = plt.subplot(111)
            ax.axis('off')
            ax.table(cellText=df.values, colLabels=df.columns, bbox=[0,0,1,1])
            plt.savefig('planilha.jpg')


          ##    >>>>>>>>>>>>

          def add_row(bold_1,text_1,bold_2,text_2):
            pdf.set_font('arial','B',12)
            pdf.cell(30,10,bold_1,0,0)

            pdf.set_font('arial','',12)
            pdf.cell(65,10,text_1,0,0,align='C')

            pdf.set_font('arial','B',12)
            pdf.cell(30,10,bold_2,0,0)

            pdf.set_font('arial','',12)
            pdf.cell(65,10,text_2,0,1,align='C')


          def add_row2(bold_1,text_1,bold_2,text_2,bold_3,text_3):
            pdf.set_font('arial','B',12)
            pdf.cell(22,10,bold_1,0,0)

            pdf.set_font('arial','',12)
            pdf.cell(41,10,text_1,0,0,align='C')

            pdf.set_font('arial','B',12)
            pdf.cell(21,10,bold_2,0,0)

            pdf.set_font('arial','',12)
            pdf.cell(41,10,text_2,0,0,align='C')

            pdf.set_font('arial','B',12)
            pdf.cell(21,10,bold_3,0,0)

            pdf.set_font('arial','',12)
            pdf.cell(41,10,text_3,0,1,align='C')


          def add_row3(bold_1,text_1,bold_2,text_2,bold_3,text_3):
            pdf.set_font('arial','B',12)
            pdf.cell(10,10,bold_1,0,0)

            pdf.set_font('arial','',12)
            pdf.cell(38,10,text_1,0,0,align='C')

            pdf.set_font('arial','B',12)
            pdf.cell(27,10,bold_2,0,0)

            pdf.set_font('arial','',12)
            pdf.cell(48,10,text_2,0,0,align='C')

            pdf.set_font('arial','B',12)
            pdf.cell(15,10,bold_3,0,0)

            pdf.set_font('arial','',12)
            pdf.cell(46,10,text_3,0,1,align='C')


          def ranking1():
            largura = 0.20
            plt.rcParams.update({'font.size':12})
            x = 1 #np.arange(len(df_gerencia.data))
            fig, ax = plt.subplots(figsize =(20, 12))
            
            total_g1 = df_garcom_1['total'].sum()
            total_g2 = df_garcom_2['total'].sum()
            total_g3 = df_garcom_3['total'].sum()
            total_g4 = df_garcom_4['total'].sum()
            total_g5 = df_garcom_5['total'].sum()
            total_g = df_gerencia['total'].sum()
            
            total_ranking_garcom_1 = ax.bar(x, total_g1, largura, label = 'Garçom 1', color = 'gray')
            total_ranking_garcom_2 = ax.bar(x + largura, total_g2, largura, label = 'Garçom 2', color = 'cyan')
            total_ranking_garcom_3 = ax.bar(x + largura*2, total_g3, largura, label = 'Garçom 3', color = 'lime')
            total_ranking_garcom_4 = ax.bar(x + largura*3, total_g4, largura, label = 'Garçom 4', color = 'pink')
            total_ranking_garcom_5 = ax.bar(x + largura*4, total_g5, largura, label = 'Garçom 5', color = 'orange')
            total_ranking_gerencia = ax.bar(x + largura*5, total_g, largura, label = 'Balcão', color = 'blue')
            ax.set_title(f'{date}')
            ax.legend()
            #ax.set_ylim([0,120])
            #ax.set_xticks(x)
            #ax.set_xticklabels(df_gerencia.data, rotation=75)
            for i in total_ranking_gerencia:
              h = i.get_height()
              ax.annotate('{}'.format(h),xy=(i.get_x()+i.get_width()/2,h),xytext=(0,3),textcoords='offset points',ha='center')
            for a in total_ranking_garcom_1:
              h = a.get_height()
              ax.annotate('{}'.format(h),xy=(a.get_x()+a.get_width()/2,h),xytext=(0,3),textcoords='offset points',ha='center')
            for b in total_ranking_garcom_2:
              h = b.get_height()
              ax.annotate('{}'.format(h),xy=(b.get_x()+b.get_width()/2,h),xytext=(0,3),textcoords='offset points',ha='center')
            for c in total_ranking_garcom_3:
              h = c.get_height()
              ax.annotate('{}'.format(h),xy=(c.get_x()+c.get_width()/2,h),xytext=(0,3),textcoords='offset points',ha='center')
            for d in total_ranking_garcom_4:
              h = d.get_height()
              ax.annotate('{}'.format(h),xy=(d.get_x()+d.get_width()/2,h),xytext=(0,3),textcoords='offset points',ha='center')
            for e in total_ranking_garcom_5:
              h = e.get_height()
              ax.annotate('{}'.format(h),xy=(e.get_x()+e.get_width()/2,h),xytext=(0,3),textcoords='offset points',ha='center')
            plt.savefig('ranking.jpg')




          def ranking2():
            largura = 0.20
            plt.rcParams.update({'font.size':12})
            x = np.arange(len(df_gerencia.data))
            fig, ax = plt.subplots(figsize =(20, 12))
            total_ranking_garcom_1 = ax.bar(x, df_garcom_1.total, largura, label = 'Garçom 1', color = 'gray')
            total_ranking_garcom_2 = ax.bar(x + largura, df_garcom_2.total, largura, label = 'Garçom 2', color = 'cyan')
            total_ranking_garcom_3 = ax.bar(x + largura*2, df_garcom_3.total, largura, label = 'Garçom 3', color = 'lime')
            total_ranking_garcom_4 = ax.bar(x + largura*3, df_garcom_4.total, largura, label = 'Garçom 4', color = 'pink')
            total_ranking_garcom_5 = ax.bar(x + largura*4, df_garcom_5.total, largura, label = 'Garçom 5', color = 'orange')
            total_ranking_gerencia = ax.bar(x + largura*5, df_gerencia.total, largura, label = 'Balcão', color = 'blue')
            ax.set_title(f'{date}')
            ax.legend()
            #ax.set_ylim([0,120])
            ax.set_xticks(x)
            ax.set_xticklabels(df_gerencia.data, rotation=75)
            for i in total_ranking_gerencia:
              h = i.get_height()
              ax.annotate('{}'.format(h),xy=(i.get_x()+i.get_width()/2,h),xytext=(0,3),textcoords='offset points',ha='center')
            for a in total_ranking_garcom_1:
              h = a.get_height()
              ax.annotate('{}'.format(h),xy=(a.get_x()+a.get_width()/2,h),xytext=(0,3),textcoords='offset points',ha='center')
            for b in total_ranking_garcom_2:
              h = b.get_height()
              ax.annotate('{}'.format(h),xy=(b.get_x()+b.get_width()/2,h),xytext=(0,3),textcoords='offset points',ha='center')
            for c in total_ranking_garcom_3:
              h = c.get_height()
              ax.annotate('{}'.format(h),xy=(c.get_x()+c.get_width()/2,h),xytext=(0,3),textcoords='offset points',ha='center')
            for d in total_ranking_garcom_4:
              h = d.get_height()
              ax.annotate('{}'.format(h),xy=(d.get_x()+d.get_width()/2,h),xytext=(0,3),textcoords='offset points',ha='center')
            for e in total_ranking_garcom_5:
              h = e.get_height()
              ax.annotate('{}'.format(h),xy=(e.get_x()+e.get_width()/2,h),xytext=(0,3),textcoords='offset points',ha='center')
            plt.savefig('ranking.jpg')



          date = str(frase)
          self.data_requirida = str(frase)
          mes_ou_dia = date.count('/')
          df = pd.DataFrame(self.frases['balanco'])
          maximo = len(self.frases['balanco']['data'])
          conte = 0

          while True:
              dt = str(df.loc[conte, 'data'])
              dt1 = dt.replace('/',' ').split()
              d = dt1[0]
              m = dt1[1]
              a = dt1[2]
              if conte == (int(maximo) - 1):
                if mes_ou_dia == 1:
                  if f'{m}/{a}' != date:
                    df = df.drop(int(conte))
                  df = pd.DataFrame(df.groupby(['data'])['dinheiro','cartao'].sum())
                  df = df.reset_index()
                  analise()
                  break
                else:
                  if f'{d}/{m}/{a}' != date:
                    df = df.drop(int(conte))
                  df = pd.DataFrame(df.groupby(['data','num_mesa'])['dinheiro','cartao'].sum())
                  df = df.reset_index()
                  analise2()
                  break
              else:
                if mes_ou_dia == 1:
                  if f'{m}/{a}' != date:
                    df = df.drop(int(conte))
                else:
                  if f'{d}/{m}/{a}' != date:
                    df = df.drop(int(conte))
                conte += 1



          df_gerencia = pd.DataFrame(self.frases[self.nome_empresa]['ids'][str(self.c_gerencia)])
          df_garcom_1 = pd.DataFrame(self.frases[self.nome_empresa]['ids'][str(self.garcom_1)])
          df_garcom_2 = pd.DataFrame(self.frases[self.nome_empresa]['ids'][str(self.garcom_2)])
          df_garcom_3 = pd.DataFrame(self.frases[self.nome_empresa]['ids'][str(self.garcom_3)])
          df_garcom_4 = pd.DataFrame(self.frases[self.nome_empresa]['ids'][str(self.garcom_4)])
          df_garcom_5 = pd.DataFrame(self.frases[self.nome_empresa]['ids'][str(self.garcom_5)])
          maximo_gerencia = len(self.frases[self.nome_empresa]['ids'][str(self.c_gerencia)]['data'])
          conte_gerencia = 0

          while True:
              dt = str(df_gerencia.loc[conte_gerencia, 'data'])
              dt1 = dt.replace('/',' ').split()
              d = dt1[0]
              m = dt1[1]
              a = dt1[2]
              if conte_gerencia == (int(maximo_gerencia) - 1):
                if mes_ou_dia == 1:
                  if f'{m}/{a}' != date:
                    df_gerencia = df_gerencia.drop(int(conte_gerencia))
                    df_garcom_1 = df_garcom_1.drop(int(conte_gerencia))
                    df_garcom_2 = df_garcom_2.drop(int(conte_gerencia))
                    df_garcom_3 = df_garcom_3.drop(int(conte_gerencia))
                    df_garcom_4 = df_garcom_4.drop(int(conte_gerencia))
                    df_garcom_5 = df_garcom_5.drop(int(conte_gerencia))

                  df_gerencia = pd.DataFrame(df_gerencia.groupby(['id'])['total'].sum())
                  df_garcom_1 = pd.DataFrame(df_garcom_1.groupby(['id'])['total'].sum())
                  df_garcom_2 = pd.DataFrame(df_garcom_2.groupby(['id'])['total'].sum())
                  df_garcom_3 = pd.DataFrame(df_garcom_3.groupby(['id'])['total'].sum())
                  df_garcom_4 = pd.DataFrame(df_garcom_4.groupby(['id'])['total'].sum())
                  df_garcom_5 = pd.DataFrame(df_garcom_5.groupby(['id'])['total'].sum())

                  df_gerencia = df_gerencia.reset_index()
                  df_garcom_1 = df_garcom_1.reset_index()
                  df_garcom_2 = df_garcom_2.reset_index()
                  df_garcom_3 = df_garcom_3.reset_index()
                  df_garcom_4 = df_garcom_4.reset_index()
                  df_garcom_5 = df_garcom_5.reset_index()
                  ranking1()
                  break
                else:
                  if f'{d}/{m}/{a}' != date:
                    df_gerencia = df_gerencia.drop(int(conte_gerencia))
                    df_garcom_1 = df_garcom_1.drop(int(conte_gerencia))
                    df_garcom_2 = df_garcom_2.drop(int(conte_gerencia))
                    df_garcom_3 = df_garcom_3.drop(int(conte_gerencia))
                    df_garcom_4 = df_garcom_4.drop(int(conte_gerencia))
                    df_garcom_5 = df_garcom_5.drop(int(conte_gerencia))

                  df_gerencia = df_gerencia.reset_index()
                  df_garcom_1 = df_garcom_1.reset_index()
                  df_garcom_2 = df_garcom_2.reset_index()
                  df_garcom_3 = df_garcom_3.reset_index()
                  df_garcom_4 = df_garcom_4.reset_index()
                  df_garcom_5 = df_garcom_5.reset_index()
                  ranking2()
                  break
              else:
                if mes_ou_dia == 1:
                  if f'{m}/{a}' != date:
                    df_gerencia = df_gerencia.drop(int(conte_gerencia))
                    df_garcom_1 = df_garcom_1.drop(int(conte_gerencia))
                    df_garcom_2 = df_garcom_2.drop(int(conte_gerencia))
                    df_garcom_3 = df_garcom_3.drop(int(conte_gerencia))
                    df_garcom_4 = df_garcom_4.drop(int(conte_gerencia))
                    df_garcom_5 = df_garcom_5.drop(int(conte_gerencia))
                else:
                  if f'{d}/{m}/{a}' != date:
                    df_gerencia = df_gerencia.drop(int(conte_gerencia))
                    df_garcom_1 = df_garcom_1.drop(int(conte_gerencia))
                    df_garcom_2 = df_garcom_2.drop(int(conte_gerencia))
                    df_garcom_3 = df_garcom_3.drop(int(conte_gerencia))
                    df_garcom_4 = df_garcom_4.drop(int(conte_gerencia))
                    df_garcom_5 = df_garcom_5.drop(int(conte_gerencia))
                conte_gerencia += 1


          df3 = pd.DataFrame(self.frases['vendidos'])
          maximo3 = len(self.frases['vendidos']['data'])
          conte3 = 0

          while True:
              dt3 = str(df3.loc[conte3, 'data'])
              dt4 = dt3.replace('/',' ').split()
              d3 = dt4[0]
              m3 = dt4[1]
              a3 = dt4[2]
              if conte3 == (int(maximo3) - 1):
                if mes_ou_dia == 1:
                  if f'{m3}/{a3}' != date:
                    df3 = df3.drop(int(conte3))
                  df3 = pd.DataFrame(df3.groupby(['data','codigo','item'])['total_vendas'].sum())
                  df3 = df3.reset_index()
                
                  df4 = df3.copy()
                  df4 = df4[['codigo','item','total_vendas']]
                  df4 = df4.reset_index()
                  df4 = pd.DataFrame(df4.groupby(['codigo','item'])['total_vendas'].sum())
                  df4 = df4.reset_index()                  
                  analise5()
                  break
                else:
                  if f'{d3}/{m3}/{a3}' != date:
                    df3 = df3.drop(int(conte3))
                  df3 = pd.DataFrame(df3.groupby(['data','codigo','item'])['total_vendas'].sum())
                  df3 = df3.reset_index()
                  analise3()
                  break
              else:
                if mes_ou_dia == 1:
                  if f'{m3}/{a3}' != date:
                    df3 = df3.drop(int(conte3))
                else:
                  if f'{d3}/{m3}/{a3}' != date:
                    df3 = df3.drop(int(conte3))
                conte3 += 1

          df7 = pd.DataFrame(self.frases['abast_estoque'])
          maximo7 = len(self.frases['abast_estoque']['data'])
          conte7 = 0

          while True:
              dt7 = str(df7.loc[conte7, 'data'])
              dt7 = dt7.replace('/',' ').split()
              d7 = dt7[0]
              m7 = dt7[1]
              a7 = dt7[2]
              if conte7 == (int(maximo7) - 1):
                if mes_ou_dia == 1:
                    if f'{m7}/{a7}' != date:
                        df7 = df7.drop(int(conte7))
                    df7 = pd.DataFrame(df7.groupby(['data','item'])['quantidade'].sum())
                    df7 = df7.reset_index()
                    #dtFrame2()
                    break

                else:
                  if f'{d7}/{m7}/{a7}' != date:
                    df7 = df7.drop(int(conte7))
                  df7 = pd.DataFrame(df7.groupby(['data','item'])['quantidade'].sum())
                  df7 = df7.reset_index()
                  break
              else:
                if mes_ou_dia == 1:
                  if f'{m7}/{a7}' != date:
                    df7 = df7.drop(int(conte7))
                else:
                  if f'{d7}/{m7}/{a7}' != date:
                    df7 = df7.drop(int(conte7))
                conte7 += 1      

          total_cartao = sum(df.cartao)
          total_dinheiro = sum(df.dinheiro)
          balanco_total = int(total_cartao) + int(total_dinheiro)
          dtFrame()
          estq()

          #########   CRIANDO UM PDF   ###########


          #Set Variables
          largura = 210 #mm
          altura = 297 #mm
          margem = 10 #mm

          ######### Set Configuration #########
          pdf = FPDF('P','mm','A4')
          pdf.add_page()
          pdf.set_font('arial','B',18)
          pdf.set_auto_page_break(auto=bool,margin=margem)

          ##### Colocar Cabeçalho e Rodapé ################
          pdf.image('cabecalho.jpg',x=0,y=0,w=largura)
          #pdf.image('rodape.jpg',x=0,y=altura-10,w=largura)

          ########## Inserir Titulo ###################
          company = ' AIA S.A.                            Artificial Intelligence Analyzes'
          company_rodape = 'AIA S.A.'
          pdf.cell(largura-2*margem,60,f'{company}',border=0,ln=1,align='L')
          pdf.cell(60,5,'',0,1)
          pdf.cell(60,5,'',0,1)
          pdf.cell(60,5,'',0,1)
          pdf.cell(60,5,'',0,1)

          ############### Secção Detalhes da Empresa ##############
          pdf.set_font('arial','BU',12)
          pdf.cell(60,10,'Detalhes da Empresa',0,1)

          #linha 1
          add_row('Nome:',f'{self.nome_empresa.title()}','CNPJ:',f'{self.cnpj}')

          #Linha 2
          add_row('Endereço:',f'{self.endereco.title()}','Bairro:',f'{self.bairro.title()}')

          #Linha 3
          add_row('Cidade:',f'{self.cidade.title()}','Tel:',f'{self.tel}')

          #quebra de linha
          pdf.cell(60,5,'',0,1)
          pdf.cell(60,5,'',0,1)

          ########### Secção Indicadores ######################
          pdf.set_font('arial','BU',12)
          pdf.cell(60,10,'Indicadores',0,1)

          #linha 1
          add_row('Data requirida:',f'{date}','Total em vendas:',f'R$ {balanco_total:.2f}')
          #Linha 2
          add_row('Cartão:',f'R$ {total_cartao:.2f}','Dinheiro:',f'R$ {total_dinheiro:.2f}')
          #linha 3
          #comissao = float(balanco_total) / 10
          #add_row('Total em vendas:',f'R$ {balanco_total:.2f}','Total em Comissão:',f'R$ {comissao:.2f}')

          #quebra de linha
          pdf.cell(60,5,'',0,1)

          ############ Grafico #################################
          pdf.set_font('arial','BU',12)
          pdf.cell(60,10,'Análise Gráfica das vendas na data requirida',0,1)
          img_path = 'grafico.jpg'
          pdf.image(img_path,x=pdf.get_x(),w=largura-2*margem,h=(altura-pdf.get_y()-2*margem))

          pdf.cell(60,5,'',0,1)
          pdf.cell(60,5,'',0,1)

          pdf.set_font('arial','BU',14)
          pdf.cell(60,10,'Dados das vendas na data requirida',0,1)      
          
          pdf.cell(60,5,'',0,1)
          pdf.cell(60,5,'',0,1)

          
          try:
            if mes_ou_dia == 1:
                img_path = 'planilha.jpg'
                pdf.image(img_path,x=pdf.get_x(),w=largura-2,h=(altura-pdf.get_y()-2*margem))
            else:
                conte_8 = 0
                while True:
                    f_num_mesa = str(df.loc[int(conte_8), 'num_mesa'])
                    f_cartao = float(df.loc[int(conte_8), 'cartao'])
                    f_cartao = f'{f_cartao:.2f}'
                    f_dinheiro = float(df.loc[int(conte_8), 'dinheiro'])
                    f_dinheiro = f'{f_dinheiro:.2f}'
                    add_row2('      Mesa:',f_num_mesa,'Cartão:',f_cartao,'Dinheiro:',f_dinheiro)
                    conte_8 += 1
          except KeyError:
            pass

          if mes_ou_dia == 2:
              img_path = 'branco.png'
              pdf.image(img_path,x=pdf.get_x(),w=largura-2,h=(altura-pdf.get_y()-2*margem))

          pdf.cell(60,5,'',0,1)
          pdf.cell(60,5,'',0,1)

          pdf.set_font('arial','BU',14)
          pdf.cell(60,10,'Análise gráfica do ranking de vendas na data requirida',0,1)
          img_path = 'ranking.jpg'
          pdf.image(img_path,x=pdf.get_x(),w=largura-2*margem,h=120)   #(altura-pdf.get_y()-2*margem))

          pdf.cell(60,5,'',0,1)
          pdf.cell(60,5,'',0,1)

          pdf.set_font('arial','BU',14)
          pdf.cell(60,10,'Dados do ranking de vendas na data requirida',0,1)
          pdf.cell(60,5,'',0,1)
          pdf.cell(60,5,'',0,1)

          add_row3('    ID:',f'Garçom 1','Total em vendas:',f'R$ {float(df_garcom_1.total):.2f}','Comissão:',f'R$ {float(df_garcom_1.total)/10:.2f}')
          add_row3('    ID:',f'Garçom 2','Total em vendas:',f'R$ {float(df_garcom_2.total):.2f}','Comissão:',f'R$ {float(df_garcom_2.total)/10:.2f}')
          add_row3('    ID:',f'Garçom 3','Total em vendas:',f'R$ {float(df_garcom_3.total):.2f}','Comissão:',f'R$ {float(df_garcom_3.total)/10:.2f}')
          add_row3('    ID:',f'Garçom 4','Total em vendas:',f'R$ {float(df_garcom_4.total):.2f}','Comissão:',f'R$ {float(df_garcom_4.total)/10:.2f}')
          add_row3('    ID:',f'Garçom 5','Total em vendas:',f'R$ {float(df_garcom_5.total):.2f}','Comissão:',f'R$ {float(df_garcom_5.total)/10:.2f}')
          pdf.cell(60,5,'',0,1)
          pdf.cell(60,5,'',0,1)
          add_row('     ID:',f'Balcão','Total em vendas:',f'R$ {float(df_gerencia.total):.2f}')
          pdf.cell(60,5,'',0,1)
          pdf.cell(60,5,'',0,1)
          total = float(float(df_garcom_1.total) + float(df_garcom_2.total) + float(df_garcom_3.total) + float(df_garcom_4.total) + float(df_garcom_5.total))
          comissao = float(total / 10)
          add_row('     Total vendido pelos garçoms:','','',f'R$ {total:.2f}')
          add_row('     Total em comissão:','','',f'R$ {comissao:.2f}')
          pdf.image('branco.png',x=pdf.get_x(),w=largura-2*margem,h=(altura-pdf.get_y()-2*margem))
          pdf.cell(60,5,'',0,1)
          pdf.cell(60,5,'',0,1)
          pdf.set_font('arial','BU',12)
          pdf.cell(60,10,'Análise Gráfica dos ítens vendidos na data requirida',0,1)
          pdf.image('+vendidos.jpg',x=pdf.get_x(),w=largura-2*margem,h=120)

          pdf.cell(60,5,'',0,1)

          pdf.set_font('arial','BU',12)
          pdf.cell(60,10,'Análise Gráfica do Estoque na data requirida',0,1)
          pdf.image('estoque.jpg',x=pdf.get_x(),w=largura-2*margem,h=(altura-pdf.get_y()-2*margem))

          pdf.cell(60,5,'',0,1)
          pdf.cell(60,5,'',0,1)

          pdf.set_font('arial','BU',12)
          pdf.cell(60,10,'Dados do abastecimento na data requirida',0,1)
          if mes_ou_dia == 1:
            try:
                pdf.cell(60,5,'',0,1)
                pdf.cell(60,5,'',0,1)
                self.conte_9 = 0
                while True:
                    f_data = str(df7.loc[int(self.conte_9), 'data'])
                    f_item = str(df7.loc[int(self.conte_9), 'item'])
                    f_quantidade = str(df7.loc[int(self.conte_9), 'quantidade'])
                    add_row2('      Data:',f'{f_data}','Ítem:',f'{f_item}','Qtd. Abastecida:',f'{f_quantidade}')
                    self.conte_9 += 1
            except KeyError:
                if self.conte_9 == 0:
                    pdf.cell(60,5,'',0,1)
                    pdf.cell(60,5,'',0,1)
                    pdf.set_font('arial','',12)
                    pdf.cell(60,10,'     Não houve abastecimento nessa data',0,1)
                else:
                    pass
          else:
            try:
                pdf.set_font('arial','',12)
                pdf.cell(60,5,'',0,1)
                self.conte_7 = 0
                while True:
                    f_item = str(df7.loc[self.conte_7, 'item'])
                    f_abast = str(df7.loc[self.conte_7, 'quantidade'])
                    add_row('     Ítem:',f'{f_item}','Qtd. Abastecida:',f'{f_abast}')
                    if self.conte_7 == (int(maximo7) - 1):
                        pdf.image('branco.png',x=pdf.get_x(),w=largura-2*margem,h=(altura-pdf.get_y()-2*margem))
                        break
                    else:
                        self.conte_7 += 1
            except KeyError:
                if self.conte_7 == 0:
                    pdf.cell(60,5,'',0,1)
                    pdf.cell(60,5,'',0,1)
                    pdf.set_font('arial','',12)
                    pdf.cell(60,10,'     Não houve abastecimento nessa data',0,1)
                else:
                    pass

          ### Rodapé #########################

          pdf.set_font('arial','',8)
          now = datetime.now().strftime("%d-%m-%Y")
          #if int(hora_atual) >= 3:
            #hora_atual = int(hora_atual) - 3
          nota_rodape = f'{company_rodape} Ciência de Dados | Relatório gerado em {now} _ {hora_atual}:{minuto_atual}.'
          pdf.text(x=largura - len(nota_rodape)*1.5 - margem,y=altura - margem/2,txt=nota_rodape)

          ### Salvar o pdf ##################
          data_pdf = f'{dia}/{mes}/{ano}'
          mes_pdf = f'{mes}/{ano}'
          if str(self.data_requirida) == str(data_pdf):
            pdf.output('Relatorios/' + str(data_pdf).replace('/','-') + '.pdf','F')
          if str(self.data_requirida) == str(mes_pdf):
            pdf.output('Relatorios/' + str(mes_pdf).replace('/','-') + '.pdf','F')

          pdf.output('Relatorio_Analise.pdf','F')


          #return f'Balanceamento de {date}\n\nCartão: R$ {total_cartao},00\nDinheiro: R$ {total_dinheiro},00\nTOTAL: R$ {balanco_total},00'
          return 'Balanceamento'
        ##############################################

        elif str(frase) in self.frases['card_items']['codigo']:
            list_card4 = {}
            for posicao4, codigo4 in enumerate(self.frases['card_items']['codigo']):
              list_card4[str(codigo4)] = int(posicao4)

            if frase in list_card4:
              codigo = str(frase)
              item = self.frases['card_items']['item'][int(list_card4[frase])]
              valor = str(self.frases['card_items']['valor'][int(list_card4[frase])])
              estoque = str(self.frases['card_items']['estoque'][int(list_card4[frase])])
              return f'Código: {codigo}\nÍtem: {item}\nValor Unid.: R$ {valor}\nEstoque: {estoque}'
        
        ############################################

        try:
            resp = str(eval(frase))
            return resp
        except:
            return 'Não entendi'



    def pegaNome(self,nome):
        if 'o meu nome eh ' in nome:
            nome = nome[500:]
        nome = nome
        return nome



    def respondeNome(self,nome):
        if nome in self.conhecidos:
            frase = f'Eaew {nome}'
        else:
            frase = f'Muito prazer {nome}.'
            self.conhecidos.append(nome)
            self.gravaMemoria()
        return frase



    def gravaMemoria(self):
        memoria = open(self.nome+'.json','w')
        json.dump([self.conhecidos,self.frases],memoria)
        memoria.close()



    def fala(self,frase):
        if 'executar' in frase:
            plataforma = sys.platform
            comando = frase.replace('executar ','')
            if 'win' in plataforma:
                os.startfile(comando)
            else:
                try:
                    s.Popen(comando.lower())
                except FileNotFoundError:
                    s.Popen(['xdg-open',comando])                
        self.historico.append(frase)
        os.system('clear')
        
