from scapy.all import *
import time

def icmp_ping(IP_dst,n):
    conf.verb = 0

    t1 = time.time()
    for i in range (0,n):
        try:
            sr(IP(dst=IP_dst)/ICMP(),timeout=0.05)
        except:
            print("")

    t2 = time.time()
    print("Tiempo utilizado: "+str(t2 - t1))


