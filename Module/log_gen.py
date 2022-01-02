import logging as log
import os

file = os.path.abspath("Log/")

log.basicConfig(
    level=log.INFO,
    format="%(asctime)s %(levelname)s -<%(processName)s>- [%(filename)s: %(funcName)s] ->> %(message)s",
    datefmt="%I:%M:%S",
    handlers=[
        log.FileHandler(f"{file}\data.log"),
        log.StreamHandler()],
)

if __name__ == "__main__":
    log.info('Prueba Exitosa')
    log.warning('Prueba exitosa')
    log.error('Prueba Exitosa')
    log.critical('Test exitoso')