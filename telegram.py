# -*- coding: utf-8 -*-

import json
from Chatbot import Chatbot
import telepot
from datetime import datetime
from time import strftime
import time
import pandas as pd
import matplotlib.pyplot as plt
import os
import shutil


caminho_original = '/home/ninjamaker/python/IAD/Relatorios/'
caminho_novo = '/home/ninjamaker/python/IAD/'

telegram = telepot.Bot('1761777816:AAHkc7FKpr__wK8LkF9krPe4DgCuNVkDQFE')
bot = Chatbot("TESTE_bot2")

mesa = ''
mesa_codigo = ''
mesa_item = ''
mesa_valor = ''
mesa_estoque = ''

mesa_quantidade = ''
mesa_valor_venda = ''
mesa_soma = ''
mesa_atualiza_estoque = ''
mesa_total = ''

#id dos cadastrados
garcom1 = ''
garcom2 = ''
garcom3 = ''
garcom4 = ''
garcom5 = ''
cozinha = ''
barman = ''
gerencia = ''
administrador = "1622306967"
#garcom_teste = "1090587812"

empresa = ''

doc_relatorio = ''
ultima_frase_cadastro = 'Digite o número da mesa e o nome do responsável por ela conforme o exemplo:\n\n1 joao'
ultima_frase_venda = 'Digite o número da mesa, depois o código do produto, e por último a quantidade. Segue o exemplo:\n\n3 02 2\n\n3=Mesa || 02=Cód. || 2=Qtd'
informe_data = ''
ultima_frase_garcom1 = ''
ultima_frase_garcom2 = ''
ultima_frase_garcom3 = ''
ultima_frase_garcom4 = ''
ultima_frase_garcom5 = ''
ultima_frase_gerencia = ''

dataEhora = datetime.now()
ano = str(dataEhora.year)
mes = str(dataEhora.month)
dia = str(dataEhora.day)


def pegaHorario():
    horaAtual = datetime.now().time().hour
    minutoAtual = datetime.now().time().minute
    segundoAtual = datetime.now().time().second

    if (horaAtual == 14) and (minutoAtual == 20):
        return True    


