import libvirt
import os
import shutil
import subprocess
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

            state, _ = domain.state()

            if state != libvirt.VIR_DOMAIN_SHUTOFF:
                raise Exception(
                    "Please shut down the VM before creating a snapshot."
                )

            source_disk = f"/var/lib/libvirt/images/{vm_name}.qcow2"

            if not os.path.exists(source_disk):
                raise Exception(f"VM disk not found: {source_disk}")

            snapshot_dir = os.path.join(
                os.getcwd(),
                "snapshots",
                vm_name,
            )

            os.makedirs(snapshot_dir, exist_ok=True)

            snapshot_disk = os.path.join(
                snapshot_dir,
                f"{snapshot_name}.qcow2",
            )

            if os.path.exists(snapshot_disk):
                raise Exception(
                    f"Snapshot '{snapshot_name}' already exists."
                )

            subprocess.run(
                [
                    "sudo",
                    "/home/prachi/Documents/Projects/HyperVisorX/Backend/scripts/snapshot_copy.sh",
                    source_disk,
                    snapshot_disk,
                ],
                check=True,
            )

            return True

        except subprocess.CalledProcessError:
            raise Exception("Failed to create snapshot.")

        except Exception as e:
            raise Exception(str(e))

    # -----------------------------
    # List Snapshots
    # -----------------------------
    def list_snapshots(self, vm_name: str):
        try:
            snapshot_dir = os.path.join(
                os.getcwd(),
                "snapshots",
                vm_name,
            )

            if not os.path.exists(snapshot_dir):
                return []

            snapshots = []

            for file in os.listdir(snapshot_dir):

                if not file.endswith(".qcow2"):
                    continue

                path = os.path.join(snapshot_dir, file)

                snapshots.append(
                    {
                        "name": file.replace(".qcow2", ""),
                        "size_mb": round(
                            os.path.getsize(path) / (1024 * 1024),
                            2,
                        ),
                        "created": os.path.getctime(path),
                    }
                )

            snapshots.sort(
                key=lambda x: x["created"],
                reverse=True,
            )

            return snapshots

        except Exception as e:
            raise Exception(str(e))

    # -----------------------------
    # Restore Snapshot
    # -----------------------------
    def restore_snapshot(self, vm_name: str, snapshot_name: str):
        try:
            domain = self.conn.lookupByName(vm_name)

            state, _ = domain.state()

            if state != libvirt.VIR_DOMAIN_SHUTOFF:
                raise Exception(
                    "Please shut down the VM before restoring a snapshot."
                )

            snapshot_disk = os.path.join(
                os.getcwd(),
                "snapshots",
                vm_name,
                f"{snapshot_name}.qcow2",
            )

            if not os.path.exists(snapshot_disk):
                raise Exception("Snapshot not found.")

            vm_disk = f"/var/lib/libvirt/images/{vm_name}.qcow2"

            subprocess.run(
                [
                    "sudo",
                    "/home/prachi/Documents/Projects/HyperVisorX/Backend/scripts/snapshot_copy.sh",
                    snapshot_disk,
                    vm_disk,
                ],
                check=True,
            )

            return True

        except subprocess.CalledProcessError:
            raise Exception("Failed to restore snapshot.")

        except Exception as e:
            raise Exception(str(e))

    # -----------------------------
    # Delete Snapshot
    # -----------------------------
    def delete_snapshot(self, vm_name: str, snapshot_name: str):
        try:
            snapshot_disk = os.path.join(
                os.getcwd(),
                "snapshots",
                vm_name,
                f"{snapshot_name}.qcow2",
            )

            if not os.path.exists(snapshot_disk):
                raise Exception("Snapshot not found.")

            subprocess.run(
    [
        "sudo",
        "/home/prachi/Documents/Projects/HyperVisorX/Backend/scripts/delete_snapshot.sh",
        snapshot_disk,
    ],
    check=True,
)

            return True

        except Exception as e:
            raise Exception(str(e))

    # -----------------------------
    # Get VM IP Address
    # -----------------------------
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

        except Exception:
            pass

        return None

    # -----------------------------
    # Get VM Statistics
    # -----------------------------
    def get_vm_stats(self, vm_name: str):
        """
        Get VM CPU and Memory statistics.
        """
        try:
            domain = self.conn.lookupByName(vm_name)

            info = domain.info()

            return {
                "state": info[0],
                "max_memory_mb": info[1] // 1024,
                "used_memory_mb": info[2] // 1024,
                "vcpus": info[3],
                "cpu_time_ns": info[4],
            }

        except libvirt.libvirtError as e:
            raise Exception(str(e))

    # -----------------------------
    # Get VM Network Statistics
    # -----------------------------
    def get_vm_network(self, vm_name: str):
        """
        Get VM network statistics.
        """
        try:
            domain = self.conn.lookupByName(vm_name)

            xml = domain.XMLDesc()

            import xml.etree.ElementTree as ET

            root = ET.fromstring(xml)

            interface = root.find(".//devices/interface/target")

            if interface is None:
                return {
                    "error": "No network interface found."
                }

            interface_name = interface.attrib["dev"]

            stats = domain.interfaceStats(interface_name)

            return {
                "interface": interface_name,
                "rx_bytes": stats[0],
                "rx_packets": stats[1],
                "tx_bytes": stats[4],
                "tx_packets": stats[5],
            }

        except libvirt.libvirtError as e:
            raise Exception(str(e))

    # -----------------------------
    # Close Connection
    # -----------------------------
    def close(self):
        self.conn.close()