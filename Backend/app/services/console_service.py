import subprocess

from app.libvirt.manager import VirtualMachineManager


class ConsoleService:

    def open_console(self, vm_name: str):

        manager = VirtualMachineManager()

        # Check VM exists
        manager.get_vm(vm_name)

        manager.close()

        # Check if websockify is already running
        result = subprocess.run(
            ["pgrep", "-f", "websockify 6080"],
            capture_output=True,
            text=True,
        )

        # Start it only if not already running
        if result.returncode != 0:
          subprocess.Popen(
    [
        "websockify",
        "--web",
        "/usr/share/novnc",
        "6080",
        "localhost:5900",
    ],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)

        return {
            "vm": vm_name,
            "host": "localhost",
            "port": 6080,
            "console_url": "http://localhost:6080/vnc.html?autoconnect=1"
        }