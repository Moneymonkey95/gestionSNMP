from snmp_library import *
from pysnmp.hlapi.asyncore import *
import threading
from system_group_ping_gonzalez import icmp_ping

# Email
from email.mime import multipart, text
import smtplib

# TrapReceiver
from pysnmp.carrier.asyncore.dispatch import AsyncoreDispatcher
from pysnmp.carrier.asyncore.dgram import udp, udp6, unix
from pyasn1.codec.ber import decoder
from pysnmp.proto import api
from snmp_library import *
from pysnmp.hlapi.asyncore import *


def ConfigureAlarm(version, IPdst,community,port,indexAlarm,indexTable,Value):
    snmp_engine = snmp_requests(version, community, IPdst, port)
    OID = '1.3.6.1.2.1.16.3.1.1.'+str(indexTable)+'.'+str(indexAlarm)
    varBinds = [ObjectType(ObjectIdentity(OID), Value)]
    snmp_engine.snmpset(varBinds)

def ConfigureFullAlarm(version, IPdst,community,port,indexAlarm):
    ConfigureAlarm(version, IPdst, community, port, indexAlarm, 12, Integer(2))
    ConfigureAlarm(version, IPdst, community, port, indexAlarm, 2, Integer(13))
    ConfigureAlarm(version, IPdst, community, port, indexAlarm, 3, ObjectIdentifier('1.3.6.1.2.1.5.8.0'))
    ConfigureAlarm(version, IPdst, community, port, indexAlarm, 4, Integer(2))
    ConfigureAlarm(version, IPdst, community, port, indexAlarm, 7, Integer(100))
    ConfigureAlarm(version, IPdst, community, port, indexAlarm, 8, Integer(20))
    ConfigureAlarm(version, IPdst, community, port, indexAlarm, 9, Integer(166))
    ConfigureAlarm(version, IPdst, community, port, indexAlarm, 10, Integer(0))
    ConfigureAlarm(version, IPdst, community, port, indexAlarm, 11, OctetString("Mario"))
    ConfigureAlarm(version, IPdst, community, port, indexAlarm, 12, Integer(1))

def GetFreeTrap():
    snmp_engine = snmp_requests(version, community, IPdst, port)
    OID = '1.3.6.1.4.1.43.10.10.3.0'
    varBinds = [ObjectType(ObjectIdentity(OID),)]
    result = snmp_engine.snmpget(varBinds)
    return result.varBinds[0][1]

def ConfigureTrap(version, IPdst,community,port,indexTrap,indexTable,Value):
    snmp_engine = snmp_requests(version, community, IPdst, port)
    OID = '1.3.6.1.4.1.43.10.10.2.1.'+str(indexTable)+'.'+str(indexTrap)
    varBinds = [ObjectType(ObjectIdentity(OID), Value)]
    result = snmp_engine.snmpset(varBinds)
    return result

def ConfigureEvent(version, IPdst,community,port,indexEvent,indexTable,Value):
    snmp_engine = snmp_requests(version, community, IPdst, port)
    OID = '1.3.6.1.2.1.16.9.1.1.'+str(indexTable)+'.'+str(indexEvent)
    varBinds = [ObjectType(ObjectIdentity(OID), Value)]
    result = snmp_engine.snmpset(varBinds)
    return result

def PrintResponse(response):
    if response.errorIndication:
        print 'errorIndication'
    elif response.errorStatus:
        print 'errorStatus'
    else:
        print 'varBinds'
        print str(response.varBinds[0][0]) + '\t' + str(response.varBinds[0][1])

###############################################

# Esta funcion es la que envia el mensaje
def send_msg(body):

    fromaddr = "gestiongonzalez2@gmail.com"
    toaddr = "gestiongonzalez2@gmail.com"
    password = "gestiongonzalez"

    msg = multipart.MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Alarm ICMP 100 Ping"

    msg.attach(text.MIMEText(body, 'plain'))


    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(fromaddr, password)
    cuerpo = msg.as_string()
    server.sendmail(fromaddr, toaddr, cuerpo)

