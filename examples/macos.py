import runonboot
from runonboot.runner import PythonRunner
import time

if __name__ == "__main__":
    r = PythonRunner("test", ["/Users/mine/Downloads/PythonCode.py"])
    print("Installing the following command"," ".join([r.getCommand()] + r.getArgs()))
    print(runonboot.disclaimer())
    print("runner status: " + str(runonboot.isRunnerInstalled("test")))
    print("Installing runner...")
    runonboot.installRunner(r, user_only=True)
    print("runner status: " + str(runonboot.isRunnerInstalled("test")))
    time.sleep(5)
    print("Removing runner...")
    runonboot.removeRunner("test")
    print("runner status: " + str(runonboot.isRunnerInstalled("test")))
    