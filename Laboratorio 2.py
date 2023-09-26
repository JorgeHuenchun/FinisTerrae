#Laboratorio 2
#Jorge Huenchun, Matias Urbina

import hashlib

# Función para cifrar el mensaje 
def cifrar(mensaje, red_sustitucion):
    mensaje_cifrado = ""
    for caracter in mensaje:
        if caracter in red_sustitucion:
            mensaje_cifrado += red_sustitucion[caracter]
        else:
            mensaje_cifrado += caracter
    return mensaje_cifrado

# Función para generar el hash del mensaje cifrado
def generarHash(mensaje_cifrado):
    hash = hashlib.sha256(mensaje_cifrado.encode()).hexdigest()
    return hash

# Definir las sustituciones
sustituciones = {'a': 'x','b': 'y','c': 'z','d': 'm','e': 'n','f': 'o','g': 'p',
        'h': 'q','i': 'r','j': 's','k': 't','l': 'u','m': 'v','n': 'w','o': 'a',
        'p': 'b','q': 'c','r': 'd','s': 'e','t': 'f','u': 'g','v': 'h','w': 'i',
        'x': 'j','y': 'k','z': 'l',' ': ' ','\n': '\n'}

# Leer el mensaje original desde el archivo
with open("mensajedeentrada.txt", 'r') as file:
    mensaje_original = file.read()

# Cifra el mensaje de entrada
mensaje_cifrado = cifrar(mensaje_original, sustituciones)

# Generar el hash del mensaje cifrado
hash_mensaje_cifrado = generarHash(mensaje_cifrado)

# Guardar el mensaje cifrado y el hash en un nuevo archivo 
with open("mensajeseguro.txt", 'w') as file:
    file.write(mensaje_cifrado + '\n')
    file.write(hash_mensaje_cifrado)

# Función para descifrar el mensaje
def descifrar(mensaje_cifrado, red_sustitucion):
    mensaje_original = ""
    for caracter in mensaje_cifrado:
        for clave, valor in red_sustitucion.items():
            if caracter == valor:
                mensaje_original += clave
                break
        else:
            mensaje_original += caracter
    return mensaje_original

# Función para verificar la integridad del mensaje
def verificarIntegridad(mensaje_cifrado, hash_original):
    # Generar el hash para cifrar
    hash_calculado = hashlib.sha256(mensaje_cifrado.encode()).hexdigest()
    return hash_calculado == hash_original

# Leer el mensaje cifrado y el hash desde el archivo
with open("mensajeseguro.txt", 'r') as file:
    mensaje_cifrado = file.readline().strip()
    hash_original = file.readline().strip()

# Descifrar el mensaje cifrado
mensaje_original = descifrar(mensaje_cifrado, sustituciones)

# Verificar la integridad del mensaje
if verificarIntegridad(mensaje_cifrado, hash_original):
    print("El mensaje no ha sido modificado y es autentico:")
    print("El mensaje dice:", mensaje_original)
else:
    print("El mensaje fue modificado o no es autentico.")

