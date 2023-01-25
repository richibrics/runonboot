import platform
from .booton import bootonLinux, bootonmacOS, bootonWindows

def installRunner(runner):
    bootonThis().installRunner(runner)

def removeRunner(runnerName):
    bootonThis().removeRunner(runnerName)

def isRunnerInstalled(runnerName):
    bootonThis.isRunnerInstalled(runnerName)

def bootonThis():
    if platform.system() == "Windows":
        return bootonWindows
    elif platform.system() == "Linux":
        return bootonLinux
    elif platform.system() == "Darwin":
        return bootonmacOS
    else:
        raise Exception("Unsupported platform: " + platform.system())