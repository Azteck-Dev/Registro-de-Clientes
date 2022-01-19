from PIL import Image
import os

class HandImg:
    def __init__(self, image_path:str, key_cliente:str):
        self._image_path = image_path
        self._key_client = key_cliente
        self._main_dir = os.path.abspath("Sources/clients")
        self._size = (110,90)
        self._name = None
        self._file = None

    def prepare_img(self):
        # Obtención del archivo.
        self._file = Image.open(self._image_path)
        # Renombrado del archivo.
        self._name = f"{self._main_dir}\{self._key_client}.png"
        # Redimencionamiento de la imagen y guardado.
        self._file.resize(self._size).save(self._name,"png")
        # Retorno de el path donde se guardo la nueva imagen.
        return self._name



if __name__ == "__main__":
    test = HandImg("Sources/clients/macdonal.jpg", "Mesach").prepare_img()
    print(test)