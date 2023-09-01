#####################################################
# Camada Física da Computação
#Carareto
#11/08/2022
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 
import sys
sys.path.append('../')  # Volte um diretório para chegar à pasta do projeto

from enlace import *
import time
import numpy as np
from random import *
import sys

def generate_command_sequence():
    quantidade=70
    lista=[]
    for i in range(quantidade):
        lista.append(randint(0, 9))
    return lista

def segmentar_lista(lista_original):
    tamanho_maximo_sublista = 50
    lista_segmentada = []
    sublista_atual = []

    for valor in lista_original:
        sublista_atual.append(valor)

        if len(sublista_atual) == tamanho_maximo_sublista:
            lista_segmentada.append(sublista_atual)
            sublista_atual = []

    if sublista_atual:
        lista_segmentada.append(sublista_atual)

    return lista_segmentada

def cria_header_eop(lista_pacotes):
    lista_final=[]
    lista_eop=[255,0,255]
    num_pacotes=len(lista_pacotes)
    for i in range(len(lista_pacotes)):
        lista_header=[]
        lista_header.append(num_pacotes)
        lista_header.append((i+1))
        lista_header.append(len(lista_pacotes[i]))
        for t in range(9):
            lista_header.append(0)
        lista_final.append(lista_header)
        lista_final.append(lista_pacotes[i])
        lista_final.append(lista_eop)
    
    lista_comtudo=[]

    for i in range(0,len(lista_final),3):
        pacote=[]
        for valor in  lista_final[i]:
            pacote.append(valor)
        for valor2 in lista_final[i+1]:
            pacote.append(valor2)
        for valor3 in lista_final[(i+2)]:
            pacote.append(valor3)
        lista_comtudo.append(pacote)


    return lista_comtudo





# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
# serialName = "COM3"                  # Windows(variacao de)


def main():
    try:
        print("Iniciou o main")
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)
        
       
        # Ativa comunicacao. Inicia os threads e a comunicação serial 
        com1.enable()
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("Abriu a comunicação")
        
           
                  
        #aqui você deverá gerar os dados a serem transmitidos. 
        #seus dados a serem transmitidos são um array bytes a serem transmitidos. Gere esta lista com o 
        #nome de txBuffer. Esla sempre irá armazenar os dados a serem enviados.
        print("enviando byte sacrificio")
        time.sleep(.2)
        com1.sendData(bytes([0]))
        time.sleep(0.1)

        RecebeuDeVolta=False
        while RecebeuDeVolta==False:
            print("HandShake:")
            #header
            bytes15=bytearray([255,0,0,0,0,0,0,0,0,0,0,0,255,0,255])
            com1.sendData(np.asarray(bytes15))
            time.sleep(0.1)
            
            print("esperando resposta para transmissão")
            start_time = time.time()
            while com1.rx.getBufferLen()<15:
                time.sleep(0.1)
                if time.time() - start_time > 5:
                    print('time out')
                    tentar_novamente=input("servidor inativo. Tentar novamente? S/N")
                    if tentar_novamente.lower()=='n':
                        sys.exit()
                    if tentar_novamente.lower()=='s':
                        break
            if com1.rx.getIsEmpty()==False:
                RecebeuDeVolta=True

        print('recebeu handshake')
        RxBuffer=com1.rx.getNData(15)
        print(list(RxBuffer))
        print(len(RxBuffer))
        print("----------------------")
        
        print('começando fragmentação de pacote')
        #head 12 bytes payload entre 0 e 50 e EOP 3
        #head mandar numero do pacote e a quantidades de numero total de pacotes que serao transmitidos 
        lista=generate_command_sequence()
        lista_pacotes=segmentar_lista(lista)
        lista_header_pacotes=cria_header_eop(lista_pacotes)
        print(lista_header_pacotes)
        
        for pacote in lista_header_pacotes:
            print('enviando pacote')
            bytepacote=bytearray(pacote)
            com1.sendData(np.asarray(bytepacote))
            time.sleep(0.1)
            RxBuffer=com1.rx.getNData(15)
            print()
            decimal=list(RxBuffer)
            if decimal[0]==1 and  decimal[1]==1 and  decimal[12]==255 and  decimal[13]==0  and decimal[14]==255:
                pass
            else:
                print('deu ruim')
                break
                






    
        
        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()







