from __future__ import print_function

import atexit
import ssl
import sys

from pyVim.connect import Disconnect, SmartConnect

#ESXi
ESXi_Host = "10.0.27.50"
ESXi_User = "root"
ESXi_Pass = "Nu141163695"
ESXi_Port = "443"

#vSphere
vSphere_Host = "10.0.27.55"
vSphere_User = "administrator@vsphere.local"
vSphere_Pass = "Nu141163695!"
vSphere_Port = "443"

context = None
if hasattr(ssl, "_create_unverified_context"):
    context = ssl._create_unverified_context()

def ESXiConnect():
    si = SmartConnect(host=ESXi_Host, user=ESXi_User, pwd=ESXi_Pass, port=ESXi_Port, sslContext=context)
    atexit.register(Disconnect, si)

    # if si:
    #     print("Connected to " + ESXi_Host)
    # if not si:
    #      print("Error Connecting to " + ESXi_Host)
    #      sys.exit()
    return si

def vSphereConnect():
    si = SmartConnect(host=vSphere_Host, user=vSphere_User, pwd=vSphere_Pass, port=vSphere_Port, sslContext=context)
    atexit.register(Disconnect, si)
    
    # if si:
    #     print("Connected to " + vSphere_Host)
    # if not si:
    #      print("Error Connecting to " + vSphere_Host)
    #      sys.exit()
    return si
