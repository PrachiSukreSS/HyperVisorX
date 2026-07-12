import libvirt

from app.libvirt.connection import get_connection


class VirtualMachineManager:
    """
    Handles all Virtual Machine operations.
    """

    def __init__(self):
        self.conn = get_connection()

    # -----------------------------
    # List VMs
    # -----------------------------
    def list_vms(self):
        return self.conn.listAllDomains()

    # -----------------------------
    # Start VM
    # -----------------------------
    def start_vm(self, vm_name: str):
        try:
            domain = self.conn.lookupByName(vm_name)
            domain.create()
            return True

        except libvirt.libvirtError as e:
            raise Exception(str(e))

    # -----------------------------
    # Shutdown VM
    # -----------------------------
    def shutdown_vm(self, vm_name: str):
        try:
            domain = self.conn.lookupByName(vm_name)
            domain.shutdown()
            return True

        except libvirt.libvirtError as e:
            raise Exception(str(e))

    # -----------------------------
    # Force Stop VM
    # -----------------------------
    def stop_vm(self, vm_name: str):
        try:
            domain = self.conn.lookupByName(vm_name)
            domain.destroy()
            return True

        except libvirt.libvirtError as e:
            raise Exception(str(e))

    # -----------------------------
    # Restart VM
    # -----------------------------
    def restart_vm(self, vm_name: str):
        try:
            domain = self.conn.lookupByName(vm_name)
            domain.reboot()
            return True

        except libvirt.libvirtError as e:
            raise Exception(str(e))

    # -----------------------------
    # Suspend VM
    # -----------------------------
    def suspend_vm(self, vm_name: str):
        try:
            domain = self.conn.lookupByName(vm_name)
            domain.suspend()
            return True

        except libvirt.libvirtError as e:
            raise Exception(str(e))

    # -----------------------------
    # Resume VM
    # -----------------------------
    def resume_vm(self, vm_name: str):
        try:
            domain = self.conn.lookupByName(vm_name)
            domain.resume()
            return True

        except libvirt.libvirtError as e:
            raise Exception(str(e))

    # -----------------------------
    # Delete VM
    # -----------------------------
    def delete_vm(self, vm_name: str):
        try:
            domain = self.conn.lookupByName(vm_name)
            domain.undefine()
            return True

        except libvirt.libvirtError as e:
            raise Exception(str(e))

    # -----------------------------
    # Get VM Object
    # -----------------------------
    def get_vm(self, vm_name: str):
        try:
            return self.conn.lookupByName(vm_name)

        except libvirt.libvirtError as e:
            raise Exception(str(e))

    # -----------------------------
    # Get VM Details
    # -----------------------------
    def get_vm_info(self, vm_name: str):
        try:
            domain = self.conn.lookupByName(vm_name)

            state, _ = domain.state()

            return {
                "name": domain.name(),
                "id": domain.ID(),
                "state": state,
                "memory": domain.maxMemory(),
                "vcpus": domain.maxVcpus(),
            }

        except libvirt.libvirtError as e:
            raise Exception(str(e))

    # -----------------------------
    # Create Snapshot
    # -----------------------------
    def create_snapshot(self, vm_name: str, snapshot_name: str):
        try:
            domain = self.conn.lookupByName(vm_name)

            xml = f"""
            <domainsnapshot>
                <name>{snapshot_name}</name>
            </domainsnapshot>
            """

            domain.snapshotCreateXML(xml, 0)

            return True

        except libvirt.libvirtError as e:
            raise Exception(str(e))

    # -----------------------------
    # Restore Snapshot
    # -----------------------------
    def restore_snapshot(self, vm_name: str, snapshot_name: str):
        try:
            domain = self.conn.lookupByName(vm_name)

            snapshot = domain.snapshotLookupByName(snapshot_name)

            domain.revertToSnapshot(snapshot)

            return True

        except libvirt.libvirtError as e:
            raise Exception(str(e))

    # -----------------------------
    # Delete Snapshot
    # -----------------------------
    def delete_snapshot(self, vm_name: str, snapshot_name: str):
        try:
            domain = self.conn.lookupByName(vm_name)

            snapshot = domain.snapshotLookupByName(snapshot_name)

            snapshot.delete()

            return True

        except libvirt.libvirtError as e:
            raise Exception(str(e))



    def get_vm_ip(self, domain):
        """
         Return VM IPv4 address.
          """

        try:
            interfaces = domain.interfaceAddresses(
                libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_AGENT
            )

            for _, val in interfaces.items():
                if "addrs" in val:
                    for addr in val["addrs"]:
                        if addr["type"] == libvirt.VIR_IP_ADDR_TYPE_IPV4:
                            return addr["addr"]

        except:
             pass
        return None        

    # -----------------------------
    # Close Connection
    # -----------------------------
    def close(self):
        self.conn.close()