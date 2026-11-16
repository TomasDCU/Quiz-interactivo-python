from dataclasses import dataclass, field
from typing import ClassVar # Indica que COMODINES pertenece a ClassVar y no es un campo de la clase Jugador

TIEMPO_PREGUNTA = 30

@dataclass # El decorador genera el __init__
class Jugador:
    COMODINES: ClassVar[frozenset[str]] = frozenset({"50_50", "saltar"}) # Representa al unico jugador de una partida individual

    # No se usa init aca, se definen los datatypes para no recibir un nombre erroneo y declarar variables iniciales
    nombre: str
    puntaje: int = 0
    aciertos: int = 0
    tiempo: int = TIEMPO_PREGUNTA
    _comodines_usados: set[str] = field(default_factory=set, init=False) # Registro de comodines ya usados

    def __post_init__(self):
        if not isinstance(self.nombre, str):
            raise TypeError("El nombre debe ser una cadena de texto")
        self.nombre = self.nombre.strip() or "Jugador" # Si el nombre del jugador es un espacio se asigna 'Jugador'
        if (not isinstance(self.tiempo, int) or isinstance(self.tiempo, bool) or self.tiempo <= 0):
            raise ValueError("El tiempo por pregunta debe ser un numero entero positivo")

    def registrar_acierto(self, puntos: int):
        if puntos <= 0:
            raise ValueError("Los puntos por acierto deben ser mayores que cero")
        self.puntaje += puntos
        self.aciertos += 1

    def tiene_comodin(self, nombre: str) -> bool: # Indica si el jugador todavía puede usar el comodin en esta partida
        if nombre not in self.COMODINES:
            raise ValueError(f"El comodin '{nombre}' indicado no existe")
        return nombre not in self._comodines_usados

    def registrar_uso_comodin(self, nombre: str): # Registra el uso luego de que el gestor valida la accion
        if not self.tiene_comodin(nombre):
            raise RuntimeError(f"El comodin {nombre} ya fue usado en esta partida")
        self._comodines_usados.add(nombre)

    def reiniciar_comodines(self): # Reinicia los comodines al iniciar una nueva partida
        self._comodines_usados.clear()


if __name__ == "__main__":
    jugador = Jugador(" Tomas ")
    assert jugador.nombre == "Tomas" # Si devuelve True continua la ejecucion de prueba
    assert jugador.tiempo == TIEMPO_PREGUNTA
    assert jugador.puntaje == 0 and jugador.aciertos == 0

    jugador.registrar_acierto(10)
    assert jugador.puntaje == 10 and jugador.aciertos == 1

    assert jugador.tiene_comodin("50_50")
    jugador.registrar_uso_comodin("50_50")
    assert not jugador.tiene_comodin("50_50")
    assert jugador.tiene_comodin("saltar")
    jugador.registrar_uso_comodin("saltar")

    try:
        assert jugador.tiene_comodin("saltaron")
    except ValueError as error:
        print(f"Uso inexistente controlado de valor: {error}")
        # Uso inexistente controlado de valor: El comodin 'saltaron' indicado no existe

    try:
        jugador.registrar_uso_comodin("50_50")
    except RuntimeError as error:
        print(f"Uso repetido controlado: {error}")
        # Uso repetido controlado: El comodin 50_50 ya fue usado en esta partida

    try:
        jugador.registrar_uso_comodin("saltar")
    except RuntimeError as error:
        print(f"Uso repetido controlado: {error}")
        # Uso repetido controlado: El comodin saltar ya fue usado en esta partida

    jugador.reiniciar_comodines()
    assert jugador.tiene_comodin("50_50")
    print(f"Prueba completada: {jugador.nombre}, {jugador.puntaje} puntos y {jugador.aciertos} acierto(s)")
    # Prueba completada: Tomas, 10 puntos y 1 acierto(s)