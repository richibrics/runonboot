import os
from .bootonPlatform import bootonPlatform

# Windows runs on boot all the executable files in the Startup folder.
# Since it's not convenient to create an executable file for each runner, 
# we will create a simple BAT file, which is still executable for windows.
class bootonWindows(bootonPlatform):
    def installRunner(runner, user_only=True):
        """Install a runner to run on boot on Windows."""
        if bootonWindows.isRunnerInstalled(runner.getName()):
            raise Exception("Runner already installed")
        
        if user_only:
            newRunnerPosition = bootonWindows.getRunnerFilename(runner.getName(), True)
            bootonWindows.createRunnerFile(runner, newRunnerPosition)
        else:
            # Save the bat file in a temp position and use cmd command with runas to move the file
            # in the final position using admin rights (this avoids UAC implementation)
            scriptFolder = os.path.dirname(os.path.realpath(__file__))
            tmpRunnerPosition = os.path.join(scriptFolder, runner.getName() + ".booton")
            finalRunnerPosition = bootonWindows.getRunnerFilename(runner.getName(), False)
            bootonWindows.createRunnerFile(runner, tmpRunnerPosition)

            raise Exception("Not implemented yet") # TODO Windows install in not user only mode
    
    def removeRunner(runnerName):
        """Remove a runner from running on boot."""
        if not bootonWindows.isRunnerInstalled(runnerName):
            raise Exception("Runner is not installed")
    
        # Check where it is installed
        position = None
        if os.path.exists(bootonWindows.getRunnerFilename(runnerName, True)):
            position = "user"
        else:
            raise Exception("Not implemented yet") # TODO Windows remove in not user only mode
        #elif os.path.exists(bootonWindows.getRunnerFilename(runnerName, False)):
        #    position = "common"
    
        if position == "user":
            os.remove(bootonWindows.getRunnerFilename(runnerName, True))
        
    
    def isRunnerInstalled(runnerName):
        """Check if a runner is installed to run on boot."""
        # Check bot in user only folder and all users folder
        if os.path.exists(bootonWindows.getRunnerFilename(runnerName, True)) or os.path.exists(bootonWindows.getRunnerFilename(runnerName, False)):
            return True
        return False
    
    def createRunnerFile(runner, position):
        """Create a runner file at the given position for Windows."""
        with open(position, "w") as runnerFile:
            runnerFile.write(bootonWindows.makeBatContent(runner))
    
    def makeBatContent(runner) -> str:
        """Make the content of a BAT file for the given runner."""
        return runner.getCommand()
    
    def getRunnerFilename(runnerName, user_only=True):
        """Get the file name of a runner file for Windows.
           If user_only is True, with the user's folder is returned. Otherwise, with the all users' folder is returned."""
        return os.path.join(bootonWindows.getAgentsFolder(user_only), runnerName + ".bat")
    
    def getAgentsFolder(user_only=True):
        """Get the folder where the startup files are stored on Windows.
           If user_only is True, the user's folder is returned. Otherwise, the all users' folder is returned."""
        mode = 0 if user_only else 1
        try:
            from win32com.shell import shell, shellcon 
            return shell.SHGetFolderPath(0, (shellcon.CSIDL_STARTUP, shellcon.CSIDL_COMMON_STARTUP)[mode], None, 0)
        except:
            try:
                # use fallback system
                if user_only:
                    return os.path.join(os.environ['USERPROFILE'], 'AppData', 'Roaming', 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
                else:
                    return os.path.join(os.environ['PROGRAMDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'StartUp')
            except:
                raise Exception("Can't get Startup folder path.")


    def disclaimer() -> str:
        return ""
