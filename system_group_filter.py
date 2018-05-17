
from snmp_library import *
from pysnmp.hlapi.asyncore import *
from scapy import *
import sys



def setSNMP(version, community, IPdst, port, OID, value):
    snmp_engine = snmp_requests(version, community, IPdst, port)
    varBinds = [ObjectType(ObjectIdentity(OID), value)]
    result = snmp_engine.snmpset(varBinds)
    return result.varBinds[0][1]

def configureFilterEntry(version, community, IPdst, port, filterEntryOID):
    print(setSNMP(version, community, IPdst, port, filterEntryOID + ".11.1", Integer(4)))

    print(setSNMP(version, community, IPdst, port, filterEntryOID + ".11.1", Integer(2)))
    print(setSNMP(version, community, IPdst, port, filterEntryOID + ".2.1", Integer(1)))
    print(setSNMP(version, community, IPdst, port, filterEntryOID + ".3.1", Integer(34)))
    print(setSNMP(version, community, IPdst, port, filterEntryOID + ".4.1", OctetString(hexValue='01bb')))
    print(setSNMP(version, community, IPdst, port, filterEntryOID + ".5.1", OctetString(hexValue='FFFF')))
    print(setSNMP(version, community, IPdst, port, filterEntryOID + ".6.1", OctetString(hexValue='0000')))
    print(setSNMP(version, community, IPdst, port, filterEntryOID + ".7.1", Integer(0)))
    print(setSNMP(version, community, IPdst, port, filterEntryOID + ".8.1", Integer(7)))
    print(setSNMP(version, community, IPdst, port, filterEntryOID + ".9.1", Integer(0)))
    print(setSNMP(version, community, IPdst, port, filterEntryOID + ".10.1", OctetString("Mario")))

    print(setSNMP(version, community, IPdst, port, filterEntryOID + ".11.1", Integer(1)))

def configureChannelEntry(version, community, IPdst, port, filterEntryOID):
    print(setSNMP(version, community, IPdst, port, filterEntryOID + ".12.1", Integer(4)))
    print(setSNMP(version, community, IPdst, port, filterEntryOID + ".12.1", Integer(2)))

    print(setSNMP(version, community, IPdst, port, filterEntryOID + ".2.1", Integer(3)))
    print(setSNMP(version, community, IPdst, port, filterEntryOID + ".3.1", Integer(1)))
    print(setSNMP(version, community, IPdst, port, filterEntryOID + ".4.1", Integer(1)))
    print(setSNMP(version, community, IPdst, port, filterEntryOID + ".10.1", OctetString("HTTPS")))
    print(setSNMP(version, community, IPdst, port, filterEntryOID + ".11.1", OctetString("Mario")))
    print(setSNMP(version, community, IPdst, port, filterEntryOID + ".12.1", Integer(1)))

def representar():
    OID_interfaces = '1.3.6.1.2.1.2.2'
    OID_description = '1.3.6.1.2.1.2.2.1.2'
    OID_ifindex = '1.3.6.1.2.1.2.2.1.1'
    ifIndex = 3


    varBinds = [ObjectType(ObjectIdentity(OID_interfaces + inOctects + ifIndex), )] + [ObjectType(ObjectIdentity('1.3.6.1.2.1.1.3.0'), )]
    varBinds2 = [ObjectType(ObjectIdentity(OID_interfaces + outOctects + ifIndex), )]

    t = list()
    bytes = list()
    b2 = list()

    tpol = input("Cada cuanto tiempo quieres actualizar la grafica?\n")

    t.append(0)  # Primer valor temporal = 0
    bytes.append(0)  # Primera medida de BW = 0
    b2.append(0)  # Primera medida de BW = 0
    response = snmp_engine.snmpget(varBinds)

    # Valores anteriores
    prev_B = response.varBinds[0][1]
    prev_T = response.varBinds[1][1]
    i = 0
    prev_B2 = 0
    plt.ion()

    while 1:
        time.sleep(tpol)
        i = i + 1
        response = snmp_engine.snmpget(varBinds)
        actual_B = int(response.varBinds[0][1])
        actual_T = int(response.varBinds[1][1])
        bytes.append((actual_B - prev_B) * 8 / 1000 / tpol)
        t.append((actual_T - prev_T) / 100)
        if terminal == 1:
            plt.plot(t, bytes, 'r')
            plt.xlabel('Time [s]. Sync whit SysUPTime')
            plt.ylabel('Bandwidth [Kbps]')
            plt.title('Bandwidth Live Graph of  ' + str(ip_addr) + '  if:' + ifIndex)
            plt.grid(True)
            plt.pause(0.0025)
        elif terminal == 2:
            response2 = snmp_engine.snmpget(varBinds)
            actual_B2 = int(response2.varBinds[0][1])
            b2.append((actual_B2 - prev_B2) * 8 / 1000 / tpol)
            prev_B2 = actual_B2;

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

        prev_B = actual_B
        i += 1

version = 'v1'
IPdst = '155.210.157.182'
community = 'public'
port = 161

filterEntryOID="1.3.6.1.2.1.16.7.1.1"
channelEntryOID="1.3.6.1.2.1.16.7.2.1"

configureFilterEntry(version, community, IPdst, port, filterEntryOID)
configureChannelEntry(version, community, IPdst, port, channelEntryOID)


#OctetString(hexValue='F23C'