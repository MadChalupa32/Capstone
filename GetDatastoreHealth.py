from __future__ import print_function

import atexit
import re
import ssl

import humanize
import pyVmomi
from pyVmomi import vim, vmodl

import Connect

OUTPUT = []

def get_datastore_info(datastore):
    Datastore_name = datastore.summary.name
    TotalStorageUsage = datastore.summary.capacity
    TotalStorageFree = datastore.summary.freeSpace
    FreeSpaceRatio = (float(TotalStorageFree) / TotalStorageUsage) * 100
    FreePercent = str("%.0f" % (100 - FreeSpaceRatio))
    
    c = humanize.naturalsize(TotalStorageFree, binary=True)
    temp = re.findall("\d+\.\d+", c)
    Free = ' '.join(str(p) for p in temp)

    c2 = humanize.naturalsize(TotalStorageUsage, binary=True)
    temp2 = re.findall("\d+\.\d+", c2)
    Used = ' '.join(str(p) for p in temp2)
    


    OUTPUT.append("Datastore " + Datastore_name + " is " + FreePercent + "%" + " full with " + Free + " out of " + Used + " gigabytes free")
    # print("Datastore " + Datastore_name + " is " + FreePercent + "%" + " full with " + Free + " out of " + Used + " gigabytes free")


def main():
    try:
        si = Connect.vSphereConnect()
        content = si.RetrieveContent()

        for datacenter in content.rootFolder.childEntity:
            for d in datacenter.datastore:
                get_datastore_info(d)

    except vmodl.MethodFault as error:
        print("Caught vmodl fault : " + error.msg)
        return -1
    return 0

if __name__ == "__main__":
    main()
