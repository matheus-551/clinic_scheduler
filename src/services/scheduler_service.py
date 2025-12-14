import copy
from typing import Optional
from models.agendamento import Agendamento, Prioridade
from models.paciente import Paciente
from repositories.json_repository import JsonRepository
from structures.priority_heap import PriorityHeap
from structures.stack import Stack


class SchedulerService:
    def __init__(self, repo: JsonRepository):
        self.repo = repo
        self.heap_priorizados = PriorityHeap()
        self.fila_normais = []  # FIFO
        self.pilha_historico = Stack()
        self._carregar_estado()

    def _carregar_estado(self):
        ags = self.repo.listar_agendamentos()

        for a in ags:
            if a.get('status') == 'agendado':
                if a.get('prioridade') in ('emergencia', 'preferencial'):
                    self.heap_priorizados.push(a)
                else:
                    self.fila_normais.append(a)

            elif a.get('status') == 'chamado':
                # histórico SEM duplicação de referência
                self.pilha_historico.push(copy.deepcopy(a))

    # ------------------ PACIENTE ------------------

    def criar_paciente(self, nome: str, data_nasc=None, telefone=None, documento=None) -> Paciente:
        p = Paciente.novo(
            nome=nome,
            data_nascimento=data_nasc,
            telefone=telefone,
            documento=documento
        )
        self.repo.salvar_paciente(p.to_dict())
        return p

    # ------------------ AGENDAMENTO ------------------

    def criar_agendamento(
        self,
        paciente_id: str,
        horario: Optional[str] = None,
        motivo: Optional[str] = None,
        prioridade: Prioridade = Prioridade.NORMAL
    ) -> Agendamento:

        numero = self.repo.obter_proximo_numero_agendamento()
        ag = Agendamento.novo(
            numero=numero,
            paciente_id=paciente_id,
            horario=horario,
            motivo=motivo,
            prioridade=prioridade
        )

        d = ag.to_dict()
        self.repo.salvar_agendamento(d)

        if d['prioridade'] in ('emergencia', 'preferencial'):
            self.heap_priorizados.push(d)
        else:
            self.fila_normais.append(d)

        return ag

    # ------------------ CHAMADAS ------------------

    def chamar_proximo_priorizado(self) -> Optional[dict]:
        item = self.heap_priorizados.pop()
        if not item:
            return None

        return self._finalizar_chamada(item)

    def chamar_proximo_normal(self) -> Optional[dict]:
        if not self.fila_normais:
            return None

        item = self.fila_normais.pop(0)
        return self._finalizar_chamada(item)

    def _finalizar_chamada(self, item: dict) -> dict:
        item['status'] = 'chamado'

        if 'id' in item:
            self.repo.atualizar_agendamento(item['id'], item)

        # histórico SEM referência compartilhada
        self.pilha_historico.push(copy.deepcopy(item))

        return item

    # ------------------ OUTRAS OPERAÇÕES ------------------

    def priorizar_agendamento(self, agendamento_id: str) -> bool:
        for i, a in enumerate(self.fila_normais):
            if a.get('id') == agendamento_id:
                a['prioridade'] = 'preferencial'
                self.heap_priorizados.push(a)
                del self.fila_normais[i]

                self.repo.atualizar_agendamento(a['id'], a)
                return True

        return False

    def cancelar_agendamento(self, agendamento_id: str) -> bool:
        ags = self.repo.listar_agendamentos()

        for ag in ags:
            if ag['id'] == agendamento_id and ag['status'] not in ('cancelado', 'concluido'):
                ag['status'] = 'cancelado'
                self.repo.atualizar_agendamento(agendamento_id, ag)

                self.heap_priorizados.remove_by_id(agendamento_id)
                self.fila_normais = [
                    a for a in self.fila_normais
                    if a.get('id') != agendamento_id
                ]
                return True

        return False

    # ------------------ LISTAGENS ------------------

    def listar_priorizados(self):
        return self.heap_priorizados.to_list()

    def listar_normais(self):
        return list(self.fila_normais)

    def listar_historico(self):
        return list(reversed(self.pilha_historico.to_list()))
