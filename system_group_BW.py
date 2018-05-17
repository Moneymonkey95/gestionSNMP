# Imports
import sys
from snmp_library import *
from pysnmp.hlapi.asyncore import *
import time
import numpy as np
import matplotlib.pyplot as plt
from pylab import *

class bcolors:
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    PURPLE = '\033[95m'
    GREY = '\33[90m'


OID_interfaces = '1.3.6.1.2.1.2.2'
OID_description = '1.3.6.1.2.1.2.2.1.2'
OID_ifindex = '1.3.6.1.2.1.2.2.1.1'
port = 161
Octects = ''
inOctects = '.1.10'
outOctects = '.1.16'

terminal = input("---- BANDWIDTH GRAPTH v0.1 ----"
    "\nQue desea visualizar HUB o SWITCH?"
    "\n1. HUB \n2. SWITCH\n")
ip_addr = raw_input('Ip del equipo?\n')
if terminal == 1:
    community = 'security'
    version = 'v1'
    #ifIndex='.39534'
    Octects = inOctects
elif terminal == 2:
    community = 'public'
    version = 'v2c'
else:
    print('Sintaxis no admitida')


snmp_engine = snmp_requests(version, community, ip_addr, port)

varBinds2 = [ObjectType(ObjectIdentity(OID_description), )]
response = snmp_engine.snmpgetnext(varBinds2)

print('Puerto?')
ifID = 0
while(str(response.varBinds[0][0]).startswith(OID_description)):
    time.sleep(0.5)
    ifID += 1
    print(str(ifID) + '\t' + response.varBinds[0][1])
    varBinds2 = [ObjectType(ObjectIdentity(response.varBinds[0][0]), )]
    response = snmp_engine.snmpgetnext(varBinds2)

ifIndex = input()
varBinds3 = [ObjectType(ObjectIdentity(OID_ifindex), )]
response = snmp_engine.snmpgetnext(varBinds3)
ifIndex -= 1
while ifIndex >0:
    time.sleep(0.5)
    varBinds3 = [ObjectType(ObjectIdentity(response.varBinds[0][0]), )]
    response = snmp_engine.snmpgetnext(varBinds3)
    ifIndex -= 1
print('El ID del puerto es:\t' + str(response.varBinds[0][1]))
ifIndex = '.'+str(response.varBinds[0][1])

varBinds3 = [ObjectType(ObjectIdentity(OID_description), )]
response = snmp_engine.snmpgetnext(varBinds2)


varBinds = [ObjectType(ObjectIdentity(OID_interfaces + inOctects + ifIndex), )] + [ObjectType(ObjectIdentity('1.3.6.1.2.1.1.3.0'), ) ]
varBinds2 = [ObjectType(ObjectIdentity(OID_interfaces + outOctects + ifIndex), )]


t=list()
bytes=list()
b2=list()

tpol = input("Cada cuanto tiempo quieres actualizar la grafica?\n")

t.append(0) # Primer valor temporal = 0
bytes.append(0) # Primera medida de BW = 0
b2.append(0) # Primera medida de BW = 0
response = snmp_engine.snmpget(varBinds)

#Valores anteriores
prev_B = response.varBinds[0][1]
prev_T = response.varBinds[1][1]
i=0
prev_B2=0
plt.ion()

while 1:
    time.sleep(tpol)
    i = i + 1
    response = snmp_engine.snmpget(varBinds)
    actual_B = int(response.varBinds[0][1])
    actual_T = int(response.varBinds[1][1])
    bytes.append((actual_B-prev_B)*8/1000/tpol)
    t.append((actual_T-prev_T)/100)
    if terminal==1:
        plt.plot(t,bytes,'r')
        plt.xlabel('Time [s]. Sync whit SysUPTime')
        plt.ylabel('Bandwidth [Kbps]')
        plt.title('Bandwidth Live Graph of  ' + str(ip_addr) +'  if:'+ifIndex)
        plt.grid(True)
        plt.pause(0.0025)
    elif terminal==2:
        response2 = snmp_engine.snmpget(varBinds)
        actual_B2 = int(response2.varBinds[0][1])
        b2.append((actual_B2-prev_B2)*8/1000/tpol)
        prev_B2=actual_B2;

        plt.subplot(2, 1, 1)
        plt.plot(t, bytes, 'r')
        plt.xlabel('Time [s]. Sync whit SysUPTime')
        plt.ylabel('Bandwidth [Kbps]')
        plt.title('Input Bandwidth Live Graph of  ' + str(ip_addr) + '  if:' + ifIndex)
        plt.grid(True)
        plt.pause(0.0025)

        plt.subplot(2, 1, 2)
        plt.plot(t, b2, 'b')
        plt.xlabel('Time [s]. Sync whit SysUPTime')
        plt.ylabel('Bandwidth [Kbps]')
        plt.title('Output Bandwidth Live Graph of  ' + str(ip_addr) + '  if:' + ifIndex)
        plt.grid(True)
        plt.pause(0.0025)

    prev_B=actual_B
    i += 1

