import ctypes
import sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)

print("Le programme a été exécuté avec les permissions administrateur.")

try:
    import wmi
except ImportError:
    import pip
    pip.main(['install', 'wmi'])

def get_disk_partitions():
    c = wmi.WMI()
    partitions = c.Win32_DiskPartition()

    disk_info = []

    for partition in partitions:
        yield partition

disk_partitions = get_disk_partitions()
print("Disk Partitions:")
for partition in disk_partitions:
    print(partition)


input()