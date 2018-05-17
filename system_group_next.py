# Imports
from snmp_library import *
from pysnmp.hlapi.asyncore import *
import time

print("##################################################\n"
      "                    SNMP_GETNEXT                      \n"
      "            Mario Gonzalez  | 2018                \n"
      "##################################################\n")

print("###CUESTIONES TEORICAS###\n"
      "El tiempo invertido con el uso de SNMPGETNEXT en la simulacion es mucho mayor porque debe\n"
      "descartar los OIDs no nulos. Mientras que mediante SNMPGET se conoce el OID a consultar y \n"
      "se procede mas rapidamente\n\n")

print("###EJECUCION DEL PROGRAMA###")
# VARIABLES
version = 'v1'
community = 'security'
ip_addr = raw_input("Direccion IP del Switch/Hub:\n")
port = 161

snmp_engine = snmp_requests(version, community, ip_addr, port)
varBinds = [ObjectType(ObjectIdentity('1.3.6.1.2.1.1.1')), ]

t = time.time()
print("\nCONTENIDO DEL GRUPO SYSTEM:")

for ID in range(0,7):
    response = snmp_engine.snmpgetnext(varBinds)
    varBinds = [ObjectType(ObjectIdentity(response.varBinds[0][0])), ]
    if response.errorIndication:
        print 'errorIndication'
    elif response.errorStatus:
        print 'errorStatus'
    else:
        print str(response.varBinds[0][0]) + '\t' + str (response.varBinds[0][1])

elapsed = time.time() - t
print '\nTotal execution time: ' + str(elapsed) + ' seconds'
