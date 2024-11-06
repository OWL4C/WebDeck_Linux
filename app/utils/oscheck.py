import sys


def get_os():
    if sys.platform.startswith('win'):
        return "Windows"
    elif sys.platform.startswith('linux'):
        return "Linux"
    elif sys.platform.startswith('darwin'):
        return "MacOS"
    else:
        return "Other"

def is_win():
    if os == "Windows":
        return True
    else:
        return False


os = get_os()
is_win = is_win()
