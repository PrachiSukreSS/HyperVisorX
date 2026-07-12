import libvirt

from app.core.config import settings


def get_connection():
    """
    Connect to the libvirt daemon.
    """

    conn = libvirt.open(settings.LIBVIRT_URI)

    if conn is None:
        raise Exception("Failed to connect to libvirt.")

    return conn