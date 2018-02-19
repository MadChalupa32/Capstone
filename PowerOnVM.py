from __future__ import print_function

import sys

from pyVmomi import vim, vmodl

import Connect
import VMtoList

vm_name = ""
OUTPUT = []

def get_status(ObjList):

      vmlist = []
      for vm in ObjList:
            vmlist.append(vm.name)

      for vm in ObjList:
            if not vm_name in vmlist:
                  OUTPUT.append(vm_name + " is not an active Virtual Machine")
                  break
            elif vm.name in vm_name:
                  if(vm.summary.runtime.powerState == "poweredOff"):
                        vm.PowerOn()
                        OUTPUT.append("The virtual machine " + vm_name + " has been powered on successfully")
                        # print("The virtual machine " + vm_name + " has been powered on successfully")
                  if(vm.summary.runtime.powerState == "poweredOn"):
                        OUTPUT.append("The virtual machine " + vm_name + " is already on")
                        # print("The virtual machine " + vm_name + " is already on")
                        

def main():
   try:
      VMtoList.VMNAMELIST[:] = []
      VMtoList.main()
      vm_list = VMtoList.VMNAMELIST

      if not len(vm_list):
            OUTPUT.append("No virtual machines available for power on")
            print("No virtual machines available for power on")
            
      si = Connect.ESXiConnect()
      content = si.RetrieveContent()
      objView = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
      ObjList = objView.view
      objView.Destroy()

      get_status(ObjList)

      print(OUTPUT)

   except vmodl.MethodFault as e:
      print("Caught vmodl fault : " + e.msg)
   except Exception as e:
      print("Caught Exception : " + str(e))
      return 0

if __name__ == "__main__":
   main()
