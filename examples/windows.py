import runonboot
from runonboot.runner.Runner import Runner
import time

if __name__ == "__main__":
    r = Runner("test", "test")
    print("runner status: " + str(runonboot.isRunnerInstalled("test")))
    print("Installing runner...")
    runonboot.installRunner(r, user_only=False)
    print("runner status: " + str(runonboot.isRunnerInstalled("test")))
    time.sleep(5)
    runonboot.removeRunner("test")
    print("runner status: " + str(runonboot.isRunnerInstalled("test")))
    