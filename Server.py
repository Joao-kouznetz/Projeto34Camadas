#####################################################
# Camada Física da Computação
#Carareto
#11/08/2022
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from enlace import *
import time
import numpy as np

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
serialName = "COM3"           # Ubuntu (variacao de)
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
        
        print("esperando 1 byte de sacrifício")
        rxBuffer, nRx = com1.getData(1)
        com1.rx.clearBuffer()
        time.sleep(.1)
      

        while com1.rx.getIsEmpty():
            time.sleep(0.1)


        rxBuffer = com1.rx.getNData(15)
        print("recebeu {} bytes" .format(len(rxBuffer)))
    
            

        decimal_values = []
        for byte in rxBuffer:
            decimal_values.append(byte)

        # Enviando de volta o numero de comandos
        print(decimal_values)
        if decimal_values[0] == 255:
            bytes15 = bytearray(decimal_values)
            com1.sendData(np.asarray(bytes15))

        conteudo_total = [] #conteudo junto no payload
        n_pacote = 0
        n_total_pacotes = -1
        time.sleep(0.5
                   )
        while n_pacote != n_total_pacotes:
            #HEAD                    
            rxBuffer = com1.rx.getNData(12)
            print("recebeu {} bytes na head".format(len(rxBuffer)))

            decimal_values = []
            for byte in rxBuffer:
                decimal_values.append(byte)  

            print('head', decimal_values)
            n_total_pacotes = decimal_values[0]

            if n_pacote + 1 == decimal_values[1]:
                n_pacote = decimal_values[1]

                payload = decimal_values[2] #Quantos bytes tem no payload do pacote

                #PAYLOAD
                start_time = time.time()
                rxBuffer = com1.rx.getNData(payload)
                print("recebeu {} bytes no payload" .format(len(rxBuffer)))

                decimal_values = []
                for byte in rxBuffer:
                    decimal_values.append(byte)
                    conteudo_total.append(byte)

                print('payload', decimal_values)

                #EOP
                start_time = time.time()
                tempoMenor5EOP = True
                while com1.rx.getBufferLen() < 3 and tempoMenor5EOP == True:
                    time.sleep(.1)
                    print('len buffer', com1.rx.getBufferLen())
                    print('tempo', time.time() - start_time)
                    if time.time() - start_time >= 3:
                        tempoMenor5EOP = False

                if tempoMenor5EOP == False:
                    print('Não recebeu a quantidade certa de bytes')
                    com1.rx.clearBuffer()
                    deu_ruim = bytearray([255,255,0,0,0,0,0,0,0,0,0,0,255,0,255])
                    n_pacote -= 1
                    com1.sendData(np.asarray(deu_ruim))
                    time.sleep(.1)
       
                else:
                    rxBuffer = com1.rx.getNData(3)
                    print("recebeu {} bytes no EOP" .format(len(rxBuffer)))    

                    decimal_values = []
                    for byte in rxBuffer:
                        decimal_values.append(byte) 

                    if decimal_values[0] == 255 and decimal_values[1] == 0 and decimal_values[2] == 255:
                        tudo_certo = bytearray([1,1,0,0,0,0,0,0,0,0,0,0,255,0,255])
                        com1.sendData(np.asarray(tudo_certo))
                        time.sleep(.1)
                    else:
                        print('Payload não corresponde')
                        com1.rx.clearBuffer()
                        deu_ruim = bytearray([1,255,0,0,0,0,0,0,0,0,0,0,255,0,255])
                        n_pacote -= 1
                        com1.sendData(np.asarray(deu_ruim))
                        time.sleep(.1)

            else:
                print('Numero do pacote não correspondido')
                com1.rx.clearBuffer()
                deu_ruim = bytearray([255,1,0,0,0,0,0,0,0,0,0,0,255,0,255])
                com1.sendData(np.asarray(deu_ruim))
                time.sleep(.1)
                
        print('Conteudo total:', conteudo_total)

        #Confirma para o cliente que deu tudo certo
        deu_tudo_certo = bytearray([2,2,0,0,0,0,0,0,0,0,0,0,255,0,255])
        com1.sendData(np.asarray(deu_tudo_certo))
        time.sleep(.1)

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
