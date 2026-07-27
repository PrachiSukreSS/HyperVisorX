from fastapi import APIRouter

from app.schemas.vm import VirtualMachineResponse
from app.services.vm_service import VMService

router = APIRouter(
    prefix="/vms",
    tags=["Virtual Machines"],
)

service = VMService()


# -----------------------------
# List All VMs
# -----------------------------
@router.get("/", response_model=list[VirtualMachineResponse])
def get_all_vms():
    return service.get_all_vms()


# -----------------------------
# Get VM Details
# -----------------------------
@router.get("/{vm_name}")
def get_vm(vm_name: str):
    return service.get_vm(vm_name)


# -----------------------------
# Start VM
# -----------------------------
@router.post("/{vm_name}/start")
def start_vm(vm_name: str):
    return service.start_vm(vm_name)


# -----------------------------
# Shutdown VM
# -----------------------------
@router.post("/{vm_name}/shutdown")
def shutdown_vm(vm_name: str):
    return service.shutdown_vm(vm_name)


# -----------------------------
# Force Stop VM
# -----------------------------
@router.post("/{vm_name}/stop")
def stop_vm(vm_name: str):
    return service.stop_vm(vm_name)


# -----------------------------
# Restart VM
# -----------------------------
@router.post("/{vm_name}/restart")
def restart_vm(vm_name: str):
    return service.restart_vm(vm_name)


# -----------------------------
# Suspend VM
# -----------------------------
@router.post("/{vm_name}/suspend")
def suspend_vm(vm_name: str):
    return service.suspend_vm(vm_name)


# -----------------------------
# Resume VM
# -----------------------------
@router.post("/{vm_name}/resume")
def resume_vm(vm_name: str):
    return service.resume_vm(vm_name)


# -----------------------------
# Create Snapshot
# -----------------------------
@router.post("/{vm_name}/snapshot/{snapshot_name}")
def create_snapshot(vm_name: str, snapshot_name: str):
    return service.create_snapshot(vm_name, snapshot_name)


# -----------------------------
# Restore Snapshot
# -----------------------------
@router.post("/{vm_name}/snapshot/{snapshot_name}/restore")
def restore_snapshot(vm_name: str, snapshot_name: str):
    return service.restore_snapshot(vm_name, snapshot_name)


# -----------------------------
# Delete Snapshot
# -----------------------------
@router.delete("/{vm_name}/snapshot/{snapshot_name}")
def delete_snapshot(vm_name: str, snapshot_name: str):
    return service.delete_snapshot(vm_name, snapshot_name)

@router.get("/{vm_name}/snapshots")
def list_snapshots(vm_name: str):

    service = VMService()

    return service.list_snapshots(vm_name)
