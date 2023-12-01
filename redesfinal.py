import random
import time

contador_solicitudes = {}
limite = 3
conta = 0
limite_extra = 124
limite_diario = 100
lista_negra = set()
ips_usadas = []

def solicitudes(ip):
    global conta
    if ip in lista_negra:
        conta-=1
        return
    contador_solicitudes[ip] = contador_solicitudes.get(ip, 0) + 1
    if contador_solicitudes[ip] > limite:
        lista_negra.add(ip)
        print(f"IP {ip} ha sido bloqueada. Se ha superado el limite de solicitudes para una misma IP.")
    else:
        print(f"Solicitud de  {ip} recibida. ({contador_solicitudes[ip]} solicitudes)")

def generar_ip_aleatoria(probabilidad=0.3):
    if ips_usadas and random.random() < probabilidad:
        return random.choice(ips_usadas)

    octeto1 = random.randint(0, 255)
    octeto2 = random.randint(0, 255)
    octeto3 = random.randint(0, 255)
    octeto4 = random.randint(0, 255)
    ip = f"{octeto1}.{octeto2}.{octeto3}.{octeto4}"
    ips_usadas.append(ip)
    return ip

def generar_ip_aleatoria_ddos(probabilidad=0.65):
    if ips_usadas and random.random() < probabilidad:
        return random.choice(ips_usadas)
    octeto1 = random.randint(0, 255)
    octeto2 = random.randint(0, 255)
    octeto3 = random.randint(0, 255)
    octeto4 = random.randint(0, 255)
    ip = f"{octeto1}.{octeto2}.{octeto3}.{octeto4}"
    ips_usadas.append(ip)
    return ip

def simular_solicitudes (num_solicitudes, intervalo_tiempo):
    for _ in range(num_solicitudes):
        ip = generar_ip_aleatoria()
        solicitudes(ip)
        time.sleep(intervalo_tiempo)

def simular_solicitudes_ping_ddos(num_solicitudes, intervalo_tiempo):
    global conta
    for _ in range(num_solicitudes):
        ip = generar_ip_aleatoria_ddos()
        solicitudes(ip)
        conta +=1
        if conta == limite_extra: break
        time.sleep(intervalo_tiempo)


def imprimir_lista_negra():
    print("Lista negra de IPs:")
    for ip in lista_negra:
        print(ip)

def main():
    global limite_diario
    global conta
    simular_solicitudes(40, 0.1)
    imprimir_lista_negra()
    while True:

        time.sleep(4)
        inicio = time.time()
        simular_solicitudes_ping_ddos(120, 0.008)
        fin=time.time()
        tiempo = fin-inicio
        imprimir_lista_negra()
        print(f"CANTIDAD DE PETICIONES: {conta}")
        print("")
        print(f"TIEMPO QUE SE DEMORÓ EN SIMULAR LAS SOLICITUDES: {tiempo}")

        if tiempo<=1.1 and conta>= limite_diario :
            print(" ")
            print("SE DETECTO UN ATAQUE DDOS")
            print("SE LIMITARAN LAS PETICIONES A LA MITAD")
            limite_diario = limite_diario/2
            print(" ")
            time.sleep(4)
            while True:
                simular_solicitudes_ping_ddos(50, 0.1)
                imprimir_lista_negra()
                print("---LIMITE TERMINADO---")
                time.sleep(4)
        conta = 0
if __name__ == "__main__":
    main()