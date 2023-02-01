import plistlib
import os
from .bootonPlatform import bootonPlatform
from runonboot.runner.Runner import Runner

class bootonmacOS(bootonPlatform):
    def installRunner(runner, user_only=True):
        """Install a runner on macOS."""
        if bootonmacOS.isRunnerInstalled(runner.getName()):
            raise Exception("Runner already installed")
        
        if user_only or bootonmacOS.checkIfSudoMode(): # then has rights in any case
            newRunnerPosition = bootonmacOS.getRunnerFilename(runner.getName(), user_only)
            bootonmacOS.createRunnerFile(runner, newRunnerPosition)
        else:
            # get rights to write in non user only folder
            # need to use sudo command in shell in order to make appear the sudo password input on the terminal
            
            # Steps:
            # 1. Create a temporary file with the runner's content
            # 2. Use sudo to move the file to the system's LaunchDaemons folder
            scriptFolder = os.path.dirname(os.path.realpath(__file__))
            tmpRunnerPosition = os.path.join(scriptFolder, runner.getName() + ".booton")
            finalRunnerPosition = bootonmacOS.getRunnerFilename(runner.getName(), user_only) # user only should be false here

            # Write on the temporary file
            bootonmacOS.createRunnerFile(runner, tmpRunnerPosition)
            # Move the file to the system's LaunchDaemons folder
            os.system(f"sudo mv \"{tmpRunnerPosition}\" \"{finalRunnerPosition}\"")
    
    def removeRunner(runnerName):
        """Remove a runner on macOS."""
        if not bootonmacOS.isRunnerInstalled(runnerName):
            raise Exception("Runner is not installed")
        
        position = None
        if os.path.exists(bootonmacOS.getRunnerFilename(runnerName, True)):
            position = "user"
        elif os.path.exists(bootonmacOS.getRunnerFilename(runnerName, False)):
        # TODO check if path exists even if no rights to list files there, so need to use superuser
            position = "system" 
        
        if position == "user":
            os.remove(bootonmacOS.getRunnerFilename(runnerName, True))
        elif position == "system":
            if bootonmacOS.checkIfSudoMode():
                os.remove(bootonmacOS.getRunnerFilename(runnerName, False))
            else: 
                # use sudo command in shell in order to make appear the sudo password input on the terminal
                os.system(f"sudo rm \"{bootonmacOS.getRunnerFilename(runnerName, False)}\"")
    
    # TODO check if path exists even if no rights to list files there, so need to use superuser
    def isRunnerInstalled(runnerName):
        """Check if a runner is installed on macOS."""
        if os.path.exists(bootonmacOS.getRunnerFilename(runnerName, True)) or os.path.exists(bootonmacOS.getRunnerFilename(runnerName, False)):
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
    
    def createRunnerFile(runner: Runner, filePath):
        """Create a runner file on macOS."""
                
        # Python 3.9+ only supports the dump() method, so we need to check for it.
        if hasattr(plistlib, 'dump'):
            with open(filePath, "wb") as runnerFile:
                plistlib.dump(bootonmacOS.makeRunnerPlist(runner), runnerFile)
        else:
            plistlib.writePlist(bootonmacOS.makeRunnerPlist(runner), filePath)
        
    def makeRunnerPlist(runner: Runner):
        """Create a runner plist in macOS LaunchAgents standard."""
        
        args = []
        args.append(runner.getCommand().replace(" ", "\ "))
        args.extend(runner.getArgs())
        
        return {
            "Label": runner.getName(),
            "ProgramArguments": args,
            "RunAtLoad": True
        }
        
    def checkIfSudoMode():
        """Check if the script is running in sudo mode on macOS.
           Check needed because if the script is not running in sudo mode, it will not be able to write to the system's LaunchDaemons folder."""
        return os.geteuid() == 0
    
    def disclaimer() -> str:
        return "-- If your command doesn't work, check in Settings -> Login Items if the command is correctly enabled there --"