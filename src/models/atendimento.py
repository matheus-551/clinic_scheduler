from dataclasses import dataclass, asdict
import uuid
from typing import Optional

@dataclass
class Atendimento:
    id: str
    agendamento_id: Optional[str]
    paciente_id: str
    recebido_em: Optional[str]
    descricao: Optional[str]
    origem: str # 'com_agendamento' | 'sem_agendamento'
    status: str = 'aberto' # aberto, em_andamento, finalizado, cancelado


    @staticmethod
    def novo_sem_agendamento(paciente_id: str, recebido_em: Optional[str]=None, descricao: Optional[str]=None):
        return Atendimento(id=str(uuid.uuid4()), agendamento_id=None, paciente_id=paciente_id, recebido_em=recebido_em, descricao=descricao, origem='sem_agendamento')


    def to_dict(self):
        return asdict(self)