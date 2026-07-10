
from netmiko import ConnectHandler

router = {
    'device_type': 'cisco_ios',
    'host': '192.168.56.102',
    'username': 'cisco',
    'password': 'cisco123!',
}

print(f"Conectando al router {router['host']} con Netmiko...")
conexion = ConnectHandler(**router)
print("¡Conexión SSH exitosa!\n")

# Configurar EIGRP Nombrado (AS 100) con interfaces pasivas
comandos_eigrp = [
    'router eigrp REDES_DUOC',
    'address-family ipv4 unicast autonomous-system 100',
    'passive-interface default',
    'exit-address-family',
    'address-family ipv6 unicast autonomous-system 100',
    'passive-interface default',
    'exit-address-family'
]
print("Inyectando configuración EIGRP Nombrado...")
conexion.send_config_set(comandos_eigrp)

# Ejecutar los comandos 'show'
print("Extrayendo información solicitada por la rúbrica...")
salida_eigrp = conexion.send_command('show running-config | section eigrp')
salida_interfaces = conexion.send_command('show ip interface brief')
salida_version = conexion.send_command('show version')
salida_run = conexion.send_command('show running-config')

# 4. Mostrar en pantalla el requerimiento de EIGRP
print("\n--- RESULTADO: show running-config section eigrp ---")
print(salida_eigrp)
print("----------------------------------------------------\n")

# 5. Guardar todo en archivos de texto
with open("evidencia_interfaces.txt", "w") as f:
    f.write(salida_interfaces)

with open("evidencia_version.txt", "w") as f:
    f.write(salida_version)

with open("evidencia_run.txt", "w") as f:
    f.write(salida_run)

print("¡Extracción completa! Las otras salidas se guardaron en archivos .txt")
conexion.disconnect()
