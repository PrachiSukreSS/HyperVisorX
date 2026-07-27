from fastapi import APIRouter
from app.services.console_service import ConsoleService

router = APIRouter(
    prefix="/console",
    tags=["Console"],
)

service = ConsoleService()


@router.get("/{vm_name}")
def open_console(vm_name: str):
    return service.open_console(vm_name)