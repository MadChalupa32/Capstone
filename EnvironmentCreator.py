"""EnvironmentCreator.py"""
from __future__ import print_function
import logging
import ListVM
import PowerOnVM
import PowerOffVM
import DeleteVM
import VMtoList
import CreateVM
from flask import Flask
from flask_ask import Ask, statement, question, session, context, delegate, audio
import GetDatastoreHealth
import GetHostHealth
import ListTemplate
import CloneTemplate

app = Flask(__name__)
ask = Ask(app, '/')

log = logging.getLogger()
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)
logging.getLogger("flask_Ask").setLevel(logging.DEBUG)


@ask.launch
def welcome():
    return question("welcome")



def get_dialog_state():
    return session['dialogState']



@ask.intent('AudioIntent')
def demo():
    stream_url = 'https://s3.us-east-2.amazonaws.com/environmentcreator/Jeopardy.mp3'
    return audio().play(stream_url, offset=0)




@ask.intent('CloneTemplateIntent', convert={'Name': str, 'Template': str})
def clone_template(Name, Template):
    CloneTemplate.OUTPUT[:] = []

    vm_name = Name
    vm_template = Template

    # print(vm_name)
    # print(vm_template)

    CloneTemplate.clone_name = vm_name
    CloneTemplate.clone_template = vm_template
    
    dialog_state = get_dialog_state()
    if dialog_state != "COMPLETED":
        return delegate(speech=None)

    CloneTemplate.main()
    
    output = CloneTemplate.OUTPUT
    output = '. '.join(str(p) for p in output)
    # print(output)

    return statement(output).simple_card("Clone a Template", output)




# @ask.intent('CreateVMIntent')
# def create_virtual_machine(Name, Cpu, Storage, Memory):
#     '''Creates a new Virtual Machine'''
#     vm_name = Name
#     cpu_count = Cpu
#     memory_count = Memory
#     storage_count = Storage
#     dialog_state = get_dialog_state()
#     if dialog_state != "COMPLETED":
#         return delegate(speech=None)
#     print("A virtual machine named " + vm_name + " with " +  cpu_count + " CPUs " + memory_count + " gigabytes of memory and " + storage_count + " gigabytes of storage has been created")
#     return statement("A virtual machine named " + vm_name + " with " +  cpu_count + " CPUs " + memory_count + " gigabytes of memory and " + storage_count + " gigabytes of storage has been created")




@ask.intent('DeleteVMIntent')
def delete_vm(Name):
    DeleteVM.OUTPUT[:] = []
    vm_name = Name
    DeleteVM.vm_name = vm_name

    # print(Name)#
    # print(DeleteVM.vm_name)

    dialog_state = get_dialog_state()
    if dialog_state != "COMPLETED":
        return delegate(speech=None)

    DeleteVM.main()

    output = DeleteVM.OUTPUT
    output = '. '.join(str(p) for p in output)
    # print(output)

    return statement(output).simple_card("Delete a Virtual Machine", output)




@ask.intent('GetDatastoreHealthIntent')
def datastore_health():
    GetDatastoreHealth.OUTPUT[:] = []
    GetDatastoreHealth.main()

    output = GetDatastoreHealth.OUTPUT
    output = '. '.join(str(p) for p in output)
    print(output)

    return statement(output).simple_card("Get Datastore Health", output)




@ask.intent('GetHostHealthIntent')
def host_health():
    GetHostHealth.OUTPUT[:] = []
    GetHostHealth.main()
    
    output = GetHostHealth.OUTPUT
    output = '. '.join(str(p) for p in output)
    # print(output)

    return statement(output).simple_card("Get Host Health", output)




@ask.intent('ListOptionsIntent')
def list_options():
    options = [
        # 'Audio Intent',
        'Clone a Virtual Machine', 
        # 'Create a Virtual Machine',
        'Delete a Virtual Machine',
        'List Datastore Health',
        'List Host Health',
        # 'List all Options',
        'List all Templates',
        'List all Virtual Machines', 
        'Power Off Virtual Machine', 
        'Power On Virtual Machine'
        ]

    output = '. '.join(options)
    # print(output)
    return statement(output).simple_card("List all options", output)




@ask.intent('ListTemplatesIntent')
def list_template():
    ListTemplate.OUTPUT[:] = []
    ListTemplate.main()

    output = ListTemplate.OUTPUT
    output = ". ".join(str(p) for p in output)

    return statement("Available templates include " + output).simple_card("List Templates", output)




@ask.intent('ListVMIntent')
def list_vm(): 
    ListVM.OUTPUT[:] = []
    ListVM.main()

    output = ListVM.OUTPUT
    output = '. '.join(str(p) for p in output)
    print(output)

    return statement(output).simple_card("List Virtual Machines", output)
      



@ask.intent('PowerOffIntent')
def power_off(Name):
    #print(Name)
    PowerOffVM.OUTPUT[:] = []
    PowerOffVM.vm_name = Name

    # dialog_state = get_dialog_state()
    # if dialog_state != "COMPLETED":
    #     return delegate(speech=None)

    PowerOffVM.main()

    output = str(PowerOffVM.OUTPUT[-1])
    return statement(output).simple_card("Power Off Virtual Machine", output)




@ask.intent('PowerOnIntent')
def power_on(Name):
    #print(Name)
    PowerOnVM.OUTPUT[:] = []
    PowerOnVM.vm_name = Name
    PowerOnVM.main()

    output = str(PowerOnVM.OUTPUT[-1])
    return statement(output).simple_card("Power On Virtual Machine", output)




@ask.session_ended
def session_ended():
    return "{}", 200

if __name__ == '__main__':
    app.run(debug=True)