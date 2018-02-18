from __future__ import print_function

import atexit
import ssl

from pyVim.connect import Disconnect, SmartConnect

import Connect

OUTPUT = []
vm_name = "test4"

def destroy_vm(vm, si):
    # print(str(vm.summary.config.name) + " " + str(vm.summary.config.uuid) + " " + str(vm.summary.config.template))
    VM = si.content.searchIndex.FindByUuid(None, vm.summary.config.uuid, True, False)
    
    VM.PowerOff()
    # print("Powering off " + str(vm.name))

    VM.Destroy_Task()
    # print(str(vm.name) + " has been deleted successfully")
    OUTPUT.append(vm_name + " has been deleted successfully")

def query_list(si):
    content = si.RetrieveContent()

    for child in content.rootFolder.childEntity:
            if hasattr(child, 'vmFolder'):
                  datacenter = child
            vmFolder = datacenter.vmFolder
            vm_list = vmFolder.childEntity

            vmlist = []
            for vm in vm_list:
                vmlist.append(vm.name)

            if(len(vm_list) <= 0):
                OUTPUT.append("There are no virtual machines available")
                break
            elif(not vm_name in vmlist):
                OUTPUT.append(vm_name + " is not an active Virtual Machine")
                # print(vm_name + " is not an active Virtual Machine")
            else:
                for vm in vm_list:
                    if(vm.summary.config.template == False):
                        if(vm.name == vm_name):
                            destroy_vm(vm, si) 
  

def main():
    try:
        si = Connect.vSphereConnect()

        query_list(si)

    except Exception as e:
      print("Caught Exception : " + str(e))
      return 0
    
    print(OUTPUT)
    return 0

if __name__ == "__main__":
   main()
