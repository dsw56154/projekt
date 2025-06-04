import argparse
import os
import json
import yaml
import xml.etree.ElementTree as ET

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

    args.in_ext = os.path.splitext(args.input)[1].lower()
    args.out_ext = os.path.splitext(args.output)[1].lower()

    formaty = ['.xml', '.json', '.yml', '.yaml']

    if args.in_ext not in formaty:
        parser.error(f"Blad: Nieobslugiwany format pliku wejsciowego: {args.in_ext}. Obslugiwane to: {', '.join(formaty)}")

    if args.out_ext not in formaty:
        parser.error(f"Blad: Nieobslugiwany format pliku wyjsciowego: {args.out_ext}. Obslugiwane to: {', '.join(formaty)}")

    return args

############################## JSON

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

def savetojson(dane_obiekt, sciezka_pliku: str, indent: int = 4):
    try:
        with open(sciezka_pliku, 'w', encoding='utf-8') as f:
            json.dump(dane_obiekt, f, indent=indent, ensure_ascii=False)
        print(f"Dane zostaly pomyslnie zapisane do pliku '{sciezka_pliku}'.")
        return True
    except TypeError as e:
        print(f"Blad typu danych podczas zapisu do pliku '{sciezka_pliku}': {e}")
        return False
    except Exception as e:
        print(f"Wystapil nieoczekiwany blad podczas zapisu do pliku '{sciezka_pliku}': {e}")
        return False 

########################################################## YML + YAML
def yml_yamlf(sciezka_pliku: str):
    if not os.path.exists(sciezka_pliku):
        print(f"Blad: Plik nie znaleziony pod sciezka: {sciezka_pliku}")
        return None
    try:
        with open(sciezka_pliku, 'r', encoding='utf-8') as f:
            dane = yaml.safe_load(f)
        print(f"Plik '{sciezka_pliku}' zostal pomyslnie wczytany i jest poprawny skladniowo (YAML).")
        return dane
    except yaml.YAMLError as e:
        print(f"Blad skladni YAML w pliku '{sciezka_pliku}': {e}")
        return None
    except Exception as e:
        print(f"Wystapil nieoczekiwany blad podczas wczytywania pliku '{sciezka_pliku}': {e}")
        return None
    
def savetoyml_yaml(dane_obiekt, sciezka_pliku: str, indent: int = 2):
    try:
        with open(sciezka_pliku, 'w', encoding='utf-8') as f:
            yaml.dump(dane_obiekt, f, indent=indent, allow_unicode=True, default_flow_style=False, sort_keys=False)
        print(f"Dane zostaly pomyslnie zapisane do pliku '{sciezka_pliku}'.")
        return True
    except TypeError as e:
        print(f"Blad typu danych podczas zapisu do pliku '{sciezka_pliku}': {e}")
        return False
    except Exception as e:
        print(f"Wystapil nieoczekiwany blad podczas zapisu do pliku '{sciezka_pliku}': {e}")
        return False


########################################################## XML

def xmlf(sciezka_pliku: str):
    if not os.path.exists(sciezka_pliku):
        print(f"Blad: Plik nie znaleziony pod sciezka: {sciezka_pliku}")
        return None
    try:
        tree = ET.parse(sciezka_pliku)
        root = tree.getroot()
        dane = etree_to_dict(root)
        print(f"Plik '{sciezka_pliku}' zostal pomyslnie wczytany i jest poprawny skladniowo (XML).")
        return dane
    except ET.ParseError as e:
        print(f"Blad skladni XML w pliku '{sciezka_pliku}': {e}")
        return None
    except Exception as e:
        print(f"Wystapil nieoczekiwany blad podczas wczytywania pliku '{sciezka_pliku}': {e}")
        return None
# czarna magia;    
def _build_element_from_dict(tag, data):
    element = ET.Element(tag)
    if isinstance(data, dict):
        for key, value in data.items():
            if key == '@attributes':
                for attr_name, attr_value in value.items():
                    element.set(attr_name, str(attr_value))
            elif key == '#text':
                element.text = str(value)
            elif isinstance(value, list):
                for item in value:
                    child_element = _build_element_from_dict(key, item)
                    element.append(child_element)
            elif isinstance(value, dict):
                child_element = _build_element_from_dict(key, value)
                element.append(child_element)
            else: 
                child_element = ET.SubElement(element, key)
                child_element.text = str(value)
    elif data is not None: 
        element.text = str(data)
    return element

def savetoxml(dane_obiekt, sciezka_pliku: str, indent: int = 4):
    if not isinstance(dane_obiekt, dict) or not dane_obiekt:
        print("Blad: Nieprawidlowy obiekt danych do zapisu XML. Oczekiwano niepustego slownika.")
        return False
    try:
        root_tag = list(dane_obiekt.keys())[0]
        root_data = dane_obiekt[root_tag]
        
        root_element = _build_element_from_dict(root_tag, root_data)

        if hasattr(ET, 'indent'):
            ET.indent(root_element, space=" " * indent)

        tree = ET.ElementTree(root_element)
        with open(sciezka_pliku, 'wb') as f: 
            tree.write(f, encoding='utf-8', xml_declaration=True) 
        print(f"Dane zostaly pomyslnie zapisane do pliku '{sciezka_pliku}'.")
        return True
    except TypeError as e:
        print(f"Blad typu danych podczas zapisu do pliku '{sciezka_pliku}': {e}")
        print("Upewnij sie, ze dane_obiekt zawiera tylko typy danych kompatybilne z XML.")
        return False
    except Exception as e:
        print(f"Wystapil nieoczekiwany blad podczas zapisu do pliku '{sciezka_pliku}': {e}")
        return False

if __name__ == '__main__':
    try:
        args = parsowanie_arg()
    except SystemExit as e:
        print(f"Blad podczas parsowania argumentow: {e}")
    dane = None
    match args.in_ext:
        case ".json":
            dane = jsonf(args.input)
        case ".yml":
            dane = yml_yamlf(args.input)
        case ".yaml":
            dane = yml_yamlf(args.input)
        case ".xml":
            dane = xmlf(args.input)

    if dane is None:
        print(f"Blad: Nie udalo sie wczytac danych z pliku wejsciowego '{args.input}'.")
        exit(1)

    match args.out_ext:
        case ".json":
            savetojson(dane, args.output)
        case ".yml":
            savetoyml_yaml(dane, args.output)
        case ".yaml":
            savetoyml_yaml(dane, args.output)
        case ".xml":
            savetoxml(dane, args.output)