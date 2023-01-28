import os
import sys

# python3 -c "import runonboot; runonboot.helper.moveFile()" SRC DEST
def moveFile():
    # Move a file from one position to another using passed arguments
    # Need this function to implement the file move with admin rights,
    # which needs to be done in a separate process, so instead of restarting
    # the entire script, simply call this function from another process.
    if len(sys.argv) < 3:
        raise Exception("Not enough arguments: pass the source and destination file names")
    src = sys.argv[1]
    dst = sys.argv[2]
    os.rename(src, dst)

# python3 -c "import runonboot; runonboot.helper.removeFile()" FILENAME
def removeFile():
    # Removes file passed as argument
    # Need this function to implement the file delete with admin rights,
    # which needs to be done in a separate process, so instead of restarting
    # the entire script, simply call this function from another process.
    if len(sys.argv) < 2:
        raise Exception("Not enough arguments: pass the file name")
    filename = sys.argv[1]
    if os.path.exists(filename):
        os.remove(filename)
    else:
        raise Exception("File does not exist: " + filename)