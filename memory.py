import os
from config import *

current_path = "/home"

linux_file_system = {
    "/": ["bin", "boot", "dev", "etc", "home", "lib", "lib64", "media", "mnt", "opt", "proc", "root", "run", "sbin", "srv", "sys", "tmp", "usr", "var"],
    "/bin": ["bash", "cat", "ls", "mkdir", "mv", "rm"],
    "/boot": ["grub", "vmlinuz"],
    "/dev": ["sda", "sdb", "tty", "null", "random"],
    "/etc": ["passwd", "shadow", "group", "hostname", "network"],
    "/home": ["user"],
    "/lib": ["modules"],
    "/media": ["usb", "cdrom"],
    "/mnt": [],
    "/opt": [],
    "/proc": ["cpuinfo", "meminfo", "uptime"],
    "/root": [],
    "/run": [],
    "/sbin": ["ifconfig", "reboot", "shutdown"],
    "/srv": [],
    "/sys": [],
    "/tmp": [],
    "/usr": ["bin", "lib", "local", "share", "src"],
    "/usr/bin": ["python", "vim", "nano", "gcc"],
    "/usr/lib": ["python3"],
    "/usr/local": ["bin", "etc", "games", "include", "lib", "sbin", "share", "src"],
    "/usr/share": ["man", "doc"],
    "/usr/src": [],
    "/var": ["log", "tmp", "spool", "cache"],
    "/var/log": ["syslog", "auth.log"],
    "/var/tmp": [],
    "/var/spool": ["mail"],
    "/var/cache": []
}

def update_filesystem(username):
    # Create user's home directory path
    user_path = f"/home/{username}"
    
    # Add username to /home directory if not present
    if username not in linux_file_system["/home"]:
        linux_file_system["/home"].append(username)
    
    # Create user's home directory structure if not present
    if user_path not in linux_file_system:
        linux_file_system[user_path] = ["Desktop", "Documents", "Downloads", "Music", "Pictures", "Videos", "Public"]
        
        # Create subdirectories for each folder in user's home
        subdirs = {
            f"{user_path}/Desktop": [],
            f"{user_path}/Documents": [],
            f"{user_path}/Downloads": [],
            f"{user_path}/Music": [],
            f"{user_path}/Pictures": [],
            f"{user_path}/Videos": [],
            f"{user_path}/Public": []
        }
        
        # Update filesystem with all subdirectories
        linux_file_system.update(subdirs)
    
    return user_path

def normalize_path(path, current_path):
    """Normalize a path, handling both absolute and relative paths"""
    if not path.startswith('/'):
        # Handle relative path
        if current_path.endswith('/'):
            path = current_path + path
        else:
            path = current_path + '/' + path
    
    # Remove any double slashes
    while '//' in path:
        path = path.replace('//', '/')
    
    # Remove trailing slash except for root
    if path != '/' and path.endswith('/'):
        path = path[:-1]
        
    return path