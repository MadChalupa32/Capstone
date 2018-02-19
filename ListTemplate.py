from __future__ import print_function

import atexit
import ssl

import Connect

OUTPUT = []

def append_vm(vm):
      OUTPUT.append(vm.summary.config.name)
    #   print(vm.summary.config.name)

def query_list(si):
      content = si.RetrieveContent()
      for child in content.rootFolder.childEntity:
            if hasattr(child, 'vmFolder'):
                  datacenter = child
            vmFolder = datacenter.vmFolder
            vm_list = vmFolder.childEntity
            for vm in vm_list:
                if(vm.summary.config.template == True):
                    append_vm(vm)
            print(OUTPUT)

def main():
      si = Connect.vSphereConnect()
      query_list(si)
      #print(VMNAMELIST)

      return 0

if __name__ == "__main__":
   main()
