from dataclasses import dataclass, asdict
from enum import Enum
import uuid
from typing import Optional


class Prioridade(Enum):
    NORMAL = "normal"
    PREFERENCIAL = "preferencial"
    EMERGENCIA = "emergencia"


@dataclass
class Agendamento:
    id: str
    numero: int
    paciente_id: str
    horario: Optional[str]
    motivo: Optional[str]
    prioridade: Prioridade = Prioridade.NORMAL
    status: str = "agendado" # agendado, chamado, cancelado, concluido


    @staticmethod
    def novo(numero: int, paciente_id: str, horario: Optional[str]=None, motivo: Optional[str]=None, prioridade: Prioridade=Prioridade.NORMAL):
        return Agendamento(id=str(uuid.uuid4()), numero=numero, paciente_id=paciente_id, horario=horario, motivo=motivo, prioridade=prioridade)


    def to_dict(self):
        d = asdict(self)
        d['prioridade'] = self.prioridade.value
        return d