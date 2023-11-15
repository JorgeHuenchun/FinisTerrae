import socket
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad

# Establecer parámetros Diffie-Hellman
p = 23
g = 5

# Generar clave privada del cliente
b = 15
B = (g**b) % p

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(('localhost', 12345))
print("Conexión establecida con el servidor")


cliente.sendall(str(p).encode())#Enviar parámetros Diffie-Hellman 
print("Enviado p:", p)
cliente.sendall(str(g).encode())
print("Enviado g:", g)
cliente.sendall(str(B).encode())
print("Enviado B:", B)
print("Parámetros enviados Diffie-Hellman al servidor")


A = int(cliente.recv(1024).decode()) #Recibir clave pública 
print("Recibida clave pública del servidor:", A)

#Clave compartida
s = (A**b) % p
print("Clave compartida:", s)

with open('mensajeentrada.txt', 'r') as archivo: #Leer mensaje de un archivo
    mensaje = archivo.read()

# Encriptar mensaje
clave = str(s).zfill(8)[:8].encode()
cipher = DES.new(clave, DES.MODE_ECB)
mensaje_encriptado = cipher.encrypt(pad(mensaje.encode(), 8))
print("Encriptado mensaje:", mensaje_encriptado)

#Envia mensaje encriptado al servidor
cliente.sendall(mensaje_encriptado)
print("Enviado mensaje encriptado al servidor...")

#cliente.close()
