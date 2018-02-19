from __future__ import print_function

from pyVmomi import vim

import Connect

clone_name = ""
clone_datastore = "SAN"
clone_resourcepool = "CB-ResPool"
clone_template = ""
OUTPUT = []


def wait_for_task(task):
    task_done = False
    while not task_done:
        if task.info.state == 'success':
            OUTPUT.append(clone_name + " was created successfully")
            return task.info.result
            
        if task.info.state == 'error':
            print(task.info.error.msg)
            OUTPUT.append(task.info.error.msg)
            task_done = True


def get_info(content, vimtype, name):
    obj = None
    container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
    for c in container.view:
        if name:
            if c.name == name:
                obj = c
                break
        else:
            obj = c
            break

    return obj

def clone_vm(content, template_name, vm_name, si, datastore_name, resource_pool, power_on):

    destfolder = get_info(content, [vim.Folder], None)
    datastore = get_info(content, [vim.Datastore], datastore_name)
    

    if resource_pool:
        resource_pool = get_info(content, [vim.ResourcePool], resource_pool)

    vmconf = vim.vm.ConfigSpec()

    podsel = vim.storageDrs.PodSelectionSpec()
    pod = get_info(content, [vim.StoragePod], None)
    podsel.storagePod = pod

    storagespec = vim.storageDrs.StoragePlacementSpec()
    storagespec.podSelectionSpec = podsel
    storagespec.type = 'create'
    storagespec.folder = destfolder
    storagespec.resourcePool = resource_pool
    storagespec.configSpec = vmconf


    try:
        rec = content.storageResourceManager.RecommendDatastores(storageSpec=storagespec)
        rec_action = rec.recommendations[0].action[0]
        real_datastore_name = rec_action.destination.name
    except:
        real_datastore_name = template_name.datastore[0].info.name

    datastore = get_info(content, [vim.Datastore], real_datastore_name)

    # set relospec
    relospec = vim.vm.RelocateSpec()
    relospec.datastore = datastore
    relospec.pool = resource_pool

    clonespec = vim.vm.CloneSpec()
    clonespec.location = relospec
    clonespec.powerOn = power_on
    
    reconspec = vim.vm.ReconfigVM()
    reconspec.numCPUs = 3

    print("Request is processing. Please wait.")
    task = template_name.Clone(folder=destfolder, name=vm_name, spec=reconspec)
    wait_for_task(task)

def main():
    si = Connect.vSphereConnect()
    content = si.RetrieveContent()

    template = None

    template = get_info(content, [vim.VirtualMachine], clone_template)

    if template:
        clone_vm(content, template, clone_name, content, clone_datastore, clone_resourcepool, True)
    else:
        OUTPUT.append("Template for " + clone_template + " was not found")
        print("Template for " + clone_template + " was not found")
    # print(OUTPUT)  

if __name__ == "__main__":
    main()  
