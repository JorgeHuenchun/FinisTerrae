import socket
from Crypto.PublicKey import RSA, ElGamal
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes

# Generar o cargar claves RSA (1024 bits) en el servidor
try:
    with open("private_key_rsa.pem", "rb") as file:
        private_key_rsa = RSA.import_key(file.read())
except FileNotFoundError:
    key_rsa = RSA.generate(1024)
    private_key_rsa = key_rsa.export_key()
    with open("private_key_rsa.pem", "wb") as file:
        file.write(private_key_rsa)

public_key_rsa = private_key_rsa.publickey().export_key()

# Guardar la clave pública RSA en un archivo
with open("public_key_rsa.pem", "wb") as file:
    file.write(public_key_rsa)

# Generar o cargar claves ElGamal (1024 bits) en el servidor
try:
    with open("private_key_elgamal.pem", "rb") as file:
        private_key_elgamal = ElGamal.import_key(file.read())
except FileNotFoundError:
    key_elgamal = ElGamal.generate(1024, get_random_bytes)
    private_key_elgamal = key_elgamal.export_key()
    with open("private_key_elgamal.pem", "wb") as file:
        file.write(private_key_elgamal)

public_key_elgamal = key_elgamal.publickey().export_key()

# Guardar la clave pública ElGamal en un archivo
with open("public_key_elgamal.pem", "wb") as file:
    file.write(public_key_elgamal)

# Crear socket del servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 1234))
server_socket.listen(1)

print("Esperando conexión del cliente...")

# Aceptar conexión del cliente
client_socket, address = server_socket.accept()
print("Cliente conectado:", address)

# Enviar claves públicas al cliente
client_socket.send(public_key_rsa + b'|' + public_key_elgamal)

# Recibir mensaje cifrado del cliente con ElGamal
encrypted_message_elgamal = client_socket.recv(1024)

# Descifrar el mensaje con la clave ElGamal
decrypted_message_elgamal = private_key_elgamal.decrypt(encrypted_message_elgamal)

# Guardar el mensaje descifrado en un archivo
with open("mensajerecibido.txt", "wb") as file:
    file.write(decrypted_message_elgamal)

# Imprimir el mensaje descifrado
print("Mensaje ElGamal recibido:", decrypted_message_elgamal.decode())

# Cerrar conexión
client_socket.close()
server_socket.close()
print("Proceso completado. Mensaje desencriptado y guardado en 'mensajerecibido.txt'.")
