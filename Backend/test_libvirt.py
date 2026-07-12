from app.libvirt.connection import get_connection

conn = get_connection()

print("Connected Successfully!")

print("Hostname:", conn.getHostname())

print("Libvirt Version:", conn.getLibVersion())

conn.close()