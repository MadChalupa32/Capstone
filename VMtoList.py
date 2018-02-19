from __future__ import print_function

import atexit
import ssl

import Connect

VMNAMELIST=[]
def append_vm(vm):
      VMNAMELIST.append(vm.summary.config.name)

def query_list(si):
      content = si.RetrieveContent()
      for child in content.rootFolder.childEntity:
            if hasattr(child, 'vmFolder'):
                  datacenter = child
            vmFolder = datacenter.vmFolder
            vm_list = vmFolder.childEntity
            for vm in vm_list:
                  append_vm(vm)

def main():
      si = Connect.ESXiConnect()
      query_list(si)
      #print(VMNAMELIST)

      return 0

if __name__ == "__main__":
   main()
