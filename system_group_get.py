# IMPORTS
from snmp_library import *
from pysnmp.hlapi.asyncore import *
import time

print("##################################################\n"
      "                    SNMP_GET                      \n"
      "            Mario Gonzalez  | 2018                \n"
      "##################################################\n")

print("###CUESTIONES TEORICAS###\n"
      "Ventajas e inconvenientes de solicitar mas de un OID mediante 1 solo PDU SNMP GET:\n"
      "\t+ Menor overhead\n"
      "\t+ Menor retardo\n"
      "\t- Solicitar un OID que no esta asignado para v1, no devuelve ningun valor para ningun OID\n\n"
      "El contenido de VarBinds es una tabla que contiene en las posiciones [n][0] el OID a consultar\n"
      "y en [n][1] el valor, por defecto, NULL para una SNMP GET.\n\n"
      "En la version v1 no podemos saber que objeto ha provocado el error mientras que para v2c si \n"
      "porque muestra unicamente ese campo sin valor\n")

# VARIABLES
version = 'v1'
community = 'public'
ip_addr = raw_input("###EJECUCION DEL PROGRAMA###\nDireccion IP del Switch/Hub:\n")
port = 161
modo = input("\nModo de funcionamiento del script:\n1. Solicitar todos los objetos del grupo System con un SNMPGET para "
             "cada uno de ellos.\n2. Solicitar todos los objetos del grupo System mediante un Unico PDU.\n3. Solicitar "
             "el grupo System con un OID mal formado.\n")


snmp_engine = snmp_requests(version, community, ip_addr, port)
varBinds = [ObjectType(ObjectIdentity('1.3.6.1.2.1.1.1.0')), ]
t = time.time()

if (modo == 1): #SOLICITUD MEDIANTE UN PDU DISTINTO PARA CADA SNMPGET
    # FORMACION DEL PDU
    varBinds1 = [ObjectType(ObjectIdentity('1.3.6.1.2.1.1.1.0')), ]
    varBinds2 = [ObjectType(ObjectIdentity('1.3.6.1.2.1.1.2.0')), ]
    varBinds3 = [ObjectType(ObjectIdentity('1.3.6.1.2.1.1.3.0')), ]
    varBinds4 = [ObjectType(ObjectIdentity('1.3.6.1.2.1.1.4.0')), ]
    varBinds5 = [ObjectType(ObjectIdentity('1.3.6.1.2.1.1.5.0')), ]
    varBinds6 = [ObjectType(ObjectIdentity('1.3.6.1.2.1.1.6.0')), ]
    varBinds7 = [ObjectType(ObjectIdentity('1.3.6.1.2.1.1.7.0')), ]

    response1 = snmp_engine.snmpget(varBinds1)
    response2 = snmp_engine.snmpget(varBinds2)
    response3 = snmp_engine.snmpget(varBinds3)
    response4 = snmp_engine.snmpget(varBinds4)
    response5 = snmp_engine.snmpget(varBinds5)
    response6 = snmp_engine.snmpget(varBinds6)
    response7 = snmp_engine.snmpget(varBinds7)

    elapsed = time.time() - t
    print("\nCONTENIDO DEL GRUPO SYSTEM:")
    print '1.3.6.1.2.1.1.1.0' + '\t' + tools().var_type(response1.varBinds[0][1]) + '\t' + str(response1.varBinds[0][1])
    print '1.3.6.1.2.1.1.2.0' + '\t' + tools().var_type(response2.varBinds[0][1]) + '\t' + str(response2.varBinds[0][1])
    print '1.3.6.1.2.1.1.3.0' + '\t' + tools().var_type(response3.varBinds[0][1]) + '\t' + str(response3.varBinds[0][1])
    print '1.3.6.1.2.1.1.4.0' + '\t' + tools().var_type(response4.varBinds[0][1]) + '\t' + str(response4.varBinds[0][1])
    print '1.3.6.1.2.1.1.5.0' + '\t' + tools().var_type(response5.varBinds[0][1]) + '\t' + str(response5.varBinds[0][1])
    print '1.3.6.1.2.1.1.6.0' + '\t' + tools().var_type(response6.varBinds[0][1]) + '\t' + str(response6.varBinds[0][1])
    print '1.3.6.1.2.1.1.7.0' + '\t' + tools().var_type(response7.varBinds[0][1]) + '\t' + str(response7.varBinds[0][1])

    print '\nTotal execution time: ' + str(elapsed) + ' seconds'

elif (modo == 2): #SOLICITUD MEDIANTE UN UNICO PDU
    # FORMACION DEL PDU
    for ID in range(1,8) :      ##Solo valido de (1,8), el excedente provoca el error solicitado.
        varBinds = varBinds + [ObjectType(ObjectIdentity('1.3.6.1.2.1.1.' + str(ID) + '.0')), ]
    response = snmp_engine.snmpget(varBinds)

    if response.errorIndication:
        print 'errorIndication'
    elif response.errorStatus:
        print 'errorStatus'
    else:
        elapsed = time.time() - t
        print("\nCONTENIDO DEL GRUPO SYSTEM:")
        for ID in range(1,8) : #Solo valido de (1,8), el excedente provoca el error solicitado.
            print '1.3.6.1.2.1.1.' + str(ID) + '.0' + '\t' + tools().var_type(response.varBinds[ID-1][1]) +'\t' + str(response.varBinds[ID-1][1])
        print '\nTotal execution time: ' + str(elapsed) + ' seconds'


elif (modo == 3): #PETICION CON ERROR, SE SOLICITA EL RANGO (1,9) CON EL ULTIMO VALOR NO EXISTENTE
    # FORMACION DEL PDU
    for ID in range(1, 9):  ##Solo valido de (1,8), el excedente provoca el error solicitado.
        varBinds = varBinds + [ObjectType(ObjectIdentity('1.3.6.1.2.1.1.' + str(ID) + '.0')), ]
    response = snmp_engine.snmpget(varBinds)

    if response.errorIndication:
        print 'errorIndication'
    elif response.errorStatus:
        print 'errorStatus'
    else:
        elapsed = time.time() - t
        print("\nCONTENIDO DEL GRUPO SYSTEM:")
        for ID in range(1, 9):  # Solo valido de (1,8), el excedente provoca el error solicitado.
            print '1.3.6.1.2.1.1.' + str(ID) + '.0' + '\t' + tools().var_type(
                response.varBinds[ID - 1][1]) + '\t' + str(response.varBinds[ID - 1][1])
        print '\nTotal execution time: ' + str(elapsed) + ' seconds'

else:
    print("\nIntroduce 1, 2 o 3 para la correcta ejecucion del programa")