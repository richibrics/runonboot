class Runner:
    def __init__(self, name: str, command: str, args: list = []):
        self.name = name
        self.command = command
        self.args = args
    
    def getName(self) -> str:
        return self.name
    
    def getCommand(self) -> str:
        return self.command
    
    def getArgs(self) -> list:
        return self.args