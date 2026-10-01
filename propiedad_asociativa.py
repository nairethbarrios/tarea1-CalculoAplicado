import os

import numpy as np
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


def calcular_asociativas(b, N, tipo):
    """
    Calcula las tres formas de la suma:

    1 + b^k - b^k
    (1 + b^k) - b^k
    (1 - b^k) + b^k
    """

    suma_1 = tipo(0)
    suma_2 = tipo(0)
    suma_3 = tipo(0)

    potencia = tipo(1)

    for k in range(1, N + 1):

        potencia *= tipo(b)

        suma_1 += 1 + potencia - potencia
        suma_2 += (1 + potencia) - potencia
        suma_3 += (1 - potencia) + potencia

    return suma_1, suma_2, suma_3


def _calcular_experimento_hasta_1000(b, tipo):
    """
    Calcula las tres sumas para N = 1, ..., 1000.
    """

    resultados_1 = []
    resultados_2 = []
    resultados_3 = []
    valores_validos = []

    for N in range(1, 1001):

        suma_1, suma_2, suma_3 = calcular_asociativas(
            b,
            N,
            tipo
        )

        if tipo is float and not all(
            np.isfinite(
                [suma_1, suma_2, suma_3]
            )
        ):
            break

        resultados_1.append(suma_1)
        resultados_2.append(suma_2)
        resultados_3.append(suma_3)
        valores_validos.append(N)

    return (
        valores_validos,
        resultados_1,
        resultados_2,
        resultados_3
    )


def _graficar_asociativa(
    b,
    tipo,
    nombre,
    valores_validos,
    resultados_1,
    resultados_2,
    resultados_3
):
    """
    Genera y guarda la gráfica del experimento.
    """

    plt.figure(figsize=(9, 5))

    plt.plot(
        valores_validos,
        valores_validos,
        label=r"Valor teórico $a_N=N$",
        linestyle="--",
        linewidth=2
    )

    plt.plot(
        valores_validos,
        resultados_1,
        label=r"$1+b^k-b^k$",
        linestyle="-",
        linewidth=1.5
    )

    plt.plot(
        valores_validos,
        resultados_2,
        label=r"$(1+b^k)-b^k$",
        linestyle=":",
        linewidth=2
    )

    plt.plot(
        valores_validos,
        resultados_3,
        label=r"$(1-b^k)+b^k$",
        linestyle="-.",
        linewidth=1.5
    )

    base_mostrada = (
        float(b)
        if tipo is float
        else b
    )

    plt.title(
        rf"Propiedad asociativa: $b={base_mostrada}$, "
        rf"tipo={nombre}"
    )

    plt.xlabel(r"$N$")
    plt.ylabel(r"$a_N$")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    guardar_figura(
        f"asociativa_{nombre}_b{b}.png"
    )


def experimento_asociativa():
    """
    Realiza el experimento principal para las bases
    indicadas, utilizando int y float.
    """

    bases = [2, 3, 5, 10]

    # Se comparan las expresiones con enteros y floats.
    for tipo, nombre in [
        (int, "int"),
        (float, "float")
    ]:

        for b in bases:

            (
                valores_validos,
                resultados_1,
                resultados_2,
                resultados_3
            ) = _calcular_experimento_hasta_1000(
                b,
                tipo
            )

            _graficar_asociativa(
                b,
                tipo,
                nombre,
                valores_validos,
                resultados_1,
                resultados_2,
                resultados_3
            )


def experimento_bonus():
    """
    Realiza los experimentos adicionales de la propiedad asociativa.
    """

    # Se prueban bases menores o iguales que 1.
    bases = [0, 0.5, 1]

    for b in bases:

        valores = []
        resultados = []

        suma = 0.0
        potencia = 1.0

        for N in range(1, 1001):

            potencia *= b

            suma += (
                1.0
                + potencia
                - potencia
            )

            valores.append(N)
            resultados.append(suma)

        maximo_error = max(
            abs(resultado - N)
            for resultado, N in zip(
                resultados,
                valores
            )
        )

        print(
            f"b = {b}: "
            f"máx |a_N - N| = {maximo_error:.3e}"
        )

        plt.figure(figsize=(9, 5))

        plt.plot(
            valores,
            valores,
            label=r"Valor teórico $a_N=N$",
            linestyle="--",
            linewidth=2
        )

        plt.plot(
            valores,
            resultados,
            label=r"$1+b^k-b^k$",
            linestyle="-",
            linewidth=1.5
        )

        plt.title(
            rf"Propiedad asociativa: $b={b}$"
        )

        plt.xlabel(r"$N$")
        plt.ylabel(r"$a_N$")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        guardar_figura(
            f"bonus_b_menor_igual_1_b{b}.png"
        )

    # Se prueba el comportamiento de los enteros grandes.
    N = 100000
    b = 10

    suma = 0
    potencia = 1

    for k in range(1, N + 1):

        potencia *= b
        suma += 1 + potencia - potencia

    print(
        f"Suma con int de Python para N={N}: {suma}"
    )

    # Se muestra el límite de los enteros de tamaño fijo.
    try:

        p = np.array(
            [10**18],
            dtype=np.int64
        )

        print(
            "10^18 como int64:",
            p[0]
        )

        print(
            "10^18 * 10 como int64:",
            p * 10
        )

        uno = np.array(
            [1],
            dtype=np.int64
        )

        print(
            "(1 + 10^18) - 10^18 con int64:",
            (uno + p) - p
        )

    except Exception as error:

        print(
            f"No se pudo realizar la prueba con int64: {error}"
        )

    try:

        float(10 ** 400)

    except OverflowError:

        print(
            "float(10^400) produce OverflowError."
        )

    # Se repite el experimento con bases negativas.
    bases_negativas = [-2, -3, -5, -10]

    for tipo, nombre in [
        (int, "int"),
        (float, "float")
    ]:

        for b in bases_negativas:

            (
                valores_validos,
                resultados_1,
                resultados_2,
                resultados_3
            ) = _calcular_experimento_hasta_1000(
                b,
                tipo
            )

            _graficar_asociativa(
                b,
                tipo,
                nombre,
                valores_validos,
                resultados_1,
                resultados_2,
                resultados_3
            )