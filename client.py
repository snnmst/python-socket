import socket

PORT = 5050

def main():
    try:
        with socket.socket() as clientSock:
            clientSock.connect(('127.0.0.1', PORT))

            print('Arithmetic client connected...')
            fileRead = clientSock.makefile('r')
            fileWrite = clientSock.makefile('w')

            while True:
                s = input('CMD>').strip()

                if s == '':
                    continue
                fileWrite.write(s + '\n')
                fileWrite.flush()
                if s == 'quit':
                    break
                response = fileRead.readline()
                print(response, end='')

            clientSock.shutdown(socket.SHUT_RDWR)
    except socket.error as msg:
        print('Socket error:{}'.format(msg))

main()
