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
        
        def generate_command_sequence():
            num_commands = randint(10, 30)
            
            possible_commands=[
                [4,0,0,0,0],[4,0,0,187,0],[3,187,0,0],[3,0,187,0],[3,0,0,187],[2,0,170],[2,187,0],[1,0],[1,187]
            ]
            comandosEscolhidos=[]
            for i in range(num_commands):
                k=randint(0,8)
                comandosEscolhidos.append(possible_commands[k])

            return comandosEscolhidos,num_commands
        comando,numerocomandos=generate_command_sequence()
        
        listaTodos=[]
        for i in comando:
            for t in i:
                listaTodos.append(t)
        byte_array0 = bytearray(listaTodos)

        
        print("Carregando comandos para transmissao:")
        print("esta mandando o seguinte comando{}".format(byte_array0))
        print("tem {} comandos nesse envio".format(numerocomandos))
        print("----------------------")
        
        #txBuffer = imagem em bytes!
        txBuffer = byte_array0 #isso é um array de bytes
       
        print("meu array de bytes tem tamanho {}" .format(len(txBuffer)))
        #faça aqui uma conferência do tamanho do seu txBuffer, ou seja, quantos bytes serão enviados.
       
            
        #finalmente vamos transmitir os todos. Para isso usamos a funçao sendData que é um método da camada enlace.
        #faça um print para avisar que a transmissão vai começar.
        #tente entender como o método send funciona!
        #Cuidado! Apenas trasmita arrays de bytes!
               
        
        com1.sendData(np.asarray(txBuffer))  #as array apenas como boa pratica para casos de ter uma outra forma de dados
          
        # A camada enlace possui uma camada inferior, TX possui um método para conhecermos o status da transmissão
        # O método não deve estar funcionando quando usado como abaixo. deve estar retornando zero. Tente entender como esse método funciona e faça-o funcionar.
        txSize = com1.tx.getStatus()
        
        # RECEBE NUMERO DE COMANDOS QUE ELE RECEBEU
        print("esperadno resposta")
        #inicia time out
        start_time = time.time()
        while com1.rx.getIsEmpty():
            time.sleep(0.1)
            if time.time() - start_time > 5:
                print('time out')
                break
        nComandosRecebidos=com1.rx.getAllBuffer(com1.rx.getBufferLen())
        nComandosRecebidos = list(nComandosRecebidos)      
        if numerocomandos==nComandosRecebidos[0]:
            print(f'numero de comandos era {numerocomandos} e recebi {nComandosRecebidos[0]}')
        else:
            print("Deu erro na transmissão de comandos")

        
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