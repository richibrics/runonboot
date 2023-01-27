import platform
from .booton import bootonLinux, bootonmacOS, bootonWindows, bootonPlatform
from runonboot import Runner

def installRunner(runner: Runner, user_only=True):
    """Install a runner to run on boot.
       Runner is a Runner object.
       May need to enter admin password if user_only is False."""
    return bootonThis().installRunner(runner, user_only)

def removeRunner(runnerName):
    """Remove a runner from running on boot.
       May need to enter admin password if the runner is installed to run on boot not only for the current user but system wide."""
    return bootonThis().removeRunner(runnerName)

def isRunnerInstalled(runnerName) -> bool:
    """Check if a runner is installed to run on boot.
       Returns True if installed, False if not."""
    return bootonThis().isRunnerInstalled(runnerName)

def disclaimer() -> str:
    """Get the disclaimer for the current platform.
       Returns a string with the disclaimer."""
    return bootonThis().disclaimer()

def bootonThis() -> bootonPlatform.bootonPlatform:
    if platform.system() == "Windows":
        return bootonWindows
    elif platform.system() == "Linux":
        return bootonLinux
    elif platform.system() == "Darwin":
        return bootonmacOS
    else:
        raise Exception("Unsupported platform: " + platform.system())