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
        
        #Agora vamos iniciar a recepção dos dados. Se algo chegou ao RX, deve estar automaticamente guardado
        #Observe o que faz a rotina dentro do thread RX
        #print um aviso de que a recepção vai começar.

        #Será que todos os bytes enviados estão realmente guardadas? Será que conseguimos verificar?
        #Veja o que faz a funcao do enlaceRX  getBufferLen
      

        while com1.rx.getIsEmpty():
            time.sleep(0.1)


        rxBuffer = com1.rx.getAllBuffer(com1.rx.getBufferLen())
        print("recebeu {} bytes" .format(len(rxBuffer)))
    

        
        # print("Salvando dados no arquivo:")
        # print(rxBuffer)

        decimal_values = []
        for byte in rxBuffer:
            decimal_values.append(byte)

        # print("Valores decimais individuais:", decimal_values)

        comandos = []
        comando = []

        contador = 0
        for i in decimal_values:
            if contador == 0:
                contador = i
                if len(comando) != 0:
                    comandos.append(comando)
                comando = []

            else:
                comando.append(i)
                contador -= 1
            
        comandos.append(comando)   

        # Enviando de volta o numero de comandos

        retorna_Ncomandos = bytearray([len(comandos)])
        com1.sendData(np.asarray(retorna_Ncomandos))
        
        #Printando comandos linha por linha

        for i in comandos:
            print(i)

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
