import libvirt

from app.libvirt.connection import get_connection


class VirtualMachineManager:
    """
    Handles all Virtual Machine operations.
    """

    def __init__(self):
        self.conn = get_connection()

    def list_vms(self):
        """
        Return all virtual machines.
        """
        return self.conn.listAllDomains()

    def close(self):
        """
        Close libvirt connection.
        """
        self.conn.close()