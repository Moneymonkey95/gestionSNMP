# Imports
from snmp_library import *
from pysnmp.hlapi.asyncore import *
import time


# Variables in my program
version = 'v2c'
community = 'public'
ip_addr = '155.210.157.40'
port = 161

# SNMP engine inicialization
snmp_engine = snmp_requests(version, community, ip_addr, port)


#######################################################################
#                            SNMP GET                                 #
#######################################################################

varBinds = [ObjectType(ObjectIdentity('1.3'),OctetString('calabaza'))]

t = time.time()

# Send request
response = snmp_engine.snmpget(varBinds)

if response.errorIndication:
    print 'errorIndication'
elif response.errorStatus:
    print 'errorStatus'
else:
    print 'varBinds'

# ending time counter
elapsed = time.time() - t
print 'Total execution time: ' + str(elapsed) + ' seconds'