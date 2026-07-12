from app.libvirt.manager import VirtualMachineManager
from app.models.virtual_machine import VirtualMachine
from app.core.database import SessionLocal


class VMService:

    def get_all_vms(self):

        manager = VirtualMachineManager()

        domains = manager.list_vms()

        db = SessionLocal()

        vms = []

        for domain in domains:

            state, _ = domain.state()

            info = domain.info()

            vm = db.query(VirtualMachine).filter(
                VirtualMachine.uuid == domain.UUIDString()
            ).first()

            if vm is None:

                vm = VirtualMachine(
                    name=domain.name(),
                    uuid=domain.UUIDString(),
                    os_type="Unknown",
                    cpu=info[3],
                    memory=info[1] // 1024,
                    disk_size=0,
                    status=self._get_state_name(state),
                    ip_address=manager.get_vm_ip(domain),
                    mac_address=None,
                )

                db.add(vm)

            else:

                vm.name = domain.name()
                vm.cpu = info[3]
                vm.memory = info[1] // 1024
                vm.status = self._get_state_name(state)
                vm.ip_address = manager.get_vm_ip(domain)

            db.commit()

            vms.append({
                "name": vm.name,
                "id": domain.ID(),
                "state": vm.status,
            })

        db.close()

        manager.close()

        return vms

    def _get_state_name(self, state):

        states = {
            0: "No State",
            1: "Running",
            2: "Blocked",
            3: "Paused",
            4: "Shutdown",
            5: "Shut Off",
            6: "Crashed",
            7: "Suspended",
        }

        return states.get(state, "Unknown")

    # -----------------------------
    # Start VM
    # -----------------------------
    def start_vm(self, vm_name: str):

        manager = VirtualMachineManager()

        manager.start_vm(vm_name)

        manager.close()

        return {
            "message": f"{vm_name} started successfully."
        }

    # -----------------------------
    # Shutdown VM
    # -----------------------------
    def shutdown_vm(self, vm_name: str):

        manager = VirtualMachineManager()

        manager.shutdown_vm(vm_name)

        manager.close()

        return {
            "message": f"{vm_name} shut down successfully."
        }

    # -----------------------------
    # Stop VM
    # -----------------------------
    def stop_vm(self, vm_name: str):

        manager = VirtualMachineManager()

        manager.stop_vm(vm_name)

        manager.close()

        return {
            "message": f"{vm_name} force stopped successfully."
        }

    # -----------------------------
    # Restart VM
    # -----------------------------
    def restart_vm(self, vm_name: str):

        manager = VirtualMachineManager()

        manager.restart_vm(vm_name)

        manager.close()

        return {
            "message": f"{vm_name} restarted successfully."
        }

    # -----------------------------
    # Suspend VM
    # -----------------------------
    def suspend_vm(self, vm_name: str):

        manager = VirtualMachineManager()

        manager.suspend_vm(vm_name)

        manager.close()

        return {
            "message": f"{vm_name} suspended successfully."
        }

    # -----------------------------
    # Resume VM
    # -----------------------------
    def resume_vm(self, vm_name: str):

        manager = VirtualMachineManager()

        manager.resume_vm(vm_name)

        manager.close()

        return {
            "message": f"{vm_name} resumed successfully."
        }

    # -----------------------------
    # Delete VM
    # -----------------------------
    def delete_vm(self, vm_name: str):

        manager = VirtualMachineManager()

        manager.delete_vm(vm_name)

        manager.close()

        return {
            "message": f"{vm_name} deleted successfully."
        }

    # -----------------------------
    # VM Details
    # -----------------------------
    def get_vm(self, vm_name: str):

        manager = VirtualMachineManager()

        domain = manager.get_vm(vm_name)

        state, _ = domain.state()

        info = domain.info()

        vm = {
            "name": domain.name(),
            "uuid": domain.UUIDString(),
            "state": self._get_state_name(state),
            "max_memory_mb": info[1] // 1024,
            "memory_mb": info[2] // 1024,
            "vcpus": info[3],
        }

        manager.close()

        return vm

    def get_vm_info(self, vm_name: str):

        manager = VirtualMachineManager()

        info = manager.get_vm_info(vm_name)

        manager.close()

        return info

    # -----------------------------
    # Create Snapshot
    # -----------------------------
    def create_snapshot(self, vm_name: str, snapshot_name: str):

        manager = VirtualMachineManager()

        manager.create_snapshot(vm_name, snapshot_name)

        manager.close()

        return {
            "message": f"Snapshot '{snapshot_name}' created successfully."
        }

    # -----------------------------
    # Restore Snapshot
    # -----------------------------
    def restore_snapshot(self, vm_name: str, snapshot_name: str):

        manager = VirtualMachineManager()

        manager.restore_snapshot(vm_name, snapshot_name)

        manager.close()

        return {
            "message": f"Snapshot '{snapshot_name}' restored successfully."
        }

    # -----------------------------
    # Delete Snapshot
    # -----------------------------
    def delete_snapshot(self, vm_name: str, snapshot_name: str):

        manager = VirtualMachineManager()

        manager.delete_snapshot(vm_name, snapshot_name)

        manager.close()

        return {
            "message": f"Snapshot '{snapshot_name}' deleted successfully."
        }