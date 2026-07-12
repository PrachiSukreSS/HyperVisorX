from app.libvirt.manager import VirtualMachineManager

manager = VirtualMachineManager()

vms = manager.list_vms()

print("Total VMs:", len(vms))

for vm in vms:
    print(vm.name())

manager.close()