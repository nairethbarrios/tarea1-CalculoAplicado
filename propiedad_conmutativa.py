import os
import random
from fractions import Fraction

import matplotlib.pyplot as plt


# Carpeta donde se guardan las figuras.
CARPETA_FIGURAS = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "figuras"
)


def guardar_figura(nombre):
    """
    Guarda la figura y crea la carpeta si todavía no existe.
    """

    os.makedirs(CARPETA_FIGURAS, exist_ok=True)

    ruta = os.path.join(
        CARPETA_FIGURAS,
        nombre
    )

    plt.savefig(ruta)
    plt.close()

    print(f"Figura guardada: figuras/{nombre}")


def generar_terminos(N):
    """
    Genera los términos:

        1 / (k(k + 1))
    """

    terminos = []

    for k in range(1, N + 1):

        terminos.append(
            1.0 / (k * (k + 1))
        )

    return terminos


def suma_mayor_a_menor(N):
    """
    Suma los términos desde el de mayor magnitud
    hasta el de menor magnitud.

    Como 1 / (k(k + 1)) decrece con k, el orden k = 1, ..., N
    ya es de mayor a menor módulo.
    """

    terminos = generar_terminos(N)

    suma = 0.0

    for termino in terminos:
        suma += termino

    return suma


def suma_menor_a_mayor(N):
    """
    Suma los términos desde el de menor magnitud
    hasta el de mayor magnitud.
    """

    terminos = generar_terminos(N)

    suma = 0.0

    for termino in reversed(terminos):
        suma += termino

    return suma


def suma_aleatoria(N):
    """
    Suma los términos en un orden aleatorio.
    """

    terminos = generar_terminos(N)

    random.shuffle(terminos)

    suma = 0.0

    for termino in terminos:
        suma += termino

    return suma


def suma_kahan(N):
    """
    Implementa la suma compensada de Kahan.
    """

    terminos = generar_terminos(N)

    suma = 0.0
    compensacion = 0.0

    for termino in terminos:

        y = termino - compensacion
        t = suma + y
        compensacion = (
            (t - suma) - y
        )
        suma = t

    return suma


def valor_teorico(N):
    """
    Calcula el valor teórico exacto:

        b_N = N / (N + 1)

    Se usa Fraction para que la referencia no tenga redondeo.
    """

    return Fraction(N, N + 1)


def error_relativo(resultado, teorico):
    """
    Calcula el error relativo entre un resultado en float
    y el valor teórico exacto.
    """

    return float(
        abs(Fraction(resultado) - teorico)
        / abs(teorico)
    )


def evaluar_algoritmos(N):

    teorico = valor_teorico(N)

    resultado_mayor = suma_mayor_a_menor(N)
    resultado_menor = suma_menor_a_mayor(N)
    resultado_aleatorio = suma_aleatoria(N)
    resultado_kahan = suma_kahan(N)

    return {
        "mayor": resultado_mayor,
        "menor": resultado_menor,
        "aleatorio": resultado_aleatorio,
        "kahan": resultado_kahan,
        "error_mayor": error_relativo(
            resultado_mayor,
            teorico
        ),
        "error_menor": error_relativo(
            resultado_menor,
            teorico
        ),
        "error_aleatorio": error_relativo(
            resultado_aleatorio,
            teorico
        ),
        "error_kahan": error_relativo(
            resultado_kahan,
            teorico
        )
    }


