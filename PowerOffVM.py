from __future__ import print_function
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim, vmodl

import argparse
import atexit
import getpass
import sys
import ssl, Connect, VMtoList

vm_name = ""
OUTPUT = []

def get_status(ObjList):
      for vm in ObjList:
            if vm.name in vm_name:
                  if(vm.summary.runtime.powerState == "poweredOn"):
                        vm.PowerOff()
                        OUTPUT.append("The virtual machine " + vm_name + " has been powered off successfully")
                        # print("The virtual machine " + vm_name + " has been powered off successfully")
                  if(vm.summary.runtime.powerState == "poweredOff"):
                        OUTPUT.append("The virtual machine " + vm_name + " is already off")
                        # print("The virtual machine " + vm_name + " is already off")
                        

def main():
   try:
      VMtoList.VMNAMELIST[:] = []
      VMtoList.main()
      vm_list = VMtoList.VMNAMELIST

      if not len(vm_list):
            OUTPUT.append("No virtual machines available for power off")
            #print("No virtual machines available for power off")
            sys.exit()

      si = Connect.ESXiConnect()
      content = si.RetrieveContent()
      objView = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
      ObjList = objView.view
      objView.Destroy()

      get_status(ObjList)

      # print(OUTPUT)

   except vmodl.MethodFault as e:
      print("Caught vmodl fault : " + e.msg)
   except Exception as e:
      print("Caught Exception : " + str(e))
      return 0

if __name__ == "__main__":
   main()