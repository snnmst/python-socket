import socket
import threading

PORT = 5050

def main():
    try:
        with socket.socket() as serverSock:
            serverSock.bind(('', PORT))
            serverSock.listen(8)

            print('Arithmetic server running...')

            while True:
                clientSock, clientAddr = serverSock.accept()
                print('Connected Client:{}'.format(clientAddr))
                thread = threading.Thread(target=threadProc, args=(clientSock, clientAddr))
                thread.start()

    except socket.error as msg:
        print('Socket error:{}'.format(msg))



def serverProc(fileWrite, command, param1, param2):
        if command == 'ADD':
                fileWrite.write('RESULT {}\n'.format(param1 + param2))
                fileWrite.flush()
        elif command == 'SUB':
                fileWrite.write('RESULT {}\n'.format(param1 - param2))
                fileWrite.flush()
        elif command == 'MULTIPLY':
                fileWrite.write('RESULT {}\n'.format(param1 * param2))
                fileWrite.flush()
        elif command == 'DIVIDE':
                fileWrite.write('RESULT {}\n'.format(param1 / param2))
                fileWrite.flush()
                
                

def threadProc(clientSock, clientAddr):

    fileRead = clientSock.makefile('r')
    fileWrite = clientSock.makefile('w')

    try:
        while True:
            line = fileRead.readline()

            args = line.split()
            if args[0] == 'quit':
                break
            command =args[0]
            if not command:
                fileWrite.write('ERROR "invalid operation"\n')
                fileWrite.flush()
                continue
            if len(args) != 3:
                fileWrite.write('ERROR "two operands must be specified"\n')
                fileWrite.flush()
                continue
            try:
                param1 = float(args[1])
                param2 = float(args[2])
            except:
                fileWrite.write('ERROR "invalid operand"\n')
                continue
            serverProc(fileWrite, command ,param1, param2)
            print('Message From Client {}, Command: {}'.format(clientAddr, line))

    except socket.error as msg:
        print('Socket error:{}'.format(msg))
    finally:
        clientSock.shutdown(socket.SHUT_RDWR)
        clientSock.close()
        fileRead.close()
        fileWrite.close()
    print('Client Logout {}, Command: {}'.format(clientAddr, line))

main()
