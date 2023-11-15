import socket
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad

# Establecer parámetros Diffie-Hellman
p = 23
g = 5

# Generar clave privada del servidor
a = 6
A = (g**a) % p


servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Crear servidor
servidor.bind(('localhost', 12345))
servidor.listen(1)
print("Servidor activo")


cliente, direccion = servidor.accept()
print("Cliente conectado:", direccion)


p_cliente = int(cliente.recv(1024).decode()) #Recibe parámetros Diffie-Hellman del cliente
print("Recibido p del cliente:", p_cliente)
g_cliente = int(cliente.recv(1024).decode())
print("Recibido g del cliente:", g_cliente)
B = int(cliente.recv(1024).decode())
print("Recibido B del cliente:", B)
print("Recibidos parámetros Diffie-Hellman del cliente:", p_cliente, g_cliente, B)


cliente.sendall(str(A).encode()) #Enviar clave pública al cliente
print("Enviada clave pública al cliente:", A)


s = (B**a) % p # Calcular clave compartida
print("Clave compartida:", s)

mensaje_encriptado = cliente.recv(1024)
print("Mensaje encriptado del cliente")

clave = str(s).zfill(8)[:8].encode()# Desencriptar mensaje
cipher = DES.new(clave, DES.MODE_ECB)
mensaje_desencriptado = unpad(cipher.decrypt(mensaje_encriptado), 8).decode()
print("Desencriptado mensaje:", mensaje_desencriptado)


with open('mensajerecibido.txt', 'w') as archivo: # Guardar mensaje desencriptado en un archivo
    archivo.write(mensaje_desencriptado)

cliente.close()
servidor.close()