def recebendoMsg(msg):

        #global ultima_frase
        global caminho_original
        global caminho_novo
        global garcom1
        global garcom2
        global garcom3
        global garcom4
        global garcom5
        global cozinha
        global barman
        global mesa
        global mesa_codigo
        global mesa_item
        global mesa_valor
        global mesa_estoque
        global mesa_quantidade
        global mesa_valor_venda
        global mesa_atualiza_estoque
        global mesa_soma
        global mesa_total
        global gerencia
        global doc_relatorio
        global dia
        global mes
        global ano
        global ultima_frase_cadastro
        global ultima_frase_venda
        global ultima_frase_garcom1
        global ultima_frase_garcom2
        global ultima_frase_garcom3
        global ultima_frase_garcom4
        global ultima_frase_garcom5
        global ultima_frase_gerencia
        global informe_data
        global administrador
        global empresa

        try:
            primeiro_nome = msg['chat']['first_name']
        except:
            pass
        mensagem = msg['text'].lower()
        chatID = msg['chat']['id']
        tipoMsg, tipoChat, chatID = telepot.glance(msg)



        if mensagem.lower() == 'meu id':
          telegram.sendMessage(chatID, str(chatID))
        else:
          #frase = bot.escuta(frase=mensagem)
          chatID = str(chatID)
        

          for i in bot.frases:
            if 'cnpj' in bot.frases[str(i)]:
                empresa = str(i)     
                cozinha = bot.frases[str(empresa)]['id_cozinha']
                barman = bot.frases[str(empresa)]['id_barman']

          lista = ''
          
          with open('autorizados.json', 'r') as autorizados:
                    lista = json.loads(autorizados.read())
                    for i in lista:
                        if 'gerencia' in lista[i]:
                            gerencia = i
                        if 'garcom1' in lista[i]:
                            garcom1 = i
                        if 'garcom2' in lista[i]:
                            garcom2 = i
                        if 'garcom3' in lista[i]:
                            garcom3 = i
                        if 'garcom4' in lista[i]:
                            garcom4 = i
                        if 'garcom5' in lista[i]:
                            garcom5 = i


                        ######################################
                        #with open('autorizados.txt','r') as autorizados:
                            #auto = autorizados.read()
                            #verifica se o id está autorizado
                            #if chatID in auto:
                                #verifica se o id é o do garçom
                        ########################################

          if str(chatID) in lista or str(chatID) == administrador:
                        if str(chatID) == str(garcom1) or str(chatID) == str(garcom2) or str(chatID) == str(garcom3) or str(chatID) == str(garcom4) or str(chatID) == str(garcom5):
                            frase = bot.escuta(frase=mensagem)
                            proibidos = ['/fechar_conta','/abastecer','/add_cardapio','/canc_venda','/apg_cardapio','/relatorio','/transferir_mesa']                           
                            if str(frase) == '/mesas_abertas' or str(frase) == '/cardapio':
                              resp = bot.pensa(frase)
                              if resp == 'Cardápio!':
                                teste = 'cardapio.pdf'
                                telegram.sendDocument(chatID, open(teste, 'rb'))
                                #teste = 'estoque.jpg'
                                #telegram.sendDocument(chatID, open(teste, 'rb'))
                              elif resp == 'Mesas abertas!':
                                doc = 'mesas abertas.pdf'
                                telegram.sendDocument(chatID, open(doc, 'rb'))
                            elif str(frase) in proibidos:
                              telegram.sendMessage(chatID,'Você não tem autorização para realizar esta operação!')
                            
                            
                            
                            elif str(frase) == '/novo_cliente':
                              if str(chatID) == garcom1:
                                ultima_frase_garcom1 = ultima_frase_cadastro
                                telegram.sendMessage(chatID, ultima_frase_garcom1)
                              elif str(chatID) == garcom2:
                                ultima_frase_garcom2 = ultima_frase_cadastro
                                telegram.sendMessage(chatID, ultima_frase_garcom2)
                              elif str(chatID) == garcom3:
                                ultima_frase_garcom3 = ultima_frase_cadastro
                                telegram.sendMessage(chatID, ultima_frase_garcom3)
                              elif str(chatID) == garcom4:
                                ultima_frase_garcom4 = ultima_frase_cadastro
                                telegram.sendMessage(chatID, ultima_frase_garcom4)
                              elif str(chatID) == garcom5:
                                ultima_frase_garcom5 = ultima_frase_cadastro
                                telegram.sendMessage(chatID, ultima_frase_garcom5)

                            elif frase.split()[0].isnumeric() and ultima_frase_garcom1 == ultima_frase_cadastro or frase.split()[0].isnumeric() and ultima_frase_garcom2 == ultima_frase_cadastro or frase.split()[0].isnumeric() and ultima_frase_garcom3 == ultima_frase_cadastro or frase.split()[0].isnumeric() and ultima_frase_garcom4 == ultima_frase_cadastro or frase.split()[0].isnumeric() and ultima_frase_garcom5 == ultima_frase_cadastro:
                              resp2 = bot.pensa(frase.split()[0])
                              if resp2 in bot.frases:
                                telegram.sendMessage(chatID, 'Esta mesa já está cadastrada.')
                              else:
                                frase = frase.split()
                                mesa_garçom = frase[0]
                                responsavel_mesa = str(frase[1])
                                bot.frases[mesa_garçom] = {"mesa":mesa_garçom,"responsavel":str(responsavel_mesa),"consumo": {"item":[],"qtd":[],"valor_venda":[]},"total":0}
                                if str(chatID) == garcom1:
                                    ultima_frase_garcom1 = ''
                                elif str(chatID) == garcom2:
                                    ultima_frase_garcom2 = ''
                                elif str(chatID) == garcom3:
                                    ultima_frase_garcom3 = ''
                                elif str(chatID) == garcom4:
                                    ultima_frase_garcom4 = ''
                                elif str(chatID) == garcom5:
                                    ultima_frase_garcom5 = ''

                                bot.gravaMemoria()
                                telegram.sendMessage(chatID,'Mesa cadastrada com sucesso!')


                            elif frase == '/venda':
                                if str(chatID) == garcom1:
                                    ultima_frase_garcom1 = ultima_frase_venda
                                elif str(chatID) == garcom2:
                                    ultima_frase_garcom2 = ultima_frase_venda
                                elif str(chatID) == garcom3:
                                    ultima_frase_garcom3 = ultima_frase_venda
                                elif str(chatID) == garcom4:
                                    ultima_frase_garcom4 = ultima_frase_venda
                                elif str(chatID) == garcom5:
                                    ultima_frase_garcom5 = ultima_frase_venda
                                telegram.sendMessage(chatID, ultima_frase_venda)
                            
                            elif frase.split()[0].isnumeric() and ultima_frase_garcom1 == ultima_frase_venda or frase.split()[0].isnumeric() and ultima_frase_garcom2 == ultima_frase_venda or frase.split()[0].isnumeric() and ultima_frase_garcom3 == ultima_frase_venda or frase.split()[0].isnumeric() and ultima_frase_garcom4 == ultima_frase_venda or frase.split()[0].isnumeric() and ultima_frase_garcom5 == ultima_frase_venda:
                                venda = frase.split()
                                mesa = venda[0]
                                cod = venda[1]
                                qtd = venda[2]
                                if mesa in bot.frases:
                                    list_card = {}
                                    for posicao, codigo in enumerate(bot.frases['card_items']['codigo']):
                                        list_card[str(codigo)] = int(posicao)
                                    if str(cod) in list_card:
                                        mesa_codigo = bot.frases['card_items']['codigo'][int(list_card[cod])]
                                        mesa_item = bot.frases['card_items']['item'][int(list_card[cod])]
                                        mesa_valor = bot.frases['card_items']['valor'][int(list_card[cod])]
                                        mesa_estoque = bot.frases['card_items']['estoque'][int(list_card[cod])]
                                        if qtd.isnumeric():
                                            mesa_quantidade = int(qtd)
                                            mesa_valor_venda = float(mesa_valor) * mesa_quantidade
                                            mesa_soma = bot.frases[str(mesa)]['total']
                              
                                            if mesa_estoque == 'x':
                                                mesa_atualiza_estoque = 'x'
                                            else:
                                                mesa_atualiza_estoque = mesa_estoque - mesa_quantidade
                                                mesa_estoque = mesa_atualiza_estoque

                                            mesa_total = mesa_soma + mesa_valor_venda

                                            bot.frases[mesa]['consumo']['item'].append(mesa_item)
                                            bot.frases[mesa]['consumo']['qtd'].append(mesa_quantidade)
                                            bot.frases[mesa]['consumo']['valor_venda'].append(mesa_valor_venda)

                                            garcom_total = 0
                                            if str(chatID) == garcom1:
                                                garcom_total = float(bot.frases[str(empresa)]['ids'][str(garcom1)]['total'][-1])
                                            elif str(chatID) == garcom2:
                                                garcom_total = float(bot.frases[str(empresa)]['ids'][str(garcom2)]['total'][-1])
                                            elif str(chatID) == garcom3:
                                                garcom_total = float(bot.frases[str(empresa)]['ids'][str(garcom3)]['total'][-1])
                                            elif str(chatID) == garcom4:
                                                garcom_total = float(bot.frases[str(empresa)]['ids'][str(garcom4)]['total'][-1])
                                            elif str(chatID) == garcom5:
                                                garcom_total = float(bot.frases[str(empresa)]['ids'][str(garcom5)]['total'][-1])
                                            garcom_total_soma = garcom_total + mesa_valor_venda

                                            if f'{dia}/{mes}/{ano}' in bot.frases[str(empresa)]['ids'][str(chatID)]['data'][-1]:
                                                if str(chatID) == garcom1:
                                                    ultima_frase_garcom1 = ''
                                                    bot.frases[str(empresa)]['ids'][str(chatID)]['total'][-1] = float(garcom_total_soma)
                                                elif str(chatID) == garcom2:
                                                    ultima_frase_garcom2 = ''
                                                    bot.frases[str(empresa)]['ids'][str(chatID)]['total'][-1] = float(garcom_total_soma)
                                                elif str(chatID) == garcom3:
                                                    ultima_frase_garcom3 = ''
                                                    bot.frases[str(empresa)]['ids'][str(chatID)]['total'][-1] = float(garcom_total_soma)
                                                elif str(chatID) == garcom4:
                                                    ultima_frase_garcom4 = ''
                                                    bot.frases[str(empresa)]['ids'][str(chatID)]['total'][-1] = float(garcom_total_soma)
                                                elif str(chatID) == garcom5:
                                                    ultima_frase_garcom5 = ''
                                                    bot.frases[str(empresa)]['ids'][str(chatID)]['total'][-1] = float(garcom_total_soma)
                                            else:
                                                if f'{dia}/{mes}/{ano}' not in bot.frases[str(empresa)]['ids'][str(gerencia)]['data'][-1]:
                                                    bot.frases[str(empresa)]['ids'][str(gerencia)]['id'].append(str(gerencia))
                                                    bot.frases[str(empresa)]['ids'][str(gerencia)]['data'].append(f'{dia}/{mes}/{ano}')
                                                    bot.frases[str(empresa)]['ids'][str(gerencia)]['total'].append(0)

                                                if f'{dia}/{mes}/{ano}' not in bot.frases[str(empresa)]['ids'][str(garcom1)]['data'][-1]:
                                                    if str(chatID) == garcom1:
                                                        ultima_frase_garcom1 = ''
                                                        bot.frases[str(empresa)]['ids'][str(chatID)]['data'].append(f'{dia}/{mes}/{ano}')
                                                        bot.frases[str(empresa)]['ids'][str(chatID)]['total'].append(float(mesa_valor_venda))
                                                        bot.frases[str(empresa)]['ids'][str(garcom1)]['id'].append(str(garcom1))
                                                    else:
                                                        bot.frases[str(empresa)]['ids'][str(garcom1)]['total'].append(0)
                                                        bot.frases[str(empresa)]['ids'][str(garcom1)]['data'].append(f'{dia}/{mes}/{ano}')
                                                        bot.frases[str(empresa)]['ids'][str(garcom1)]['id'].append(str(garcom1))

                                                if f'{dia}/{mes}/{ano}' not in bot.frases[str(empresa)]['ids'][str(garcom2)]['data'][-1]:
                                                    if str(chatID) == garcom2:
                                                        ultima_frase_garcom2 = ''
                                                        bot.frases[str(empresa)]['ids'][str(chatID)]['data'].append(f'{dia}/{mes}/{ano}')
                                                        bot.frases[str(empresa)]['ids'][str(garcom2)]['id'].append(str(garcom2))
                                                        bot.frases[str(empresa)]['ids'][str(chatID)]['total'].append(float(mesa_valor_venda))
                                                    else:
                                                        bot.frases[str(empresa)]['ids'][str(garcom2)]['data'].append(f'{dia}/{mes}/{ano}')
                                                        bot.frases[str(empresa)]['ids'][str(garcom2)]['total'].append(0)
                                                        bot.frases[str(empresa)]['ids'][str(garcom2)]['id'].append(str(garcom2))

                                                if f'{dia}/{mes}/{ano}' not in bot.frases[str(empresa)]['ids'][str(garcom3)]['data'][-1]:
                                                    if str(chatID) == garcom3:
                                                        ultima_frase_garcom3 = ''
                                                        bot.frases[str(empresa)]['ids'][str(garcom3)]['id'].append(str(garcom3))
                                                        bot.frases[str(empresa)]['ids'][str(chatID)]['data'].append(f'{dia}/{mes}/{ano}')
                                                        bot.frases[str(empresa)]['ids'][str(chatID)]['total'].append(float(mesa_valor_venda))
                                                    else:
                                                        bot.frases[str(empresa)]['ids'][str(garcom3)]['data'].append(f'{dia}/{mes}/{ano}')
                                                        bot.frases[str(empresa)]['ids'][str(garcom3)]['total'].append(0)
                                                        bot.frases[str(empresa)]['ids'][str(garcom3)]['id'].append(str(garcom3))

                                                if f'{dia}/{mes}/{ano}' not in bot.frases[str(empresa)]['ids'][str(garcom4)]['data'][-1]:
                                                    if str(chatID) == garcom4:
                                                        ultima_frase_garcom4 = ''
                                                        bot.frases[str(empresa)]['ids'][str(garcom4)]['id'].append(str(garcom4))
                                                        bot.frases[str(empresa)]['ids'][str(chatID)]['data'].append(f'{dia}/{mes}/{ano}')
                                                        bot.frases[str(empresa)]['ids'][str(chatID)]['total'].append(float(mesa_valor_venda))
                                                    else:
                                                        bot.frases[str(empresa)]['ids'][str(garcom4)]['data'].append(f'{dia}/{mes}/{ano}')
                                                        bot.frases[str(empresa)]['ids'][str(garcom4)]['total'].append(0)
                                                        bot.frases[str(empresa)]['ids'][str(garcom4)]['id'].append(str(garcom4))

                                                if f'{dia}/{mes}/{ano}' not in bot.frases[str(empresa)]['ids'][str(garcom5)]['data'][-1]:
                                                    if str(chatID) == garcom5:
                                                        ultima_frase_garcom5 = ''
                                                        bot.frases[str(empresa)]['ids'][str(garcom5)]['id'].append(str(garcom5))
                                                        bot.frases[str(empresa)]['ids'][str(chatID)]['data'].append(f'{dia}/{mes}/{ano}')
                                                        bot.frases[str(empresa)]['ids'][str(chatID)]['total'].append(float(mesa_valor_venda))
                                                    else:
                                                        bot.frases[str(empresa)]['ids'][str(garcom5)]['data'].append(f'{dia}/{mes}/{ano}')
                                                        bot.frases[str(empresa)]['ids'][str(garcom5)]['total'].append(0)
                                                        bot.frases[str(empresa)]['ids'][str(garcom5)]['id'].append(str(garcom5))


                                            bot.frases['vendidos']['data'].append(f'{dia}/{mes}/{ano}')
                                            bot.frases['vendidos']['codigo'].append(mesa_codigo)
                                            bot.frases['vendidos']['item'].append(mesa_item)
                                            bot.frases['vendidos']['total_vendas'].append(mesa_quantidade)

                                            list_card = {}
                                            for posicao, codigo in enumerate(bot.frases['card_items']['codigo']):
                                                list_card[str(codigo)] = int(posicao)         
              
                                            if str(mesa_codigo) in list_card:
                                                if bot.frases['card_items']['estoque'][int(list_card[mesa_codigo])] == 'x':
                                                    bot.frases['card_items']['estoque'][int(list_card[mesa_codigo])] = 'x'
                                                else:
                                                    bot.frases['card_items']['estoque'][int(list_card[mesa_codigo])] = mesa_atualiza_estoque

                                                bot.frases[mesa]['total'] = float(mesa_total)
                                                bot.gravaMemoria()
                                                pedido = f'Mesa: {mesa}\nPedido: {mesa_item}\nQuantidade: {mesa_quantidade}'

                                                mesa = ''
                                                mesa_codigo = ''
                                                mesa_item = ''
                                                mesa_valor = ''
                                                mesa_estoque = ''

                                                mesa_quantidade = ''
                                                mesa_valor_venda = ''
                                                mesa_soma = ''
                                                mesa_atualiza_estoque = ''
                                                mesa_total = ''

                                                resp = f'{pedido}\n\nVenda realizada com sucesso'

                                                #if 'Pedido' in str(pedido):
                                                lista_cozinha = ['camarão','peixe','lula','pastel','pf','salada','batata','calabresa','asdfg']
                                                maximo = int(len(lista_cozinha))-1
                                                conte = 0
                                                while True:
                                                        if conte == int(maximo):
                                                            if lista_cozinha[int(conte)] in str(pedido):
                                                                telegram.sendMessage(cozinha, f'Pedido feito por {primeiro_nome}\n{pedido}')
                                                                break
                                                            else:
                                                                telegram.sendMessage(barman, f'Pedido feito por {primeiro_nome}\n{pedido}')
                                                                break
                                                        else:
                                                            if lista_cozinha[int(conte)] in str(pedido):
                                                                telegram.sendMessage(cozinha, f'Pedido feito por {primeiro_nome}\n{pedido}')
                                                                break
                                                            else:
                                                                conte += 1
                                                #telegram.sendMessage(chatID, resp)

                                                                
                                        else:
                                            telegram.sendMessage(chatID, 'Erro nos valores informados!')
                                    else:
                                        telegram.sendMessage(chatID, 'Ítem não encontrado!')
                                else:
                                    telegram.sendMessage(chatID, 'Não há cadastro nessa mesa')



                            try:
                                bot.fala(resp)
                                #telegram.sendMessage(chatID,'{} disse {}'.format(nome,frase))
                                telegram.sendMessage(chatID,resp)
                            except:
                                pass

                        else:
                            if mensagem == 'mostrar relatorio':
                                relatorio = '/home/ninjamaker/python/IAD/Relatorios/8-5-2021.pdf'
                                telegram.sendDocument(chatID, open(relatorio, 'rb'))
                            
                            if mensagem == '/relatorio':
                                frase = bot.escuta(frase=mensagem)
                                resp = bot.pensa(frase)
                                bot.fala(resp)
                                ultima_frase_gerencia = resp
                                informe_data = resp
                                telegram.sendMessage(chatID,resp)
                            
                            elif '/' in str(mensagem) and mensagem.replace('/',' ').split()[0].isnumeric() and ultima_frase_gerencia == informe_data:
                                try:
                                    frase_data = mensagem.replace('/','-')
                                    if f'{dia}-{mes}-{ano}' == str(frase_data) or f'{mes}-{ano}' == str(frase_data):
                                        frase = bot.escuta(frase=mensagem)
                                        resp = bot.pensa(frase)
                                        if 'Balanceamento' in str(resp):
                                            doc = 'Relatorio_Analise.pdf'
                                            telegram.sendDocument(chatID, open(doc, 'rb'))
                                            informe_data = ''
                                            ultima_frase_gerencia = ''
                                            bot.fala(resp)
                                            telegram.sendMessage(chatID,resp)
                                        else:
                                            informe_data = ''
                                            ultima_frase_gerencia = ''
                                            telegram.sendMessage(chatID,'Houve algum erro na operação!')
                                    else:
                                        relatorio = f'/home/ninjamaker/EMPRESA 1/Relatorios/{frase_data}.pdf'
                                        telegram.sendDocument(chatID, open(relatorio, 'rb'))
                                        telegram.sendMessage(chatID,f'Relatório da data {frase_data}')
                                        '''
                                        #relatorio = f'{frase_data}.pdf'
                                        for root, dirs, files in os.walk(caminho_original):
                                            for file in files:
                                                if '.pdf' in file:
                                                    #if frase_data in file:
                                                        os.remove('Relatorio_Analise.pdf')
                                                        #time.sleep(1)
                                                
                                                #old_file_path = os.path.join(root, file)
                                                #new_file_path = os.path.join(caminho_novo,file)
                                                                                                
                                                #if '.pdf' in file:
                                                #shutil.copy(old_file_path, new_file_path)

                                                informe_data = ''
                                                ultima_frase_gerencia = ''
                                                telegram.sendDocument(chatID, open(file, 'rb'))
                                        telegram.sendMessage(chatID,'Relatório da data {frase}')
                                        '''
                                except:
                                    frase = bot.escuta(frase=mensagem)
                                    resp = bot.pensa(frase)
                                    if 'Balanceamento' in str(resp):
                                        doc = 'Relatorio_Analise.pdf'
                                        telegram.sendDocument(chatID, open(doc, 'rb'))
                                        informe_data = ''
                                        ultima_frase_gerencia = ''
                                        bot.fala(resp)
                                        telegram.sendMessage(chatID,resp)
                                    else:
                                        informe_data = ''
                                        ultima_frase_gerencia = ''
                                        telegram.sendMessage(chatID,'Houve algum erro na operação!')

                            else:
                                frase = bot.escuta(frase=mensagem)
                                resp = bot.pensa(frase)
                                pedido = resp
                                pedido2 = pedido.replace("Venda realizada com sucesso","")
                                
                                ##########       Envia mensagem para id da cozinha ou barman       ###########

                                if 'Pedido' in str(resp):
                                    lista_cozinha = ['camarão','peixe','lula','pastel','pf','salada','batata','calabresa','asdfg']
                                    maximo = int(len(lista_cozinha))-1
                                    conte = 0
                                    while True:
                                        if conte == int(maximo):
                                            if lista_cozinha[int(conte)] in str(pedido2):
                                                telegram.sendMessage(cozinha, f'Pedido feito por {primeiro_nome}\n{pedido2}')
                                                break
                                            else:
                                                telegram.sendMessage(barman, f'Pedido feito por {primeiro_nome}\n{pedido2}')
                                                break
                                        else:                                    
                                            if lista_cozinha[int(conte)] in str(pedido2):
                                                telegram.sendMessage(cozinha, f'Pedido feito por {primeiro_nome}\n{pedido2}')
                                                break
                                            else:
                                                conte += 1
                                


                                if resp == 'Cardápio!':
                                    teste = 'cardapio.pdf'
                                    telegram.sendDocument(chatID, open(teste, 'rb'))
                                    #teste = 'estoque.jpg'
                                    #telegram.sendDocument(chatID, open(teste, 'rb'))
                                elif resp == 'Mesas abertas!':
                                    doc = 'mesas abertas.pdf'
                                    telegram.sendDocument(chatID, open(doc, 'rb'))
                                elif 'Forma de pagamento: digite "c" para cartão, "d" para dinheiro, "e" para dividir.' in str(resp):
                                    doc = 'conta.pdf'
                                    telegram.sendDocument(chatID, open(doc, 'rb'))
                                elif 'Ítem!' in str(resp):
                                    doc = 'item.jpg'
                                    telegram.sendDocument(chatID, open(doc, 'rb'))
                                elif 'teste plot' in str(resp):
                                    doc = 'teste.jpg'
                                    telegram.sendDocument(chatID, open(doc, 'rb'))
                                elif 'Balanceamento' in str(resp):
                                    doc = 'Relatorio_Analise.pdf'
                                    telegram.sendDocument(chatID, open(doc, 'rb'))
                                try:
                                    bot.fala(resp)
                                    telegram.sendMessage(chatID,resp)
                                except:
                                    pass
          else:
            if mensagem == 'aia':
                telegram.sendMessage(chatID,str(chatID))
            else:
                telegram.sendMessage(chatID,'Você não é autorizado para usar este programa.')                


telegram.message_loop(recebendoMsg)

while True:
    pass
