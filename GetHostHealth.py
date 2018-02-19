from __future__ import print_function

import re

import humanize
import pyVmomi
from pyVmomi import vim, vmodl

import Connect

OUTPUT = []

def get_host_info(host):
    try:
        Host_name = host.name
        TotalMemoryUsage = str(float(host.summary.quickStats.overallMemoryUsage / 1024))
        TotalCpuUsage = str(host.summary.quickStats.overallCpuUsage)
        Color = str(host.summary.overallStatus)

        Memory = humanize.naturalsize(host.hardware.memorySize,binary=True)
        Temp = re.findall("\d+\.\d+", Memory)
        MemoryCapacity = str(' '.join(str(p) for p in Temp))

        OUTPUT.append("Host " + Host_name + " is " + Color + "with CPU running at " + TotalCpuUsage + " MegaHertZ and is using " + TotalMemoryUsage + " out of " + MemoryCapacity + " gigabytes of memory")
        # print(OUTPUT)
    
    except Exception as error:
        print(error)
        pass

def main():
    try:
        si = Connect.vSphereConnect()
        content = si.RetrieveContent()

        for datacenter in content.rootFolder.childEntity:
            if hasattr(datacenter.vmFolder, 'childEntity'):
                hostFolder = datacenter.hostFolder
                computeResourceList = hostFolder.childEntity
                for computeResource in computeResourceList:
                    hostList = computeResource.host
                    for host in hostList:
                        get_host_info(host)

    except vmodl.MethodFault as error:
        print("Caught vmodl fault : " + error.msg)
        return -1
    return 0

if __name__ == "__main__":
    main()
