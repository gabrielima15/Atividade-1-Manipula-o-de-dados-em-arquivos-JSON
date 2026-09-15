import json


def read(fileName):
    try:
        with open(fileName, "r") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print("Error: 'data.json' file was not found.")
        
        
def write(fileName, dados):
    try:
        with open(fileName, "w", encoding="utf-8") as file:
            json.dump(dados, file, indent=4, ensure_ascii=False)
            
    except FileNotFoundError:
        print("error: problema no arquivo.")
