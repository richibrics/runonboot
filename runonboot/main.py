import platform
from .booton import bootonLinux, bootonmacOS, bootonWindows

def installRunner(runner, user_only=True):
    return bootonThis().installRunner(runner, user_only)

def removeRunner(runnerName):
    return bootonThis().removeRunner(runnerName)

def isRunnerInstalled(runnerName):
    return bootonThis().isRunnerInstalled(runnerName)

def bootonThis():
    if platform.system() == "Windows":
        return bootonWindows
    elif platform.system() == "Linux":
        return bootonLinux
    elif platform.system() == "Darwin":
        return bootonmacOS
    else:
        raise Exception("Unsupported platform: " + platform.system())