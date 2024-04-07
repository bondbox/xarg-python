from time import time

from xarg import cmds

if __name__ == "__main__":
    cmds.initiate_logging(level="info")
    end = time() + 100
    while time() < end:
        cmds.logger.info(int(time() / 3))
