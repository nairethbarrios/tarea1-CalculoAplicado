import os
import math

import matplotlib.pyplot as plt
from fractions import Fraction


# Carpeta donde se guardan las figuras de los experimentos.
CARPETA_FIGURAS = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "figuras"
)


def guardar_figura(nombre):
    """
    Crea la carpeta de figuras si es necesario,
    guarda la figura y muestra al usuario dónde se guardó.
    """

    os.makedirs(CARPETA_FIGURAS, exist_ok=True)

    ruta = os.path.join(
        CARPETA_FIGURAS,
        nombre
    )

    plt.savefig(ruta)
    plt.close()

    print(f"Figura guardada: figuras/{nombre}")


def b_directa(N):
    """
    Calcula b_N directamente:

        b_N = sum(1 / (k(k + 1)))
    """

    suma = 0.0

    for k in range(1, N + 1):

        suma += (
            1.0 / (k * (k + 1))
        )

    return suma


def b_telescopica(N):
    """
    Calcula b_N utilizando:

        1 / (k(k + 1)) = 1/k - 1/(k + 1)
    """

    suma = 0.0

    for k in range(1, N + 1):

        suma += (
            1.0 / k
            - 1.0 / (k + 1)
        )

    return suma


def b_teorico(N):
    return Fraction(
        N,
        N + 1
    )


def error_relativo(resultado, teorico):
    return float(
        abs(
            Fraction(resultado)
            - teorico
        )
        / abs(teorico)
    )


def c_racionalizada(N):
    """
    Utiliza la forma racionalizada:

        1 / (sqrt(k^2 + 1) + k)
    """

    suma = 0.0

    for k in range(1, N + 1):

        suma += 1.0 / (
            math.sqrt(k * k + 1) + k
        )

    return suma


def c_cancelacion(N):
    """
    Utiliza la forma:

        sqrt(k^2 + 1) - k

    Al restar dos números muy parecidos
    puede perderse precisión.
    """

    suma = 0.0

    for k in range(1, N + 1):

        suma += (
            math.sqrt(k * k + 1) - k
        )

    return suma


def experimento_representaciones():

    # Valores utilizados para estudiar el error relativo de b_N.
    valores_N = (
        [1]
        + list(
            range(10, 10001, 10)
        )
    )

    errores_directa = []
    errores_telescopica = []

    suma_directa = 0.0
    suma_telescopica = 0.0

    siguiente_N = iter(
        valores_N
    )

    objetivo = next(
        siguiente_N
    )

    # Las sumas se acumulan una sola vez para evitar recalcular.
    for k in range(1, 10001):

        suma_directa += (
            1.0 / (k * (k + 1))
        )

        suma_telescopica += (
            1.0 / k
            - 1.0 / (k + 1)
        )

        if k == objetivo:

            teorico = b_teorico(k)

            errores_directa.append(
                error_relativo(
                    suma_directa,
                    teorico
                )
            )

            errores_telescopica.append(
                error_relativo(
                    suma_telescopica,
                    teorico
                )
            )

            try:

                objetivo = next(
                    siguiente_N
                )

            except StopIteration:

                break

    plt.figure(
        figsize=(10, 6)
    )

    plt.plot(
        valores_N,
        errores_directa,
        label="Forma directa"
    )

    plt.plot(
        valores_N,
        errores_telescopica,
        label="Forma telescópica"
    )

    plt.yscale("log")

    plt.xlabel(r"$N$")
    plt.ylabel("Error relativo")

    plt.title(
        r"Error relativo de las representaciones de $b_N$"
    )

    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    guardar_figura(
        "representaciones_b.png"
    )

    # Se comparan las dos formas de c_N.
    valores_c = list(
        range(1, 10001)
    )

    diferencias = []

    suma_c1 = 0.0
    suma_c2 = 0.0

    for N in valores_c:

        k = N

        suma_c1 += 1.0 / (
            math.sqrt(k * k + 1) + k
        )

        suma_c2 += (
            math.sqrt(k * k + 1) - k
        )

        diferencias.append(
            abs(
                suma_c1 - suma_c2
            )
        )

    plt.figure(
        figsize=(10, 6)
    )

    plt.plot(
        valores_c,
        diferencias
    )

    plt.yscale("log")

    plt.xlabel(r"$N$")
    plt.ylabel(r"$D_N$")

    plt.title(
        r"Diferencia entre las dos representaciones de $c_N$"
    )

    plt.grid(True)
    plt.tight_layout()

    guardar_figura(
        "representaciones_c.png"
    )

    print(
        "\nDiferencias entre las representaciones de c_N:"
    )

    for N in [
        10,
        100,
        1000,
        5000,
        10000
    ]:

        c1 = c_racionalizada(N)
        c2 = c_cancelacion(N)

        print(
            f"N = {N}: "
            f"D_N = {abs(c1 - c2):.3e}"
        )


def experimento_bonus():

    valores_N = [
        10 ** x
        for x in range(1, 19)
    ]

    print(
        "\nComparación de las dos formas de b_N:"
    )

    for N_entero in valores_N:

        N = float(
            N_entero
        )

        forma_1 = (
            1.0
            - 1.0 / (N + 1.0)
        )

        forma_2 = (
            N / (N + 1.0)
        )

        teorico = Fraction(
            N_entero,
            N_entero + 1
        )

        error_1 = float(
            abs(
                Fraction(forma_1)
                - teorico
            )
            / abs(teorico)
        )

        error_2 = float(
            abs(
                Fraction(forma_2)
                - teorico
            )
            / abs(teorico)
        )

        diferencia = abs(
            forma_1 - forma_2
        )

        print(
            f"N = {N_entero:.0e}: "
            f"diferencia = {diferencia:.3e} | "
            f"error forma 1 = {error_1:.3e} | "
            f"error forma 2 = {error_2:.3e}"
        )

    print(
        "\nComparación de los términos de c_N:"
    )

    for k in [
        10,
        100,
        1000,
        10000,
        100000,
        1_000_000,
        10_000_000,
        100_000_000
    ]:

        forma_estable = 1.0 / (
            math.sqrt(k * k + 1) + k
        )

        forma_cancelacion = (
            math.sqrt(k * k + 1) - k
        )

        diferencia_relativa = abs(
            forma_estable
            - forma_cancelacion
        ) / abs(
            forma_estable
        )

        print(
            f"k = {k}: "
            f"diferencia relativa = "
            f"{diferencia_relativa:.3e}"
        )

    # Se buscan distintos niveles de pérdida de precisión.
    umbrales = [
        1e-8,
        1e-6,
        1e-4
    ]

    print(
        "\nPrimeros valores aproximados "
        "para distintos niveles de pérdida:"
    )

    for umbral in umbrales:

        primer_k = None

        for k in range(
            1,
            1_000_001
        ):

            forma_estable = 1.0 / (
                math.sqrt(k * k + 1) + k
            )

            forma_cancelacion = (
                math.sqrt(k * k + 1) - k
            )

            diferencia_relativa = abs(
                forma_estable
                - forma_cancelacion
            ) / abs(
                forma_estable
            )

            if diferencia_relativa > umbral:

                primer_k = k
                break

        if primer_k is not None:

            print(
                f"Umbral {umbral:.0e}: "
                f"k = {primer_k}"
            )