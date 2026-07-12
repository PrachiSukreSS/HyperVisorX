from fastapi import APIRouter

from app.services.monitoring_service import MonitoringService

router = APIRouter(
    prefix="/monitoring",
    tags=["Monitoring"],
)

service = MonitoringService()

@router.get("/")
def get_dashboard_metrics():

    return service.get_dashboard_metrics()
    
@router.get("/host/cpu")
def get_host_cpu():

    return service.get_host_cpu()

@router.get("/host/memory")
def get_host_memory():

    return service.get_host_memory()

@router.get("/host/disk")
def get_host_disk():

    return service.get_host_disk()        

@router.get("/host/network")
def get_host_network():

    return service.get_host_network()    

@router.get("/vm/{vm_name}")
def get_vm_stats(vm_name: str):

    return service.get_vm_stats(vm_name)  

@router.get("/vm/{vm_name}/network")
def get_vm_network(vm_name: str):

    return service.get_vm_network(vm_name)      