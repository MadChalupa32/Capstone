from __future__ import print_function

import pyVmomi
from pyVmomi import vim, vmodl

import Connect

OUTPUT = []

def get_datastore_info(datastore):
    Datastore_name = datastore.summary.name

    OUTPUT.append(Datastore_name)
    # print(Datastore_name)

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

    # print(OUTPUT)
    return 0

if __name__ == "__main__":
    main()
