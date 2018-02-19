from __future__ import print_function

import Connect

OUTPUT = []

def print_vm(vm):
      if(vm.summary.runtime.powerState == "poweredOff"):
            VMState = "powered off"
      elif(vm.summary.runtime.powerState == "poweredOn"):
            VMState = "powered on"

      OUTPUT.append(vm.summary.config.name + " is running " + vm.summary.config.guestFullName + " and is " + VMState)
      print(vm.summary.config.name + " is running " + vm.summary.config.guestFullName + " and is " + VMState)

def main():
      si = Connect.ESXiConnect()
      content = si.RetrieveContent()
      
      for child in content.rootFolder.childEntity:
            if hasattr(child, 'vmFolder'):
                  datacenter = child
            vmFolder = datacenter.vmFolder
            vm_list = vmFolder.childEntity

            if len(vm_list) == 0:
                  OUTPUT.append("There are no virtual machines available")
                  print("There are no virtual machines available")
            else:
                  for vm in vm_list:
                        print_vm(vm)

      # print(OUTPUT)
      return 0

if __name__ == "__main__":
   main()
