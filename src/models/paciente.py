from dataclasses import dataclass, asdict
from typing import Optional
import uuid

@dataclass
class Paciente:
    id: str
    nome: str
    data_nascimento: Optional[str] = None
    telefone: Optional[str] = None
    documento: Optional[str] = None


    @staticmethod
    def novo(nome: str, data_nascimento: Optional[str]=None, telefone: Optional[str]=None, documento: Optional[str]=None):
        return Paciente(id=str(uuid.uuid4()), nome=nome, data_nascimento=data_nascimento, telefone=telefone, documento=documento)

    def to_dict(self):
        return asdict(self)