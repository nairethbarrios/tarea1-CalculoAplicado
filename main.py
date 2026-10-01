import propiedad_asociativa
import propiedad_conmutativa
import representaciones_suma


def mostrar_menu():

    while True:

        print(
            "\nOptimización numérica en una dimensión"
        )
        print("1. Propiedad asociativa")
        print("2. Bonus de propiedad asociativa")
        print("3. Propiedad conmutativa")
        print("4. Representaciones de una suma")
        print("5. Bonus de representaciones")
        print("6. Ejecutar todos los experimentos")
        print("0. Salir")

        opcion = input(
            "\nSeleccione una opción: "
        )

        if opcion == "1":

            print(
                "\nEjecutando propiedad asociativa..."
            )

            propiedad_asociativa.experimento_asociativa()

            print(
                "Propiedad asociativa finalizada."
            )

        elif opcion == "2":

            print(
                "\nEjecutando bonus de propiedad asociativa..."
            )

            propiedad_asociativa.experimento_bonus()

            print(
                "Bonus de propiedad asociativa finalizado."
            )

        elif opcion == "3":

            print(
                "\nEjecutando propiedad conmutativa..."
            )

            propiedad_conmutativa.experimento_conmutativa()

            print(
                "Propiedad conmutativa finalizada."
            )

        elif opcion == "4":

            print(
                "\nEjecutando representaciones de una suma..."
            )

            representaciones_suma.experimento_representaciones()

            print(
                "Representaciones de una suma finalizadas."
            )

        elif opcion == "5":

            print(
                "\nEjecutando bonus de representaciones..."
            )

            representaciones_suma.experimento_bonus()

            print(
                "Bonus de representaciones finalizado."
            )

        elif opcion == "6":

            ejecutar_todo()

        elif opcion == "0":

            print("Programa finalizado.")
            break

        else:

            print("Opción no válida.")


def ejecutar_todo():

    print("\nPropiedad asociativa")

    propiedad_asociativa.experimento_asociativa()

    print(
        "Propiedad asociativa finalizada."
    )

    print(
        "\nBonus de propiedad asociativa"
    )

    propiedad_asociativa.experimento_bonus()

    print(
        "Bonus de propiedad asociativa finalizado."
    )

    print("\nPropiedad conmutativa")

    propiedad_conmutativa.experimento_conmutativa()

    print(
        "Propiedad conmutativa finalizada."
    )

    print(
        "\nRepresentaciones de una suma"
    )

    representaciones_suma.experimento_representaciones()

    print(
        "Representaciones de una suma finalizadas."
    )

    print(
        "\nBonus de representaciones"
    )

    representaciones_suma.experimento_bonus()

    print(
        "Bonus de representaciones finalizado."
    )

    print(
        "\nTodos los experimentos finalizaron."
    )


if __name__ == "__main__":
    mostrar_menu()
