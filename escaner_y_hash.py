import socket 
import hashlib
import os
import threading
import sys, time
import pyfiglet
from colorama import Fore, Style, init

init(autoreset=True)

puertos_abiertos = []

def escribir(texto, delay=0.03, color=Fore.WHITE):
    sys.stdout.write(color)   
    for char in texto:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(Style.RESET_ALL + "\n") 

#Escaneo de un solo puerto
def escanear_puerto(host, puerto):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        if s.connect_ex((host, puerto)) == 0:
            print(Fore.GREEN + f"[+] Puerto {puerto} abierto")
            puertos_abiertos.append(puerto)
        s.close()
    except Exception:
        pass

#Escaneo de rango de puertos con threads
def escanear_puertos(host, rango_puertos):
    print(Fore.CYAN + f"\nEscaneando puertos de {host}...")
    threads = []
    
    for puerto in rango_puertos:
        t = threading.Thread(target=escanear_puerto, args=(host, puerto))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(Fore.YELLOW + f"\nEscaneo completado. Puertos abiertos: {puertos_abiertos}")

#Hashing de archivos
def calcular_hash_archivo(ruta_archivo):
    if not os.path.isfile(ruta_archivo):
        print(Fore.RED + f"Archivo no encontrado: {ruta_archivo}")
        return None
    hash_sha256 = hashlib.sha256()
    with open(ruta_archivo, "rb") as f:
        for bloque in iter(lambda: f.read(4096), b""):
            hash_sha256.update(bloque)
    return hash_sha256.hexdigest()

#Menú
def menu_principal():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        banner = pyfiglet.figlet_format("Cyber Tool")
        print(Fore.GREEN + banner)
        print(Fore.CYAN + "===========================================")
        print(Fore.YELLOW + "[1]. Escanear puertos")
        print(Fore.MAGENTA + "[2]. Calcular hash de archivo")
        print(Fore.RED + "[3]. Salir")
        print(Fore.CYAN + "===========================================")

        opcion = input(Fore.WHITE + "Elige una opción: ")

        if opcion == "1":
            host = input("Ingresa IP o localhost: ")
            inicio = int(input("Puerto inicial: "))
            fin = int(input("Puerto final: "))
            escanear_puertos(host, range(inicio, fin + 1))
            input(Fore.CYAN + "\nPresiona Enter para volver al menú...")

        elif opcion == "2":
            archivo = input("Ingresa la ruta del archivo: ")
            hash_resultado = calcular_hash_archivo(archivo)
            if hash_resultado:
                print(Fore.GREEN + f"\nHash SHA-256:\n{hash_resultado}")
            input(Fore.CYAN + "\nPresiona Enter para volver al menú...")

        elif opcion == "3":
            escribir("Saliendo...", delay=0.05)
            break
        else:
            print(Fore.RED + "Opción inválida, ingrese uno válido.")
            time.sleep(1)

#Ejecución
if __name__ == "__main__":
    escribir("Iniciando CyberSecurity Tool...", delay=0.05, color=Fore.GREEN)
    time.sleep(1)
    menu_principal()