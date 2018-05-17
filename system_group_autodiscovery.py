import os
import sys
from scapy.all import *
from snmp_library import *
from pysnmp.hlapi.asyncore import *

def GetMAC (ans):
    MAC = str(ans)
    inicio = MAC.find("hwsrc=")+6
    fin = MAC.rfind("psrc=")-1
    return MAC[inicio:fin]

def SendARP_WhoHas(IP_src,IP_dst):
    ansARP, unansARP = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(op=ARP.who_has, psrc=IP_src, pdst=IP_dst), timeout=0.3)
    return ansARP, unansARP

def SendSYNTCP(IP_src,IP_dst,port_src,port_dst):
    ip = IP(src=IP_src, dst=IP_dst)
    tcp = TCP(sport=port_src, dport=port_dst, flags='S', seq=1000)
    ansSYN, unansSYN = sr(ip / tcp ,timeout=0.3)
    return ansSYN

def SendACKTCP(IP_src,IP_dst,port_src,port_dst,ansSYN):
    ip = IP(src=IP_src, dst=IP_dst)
    send(ip / TCP(sport=port_src, dport=port_dst, flags='A', seq=ansSYN.ack, ack=ansSYN.seq + 1),timeout=0.3)

conf.verb=0

IP_dst='155.210.157.4'
IP_src='155.210.157.139'

ipList=[]
macList=[]
port_List=[]
snmpList = []

#TCP parametros:
freq_ports = [21,22,23,25,80,161,443]
port_dst = 80
port_src = 80

#SNMP parametros:
version = 'v1'
community = 'public'
port = 161
OID= '1.3.6.1.2.1.1.1.0' #SYS DESCRIPTION

for i in range (1,255):
    IP_dst=("155.210.157."+str(i))

    #GET MAC
    ansARP, unansARP = SendARP_WhoHas(IP_src, IP_dst)
    MAC_dst = "Not conected"
    for rcvARP in ansARP:
        try:
            MAC_dst = GetMAC(rcvARP)
        except:
            print("ERROR")

    ipList.append(IP_dst)
    macList.append("\t"+str(MAC_dst))
    port_List.append(" ")
    #print (result[i-1])
    #time.sleep(2)
    snmpList.append(" ")
    if (MAC_dst != "Not conected"):
        #CHECKEO DE PUERTOS TCP
        for port_dst in freq_ports:
            ansSYN = SendSYNTCP(IP_src,IP_dst,port_src,port_dst)
            for rcvSYN in ansSYN:
                try:
                    if (str(rcvSYN).find("flags=SA") > 1):
                        port_List[i-1] += " " + str(port_dst)
                        SendACKTCP(IP_src,IP_dst,port_src,port_dst,ansSYN)
                except:
                    print("")


        #CHECKEO DE SOPORTE SNMP
        snmpList[i - 1] += "\tSNMP:"
        snmp_engine = snmp_requests(version, community, IP_dst, port)
        varBinds = [ObjectType(ObjectIdentity(OID), )]
        result = snmp_engine.snmpget(varBinds)
        try:
            snmpList[i - 1] += str(result.varBinds[0][1])
        except:
            snmpList[i - 1] += "/"


for i in range (0,len(ipList)):
    print(str(ipList[i]) +"\t"+ str(macList[i])  +"\t"+ str(port_List[i]) +"\t"+ str(snmpList[i]) )