#se queda escuchandoa recivir un trap
# noinspection PyUnusedLocal
def cbFun(transportDispatcher, transportDomain, transportAddress, wholeMsg):
    while wholeMsg:
        msgVer = int(api.decodeMessageVersion(wholeMsg))
        if msgVer in api.protoModules:
            pMod = api.protoModules[msgVer]
        else:
            print('Unsupported SNMP version %s' % msgVer)
            return
        reqMsg, wholeMsg = decoder.decode(wholeMsg, asn1Spec=pMod.Message(),)
        print('Notification message from %s:%s: ' % (transportDomain, transportAddress))
        send_msg("contenido del mensaje")

        reqPDU = pMod.apiMessage.getPDU(reqMsg)
        text = ''
        if reqPDU.isSameTypeWith(pMod.TrapPDU()):
            if msgVer == api.protoVersion1:
                text = text + 'Enterprise: ' + pMod.apiTrapPDU.getEnterprise(reqPDU).prettyPrint() + '\n' #coger informacion del paquete.
                # Incluir el resto de campos del trap que se consideren oportunos

                varBinds = pMod.apiTrapPDU.getVarBinds(reqPDU)
            else:
                varBinds = pMod.apiPDU.getVarBinds(reqPDU)
            # Incluir el contenido de las varBinds en el correo electronico
    return wholeMsg

def escucharTrap():
    print("Escucho")
    # se queda escuchando, lanza callback (cb) cuando recibe paquyete
    transportDispatcher = AsyncoreDispatcher()

    transportDispatcher.registerRecvCbFun(cbFun)

    # UDP/IPv4
    transportDispatcher.registerTransport(
        udp.domainName, udp.UdpSocketTransport().openServerMode(('0.0.0.0', 162))
    )

    # UDP/IPv6
    transportDispatcher.registerTransport(
        udp6.domainName, udp6.Udp6SocketTransport().openServerMode(('::1', 162))
    )

    transportDispatcher.jobStarted(1)

    try:
        # Dispatcher will never finish as job#1 never reaches zero
        transportDispatcher.runDispatcher()
    except:
        transportDispatcher.closeDispatcher()

        raise

def enviarPings():
    print("Envio ICMP")
    time.sleep(1)
    icmp_ping("155.210.157.203", 200)

################################################

indexAlarm = 16
indexEvent = 166
version = 'v1'
IPdst = '155.210.157.203'
community = 'private'
port = 161
"""
CreateAlarm(version, IPdst,community,port,indexAlarm)
UnderCreationAlarm(version, IPdst,community,port,indexAlarm)
ConfigureFullAlarm(version, IPdst,community,port,indexAlarm)

indexTrap=int(GetFreeTrap())

myIndexTrap = 4

ConfigureTrap(version, IPdst,community,port,myIndexTrap,7,Integer(3))
ConfigureTrap(version, IPdst,community,port,myIndexTrap,2,OctetString('155.210.157.139'))
ConfigureTrap(version, IPdst,community,port,myIndexTrap,4,OctetString("Public"))
ConfigureTrap(version, IPdst,community,port,myIndexTrap,5,OctetString("0xFFFFFFFF"))
ConfigureTrap(version, IPdst,community,port,myIndexTrap,6,Integer(0))


ConfigureEvent(version, IPdst,community,port,indexEvent,7,Integer(1))
ConfigureEvent(version, IPdst,community,port,indexEvent,6,OctetString("Mario"))
ConfigureEvent(version, IPdst,communityi,port,indexEvent,4,OctetString("Public"))
ConfigureEvent(version, IPdst,community,port,indexEvent,3,Integer(4))
ConfigureEvent(version, IPdst,community,port,indexEvent,2,OctetString('Not monitor'))
"""

#ConfigureFullAlarm(version, IPdst,community,port,indexAlarm)
print("Empiezo")

t1 = threading.Thread(target=escucharTrap)
t2 = threading.Thread(target=enviarPings)

t1.start()
t2.start()




