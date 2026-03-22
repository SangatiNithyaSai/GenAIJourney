from dataclasses import dataclass

@dataclass
class Product:
    id: int
    name: str
    description: str
    quantity: int
    price: float
