from ncclient import manager

router = {
    "host": "192.168.56.102",
    "port": 830,
    "username": "cisco",
    "password": "cisco123!",
    "hostkey_verify": False
}


nuevo_hostname = "vega_verdejo"
xml_hostname = f"""
<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <hostname>{nuevo_hostname}</hostname>
  </native>
</config>
"""

xml_loopback = """
<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <interface>
      <Loopback>
        <name>11</name>
        <ip>
          <address>
            <primary>
              <address>11.11.11.11</address>
              <mask>255.255.255.255</mask>
            </primary>
          </address>
        </ip>
      </Loopback>
    </interface>
  </native>
</config>
"""

print(f"Iniciando conexión NETCONF con {router['host']}...")

try:
    with manager.connect(**router) as m:
        print("¡Conexión NETCONF exitosa!")
        
    
        print(f"Cambiando el hostname a: {nuevo_hostname}...")
        respuesta_host = m.edit_config(target='running', config=xml_hostname)
        
        
        print("Creando la interfaz Loopback 11 (11.11.11.11/32)...")
        respuesta_loop = m.edit_config(target='running', config=xml_loopback)
        
        print("¡Configuraciones aplicadas exitosamente!")
        
except Exception as e:
    print(f"Error durante la ejecución: {e}")