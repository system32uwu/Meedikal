from dataclasses import dataclass

@dataclass
class Persona():
    nombre: str
    edad: int

def loop(obj):
    print(isinstance(obj,list))

    obj = [obj]
    print(f"len(obj): {len(obj)}")

loop()