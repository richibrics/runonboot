import sys
from runonboot.runner.Runner import Runner

class PythonRunner(Runner):
    def __init__(self, name, python_arg: list):
        """ Runs on boot a python command, which is the parameter python_arg.
            e.g. python_arg = ["-c", "\"print('hello world')\""] will run the current python interpreter 
            with the command "print('hello world')" as if called in shell in this way:
            {python_interpreter} -c "print('hello\ world')"
        """
        super().__init__(name, "")
        self.python_arg = python_arg
        # get current interpreter
        self.interpreter = sys.executable
        
    def getCommand(self):
        return self.interpreter
    
    def getArgs(self):
        return self.python_arg