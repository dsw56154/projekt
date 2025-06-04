import argparse
import os

def parsowanie_arg():
    parser = argparse.ArgumentParser(
        description="Program do konwersji danych między formatami .xml, .json i .yml.",
        usage="%(prog)s plik_wejsciowy.x plik_wyjsciowy.y"
    )

    parser.add_argument(
        'input',
        type=str,
    )

    parser.add_argument(
        'output',
        type=str,
    )

    args = parser.parse_args()

    if not os.path.exists(args.input):
        parser.error(f"Błąd: Plik wejściowy nie znaleziony: {args.input}")

    roz_wej = os.path.splitext(args.input)[1].lower()
    roz_wyj = os.path.splitext(args.output)[1].lower()

    obslugiwane_form = ['.xml', '.json', '.yml', '.yaml']

    if roz_wej not in obslugiwane_form:
        parser.error(f"Błąd: Nieobsługiwany format pliku wejściowego: {roz_wej}. Obsługiwane to: {', '.join(obslugiwane_form)}")

    if roz_wyj not in obslugiwane_form:
        parser.error(f"Błąd: Nieobsługiwany format pliku wyjściowego: {roz_wyj}. Obsługiwane to: {', '.join(obslugiwane_form)}")

    return args

if __name__ == '__main__':
    try:
        argumenty = parsowanie_arg()
        print("Argumenty sparsowane pomyślnie:")
        print(f"Plik Wejściowy: {argumenty.input}")
        print(f"Plik Wyjściowy: {argumenty.output}")
        print(f"Format Wejściowy: {os.path.splitext(argumenty.input)[1].lower()}")
        print(f"Format Wyjściowy: {os.path.splitext(argumenty.output)[1].lower()}")
    except SystemExit as e:
        print(f"Błąd podczas parsowania argumentów: {e}")