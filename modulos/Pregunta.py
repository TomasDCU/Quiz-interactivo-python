class Pregunta():
    def __init__(self,pregunta):
        self.pregunta = pregunta

    def imprimir(self):
        print(self.pregunta)


if __name__ == '__main__':
    prueba = Pregunta('Prueba Pregunta')
    prueba.imprimir()