def _mostrar_progreso(indice, total):

    if indice % max(1, total // 10) == 0:

        porcentaje = (
            indice * 100
        ) // total

        print(
            f"Progreso: {porcentaje}%"
        )


def _calcular_experimento(valores_N):

    errores_mayor = []
    errores_menor = []
    errores_aleatorio = []
    errores_kahan = []

    total = len(valores_N)

    for indice, N in enumerate(
        valores_N,
        start=1
    ):

        resultados = evaluar_algoritmos(N)

        errores_mayor.append(
            resultados["error_mayor"]
        )

        errores_menor.append(
            resultados["error_menor"]
        )

        errores_aleatorio.append(
            resultados["error_aleatorio"]
        )

        errores_kahan.append(
            resultados["error_kahan"]
        )

        _mostrar_progreso(
            indice,
            total
        )

    return (
        errores_mayor,
        errores_menor,
        errores_aleatorio,
        errores_kahan
    )


def _graficar_errores(
    valores_N,
    errores_mayor,
    errores_menor,
    errores_aleatorio,
    errores_kahan,
    nombre
):

    plt.figure(figsize=(10, 6))

    plt.plot(
        valores_N,
        errores_mayor,
        label="Mayor a menor"
    )

    plt.plot(
        valores_N,
        errores_menor,
        label="Menor a mayor",
        linewidth=2.5
    )

    plt.plot(
        valores_N,
        errores_aleatorio,
        label="Aleatoria"
    )

    # Kahan y menor a mayor pueden coincidir: se usa línea punteada.
    plt.plot(
        valores_N,
        errores_kahan,
        label="Kahan",
        linestyle="--",
        color="black"
    )

    plt.yscale("log")

    plt.xlabel(r"$N$")
    plt.ylabel("Error relativo")

    plt.title(
        "Error relativo según el orden de suma"
    )

    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    guardar_figura(nombre)


def experimento_conmutativa():

    random.seed(12345)

    # Primer experimento.
    valores_N = list(
        range(10, 10001, 10)
    )

    print(
        "\nCalculando sumas para "
        "N = 10, 20, ..., 10000..."
    )

    (
        errores_mayor,
        errores_menor,
        errores_aleatorio,
        errores_kahan
    ) = _calcular_experimento(
        valores_N
    )

    print(
        "Generando gráfico..."
    )

    _graficar_errores(
        valores_N,
        errores_mayor,
        errores_menor,
        errores_aleatorio,
        errores_kahan,
        "conmutativa_hasta_10000.png"
    )

    # Segundo experimento.
    valores_N_grandes = list(
        range(1000, 1000001, 1000)
    )

    print(
        "\nCalculando sumas para "
        "N = 1.000, 2.000, ..., 1.000.000..."
    )

    (
        errores_mayor_grandes,
        errores_menor_grandes,
        errores_aleatorio_grandes,
        errores_kahan_grandes
    ) = _calcular_experimento(
        valores_N_grandes
    )

    N_final = 1_000_000

    resultados_finales = evaluar_algoritmos(
        N_final
    )

    print(
        f"\nResultados para N = {N_final:,}:"
        .replace(",", ".")
    )

    print(
        "Mayor a menor: "
        f"{resultados_finales['mayor']:.16f} | "
        f"error relativo = "
        f"{resultados_finales['error_mayor']:.3e}"
    )

    print(
        "Menor a mayor: "
        f"{resultados_finales['menor']:.16f} | "
        f"error relativo = "
        f"{resultados_finales['error_menor']:.3e}"
    )

    print(
        "Aleatoria: "
        f"{resultados_finales['aleatorio']:.16f} | "
        f"error relativo = "
        f"{resultados_finales['error_aleatorio']:.3e}"
    )

    print(
        "Kahan: "
        f"{resultados_finales['kahan']:.16f} | "
        f"error relativo = "
        f"{resultados_finales['error_kahan']:.3e}"
    )

    print(
        "Generando gráfico..."
    )

    _graficar_errores(
        valores_N_grandes,
        errores_mayor_grandes,
        errores_menor_grandes,
        errores_aleatorio_grandes,
        errores_kahan_grandes,
        "conmutativa_hasta_1000000.png"
    )

    # Se repite la suma aleatoria para observar su variabilidad.
    print(
        "\nCinco repeticiones de la suma aleatoria "
        f"para N = {N_final:,}:"
        .replace(",", ".")
    )

    for i in range(1, 6):

        resultado = suma_aleatoria(
            N_final
        )

        teorico = valor_teorico(
            N_final
        )

        error = error_relativo(
            resultado,
            teorico
        )

        print(
            f"Repetición {i}: "
            f"{resultado:.16f} | "
            f"error relativo = {error:.3e}"
        )