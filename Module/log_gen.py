import logging as log
import os

file = os.path.abspath("Log/")

log.basicConfig(
    level=log.WARNING,
    format="%(asctime)s %(levelname)s :::%(filename)s::: [%(funcName)s Line: %(lineno)d] ->> %(message)s",
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