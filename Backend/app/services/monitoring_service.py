import psutil

from app.libvirt.manager import VirtualMachineManager


class MonitoringService:

    # -----------------------------
    # Host CPU
    # -----------------------------
    def get_host_cpu(self):

        return {
            "cpu_percent": psutil.cpu_percent(interval=1)
        }

    # -----------------------------
    # Host Memory
    # -----------------------------
    def get_host_memory(self):

        memory = psutil.virtual_memory()

        return {
            "total_mb": round(memory.total / (1024 * 1024), 2),
            "used_mb": round(memory.used / (1024 * 1024), 2),
            "available_mb": round(memory.available / (1024 * 1024), 2),
            "usage_percent": memory.percent,
        }

    # -----------------------------
    # Host Disk
    # -----------------------------
    def get_host_disk(self):

        disk = psutil.disk_usage("/")

        return {
            "total_gb": round(disk.total / (1024 ** 3), 2),
            "used_gb": round(disk.used / (1024 ** 3), 2),
            "free_gb": round(disk.free / (1024 ** 3), 2),
            "usage_percent": disk.percent,
        }

    # -----------------------------
    # Host Network
    # -----------------------------
    def get_host_network(self):

        network = psutil.net_io_counters()

        return {
            "bytes_sent": network.bytes_sent,
            "bytes_received": network.bytes_recv,
            "packets_sent": network.packets_sent,
            "packets_received": network.packets_recv,
        }

    # -----------------------------
    # VM CPU / Memory Stats
    # -----------------------------
    def get_vm_stats(self, vm_name: str):

        manager = VirtualMachineManager()

        stats = manager.get_vm_stats(vm_name)

        manager.close()

        return stats

    # -----------------------------
    # VM Network Stats
    # -----------------------------
    def get_vm_network(self, vm_name: str):

        manager = VirtualMachineManager()

        stats = manager.get_vm_network(vm_name)

        manager.close()

        return stats

    # -----------------------------
    # Dashboard Metrics
    # -----------------------------
    def get_dashboard_metrics(self):

        cpu = self.get_host_cpu()
        memory = self.get_host_memory()
        disk = self.get_host_disk()
        network = self.get_host_network()

        return {
            "cpu_usage": cpu["cpu_percent"],
            "memory_usage": memory["usage_percent"],
            "disk_usage": disk["usage_percent"],
            "network_sent": round(network["bytes_sent"] / 1024, 2),  
            "host_usage": cpu["cpu_percent"],
            "vm_usage": 0
        }