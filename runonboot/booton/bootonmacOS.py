import plistlib
import os
from .bootonPlatform import bootonPlatform
from runonboot import Runner

class bootonmacOS(bootonPlatform):
    def installRunner(runner):
        """Install a runner on macOS."""
        if bootonmacOS.isRunnerInstalled(runner.getName()):
            raise Exception("Runner already installed")
        bootonmacOS.createRunnerFile(runner)
    
    def removeRunner(runnerName):
        """Remove a runner on macOS."""
        position = None
        if os.path.exists(bootonmacOS.getRunnerFilename(runnerName, True)):
            position = "user"
        elif os.path.exists(bootonmacOS.getRunnerFilename(runnerName, False)):
            position = "system"
        
        if position is not None:
            if position == "user":
                os.remove(bootonmacOS.getRunnerFilename(runnerName, True))
            elif position == "system":
                os.remove(bootonmacOS.getRunnerFilename(runnerName, False))
    
    def isRunnerInstalled(runnerName):
        """Check if a runner is installed on macOS."""
        if os.path.exists(bootonmacOS.getRunnerFilename(runnerName, True)) or os.path.exists(bootonmacOS.getRunnerFilename(runnerName)):
            return True
        return False
    
    def getAgentsFolder(user_only=True):
        """Get the folder where the launch agents are stored on macOS.
           If user_only is True, the user's folder is returned. Otherwise, the system's folder is returned."""
        if user_only == True:
            return os.path.expanduser("~/Library/LaunchAgents")
        return "/Library/LaunchDaemons"
    
    def getRunnerFilename(runnerName, user_only=True):
        """Get the filename of a runner on macOS, based on the runner's name and the type of folder to use."""
        return os.path.join(bootonmacOS.getAgentsFolder(user_only), runnerName + ".plist")
    
    def createRunnerFile(runner: Runner, user_only=True):
        """Create a runner file on macOS."""
        runnerFilename = bootonmacOS.getRunnerFilename(runner.getName(), user_only)
                
        # Python 3.9+ only supports the dump() method, so we need to check for it.
        if hasattr(plistlib, 'dump'):
            with open(runnerFilename, "wb") as runnerFile:
                plistlib.dump(bootonmacOS.makeRunnerPlist(runner), runnerFile)
        else:
            plistlib.writePlist(bootonmacOS.makeRunnerPlist(runner, runnerFile))
        
    def makeRunnerPlist(runner: Runner):
        """Create a runner plist in macOS LaunchAgents standard."""
        return {
            "Label": runner.getName(),
            "ProgramArguments": runner.getCommand().split(" "),
            "RunAtLoad": True
        }