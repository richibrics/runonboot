class Runner:
    def __init__(self, name, command):
        self.name = name
        self.command = command
    
    def getName(self):
        return self.name
    
    def getCommand(self):
        return self.command