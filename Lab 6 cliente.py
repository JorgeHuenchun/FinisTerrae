import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

#Crea las conexiones de cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 1234))

#Recibe clave publica 
public_key = client_socket.recv(2048)

#Lee el archivo de entrada
with open("mensajeentrada.txt", "rb") as file:
    message = file.read()

#Carga la clave publica
server_public_key = RSA.import_key(public_key)

#Cifra el archivo con clave publica 
cipher_rsa = PKCS1_OAEP.new(server_public_key)
encrypted_message = cipher_rsa.encrypt(message)

#Envia archivo al servidor
client_socket.send(encrypted_message)

#Se cierra la conexión
client_socket.close()
print("Proceso completado. Archivo cifrado enviado al servidor.")

##Cliente##
