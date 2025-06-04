import argparse
import os
import json

def parsowanie_arg():
    parser = argparse.ArgumentParser(
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
        parser.error(f"Blad: Plik wejsciowy nie znaleziony: {args.input}")
    global in_ext,out_ext
    in_ext = os.path.splitext(args.input)[1].lower()
    out_ext = os.path.splitext(args.output)[1].lower()

    formaty = ['.xml', '.json', '.yml', '.yaml']

    if in_ext not in formaty:
        parser.error(f"Blad: Nieobslugiwany format pliku wejsciowego: {in_ext}. Obslugiwane to: {', '.join(formaty)}")

    if out_ext not in formaty:
        parser.error(f"Blad: Nieobslugiwany format pliku wyjsciowego: {out_ext}. Obslugiwane to: {', '.join(formaty)}")

    return args

def jsonf(sciezka_pliku: str):
    if not os.path.exists(sciezka_pliku):
        print(f"Blad: Plik nie znaleziony pod sciezka: {sciezka_pliku}")
        return None

    try:
        with open(sciezka_pliku, 'r', encoding='utf-8') as f:
            dane = json.load(f)
        print(f"Plik '{sciezka_pliku}' zostal pomyslnie wczytany i jest poprawny skladniowo.")
        return dane
    except json.JSONDecodeError as e:
        print(f"Blad skladni JSON w pliku '{sciezka_pliku}': {e}")
        return None
    except Exception as e:
        print(f"Wystapil nieoczekiwany blad podczas wczytywania pliku '{sciezka_pliku}': {e}")
        return None
    

if __name__ == '__main__':
    try:
        argumenty = parsowanie_arg()
    except SystemExit as e:
        print(f"Blad podczas parsowania argumentow: {e}")
    match in_ext:
        case "json":
            jsonf(input)
        case "yml":
            yml(input)
        case "yaml":
            yaml(input)
        case "xml":
            xml(input)