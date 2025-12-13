from typing import Optional
from models.agendamento import Agendamento, Prioridade
from models.atendimento import Atendimento
from models.paciente import Paciente
from repositories.json_repository import JsonRepository
from structures.priority_heap import PriorityHeap
from structures.stack import Stack
from structures.linked_list import LinkedList

class SchedulerService:
    def __init__(self, repo: JsonRepository):
        self.repo = repo
        self.heap_priorizados = PriorityHeap()
        self.fila_normais = [] # simples FIFO
        self.pilha_historico = Stack()
        self.lista_historico_encadeada = LinkedList()
        self._carregar_estado()
        
    def _carregar_estado(self):
        # Carrega do JSON para as estruturas em memória (apenas os agendamentos abertos/nao cancelados)
        ags = self.repo.listar_agendamentos()
        for a in ags:
            if a.get('status') in ('agendado', 'chamado'):
                if a.get('prioridade') in ('emergencia','preferencial'):
                    self.heap_priorizados.push(a)
                else:
                    self.fila_normais.append(a)
    
    def criar_paciente(self, nome: str, data_nasc: Optional[str]=None, telefone: Optional[str]=None, documento: Optional[str]=None) -> Paciente:
        p = Paciente.novo(nome=nome, data_nascimento=data_nasc, telefone=telefone, documento=documento)
        self.repo.salvar_paciente(p.to_dict())
        return p
    
    def criar_agendamento(self, paciente_id: str, horario: Optional[str]=None, motivo: Optional[str]=None, prioridade: Prioridade=Prioridade.NORMAL) -> Agendamento:
        numero = self.repo.obter_proximo_numero_agendamento()
        ag = Agendamento.novo(numero=numero, paciente_id=paciente_id, horario=horario, motivo=motivo, prioridade=prioridade)
        self.repo.salvar_agendamento(ag.to_dict())
        
        # inserir na estrutura correta
        d = ag.to_dict()
        
        if d['prioridade'] in ('emergencia','preferencial'):
            self.heap_priorizados.push(d)
        else:
            self.fila_normais.append(d)
        
        return ag
    
    def chamar_proximo_priorizado(self) -> Optional[dict]:        
        item = self.heap_priorizados.pop()
        
        if not item:
            return None
        
        # atualizar status no repo
        item['status'] = 'chamado'
        self.repo.atualizar_agendamento(item['id'], item)
        
        # empilhar no histórico (pilha)
        self.pilha_historico.push(item)
        self.lista_historico_encadeada.append(item)
        
        return item
    
    def chamar_proximo_normal(self) -> Optional[dict]:
        if not self.fila_normais:
            return None

        item = self.fila_normais.pop(0)
        item['status'] = 'chamado'
        
        # se for agendamento armazenado no repo, atualiza
        if 'id' in item:
            self.repo.atualizar_agendamento(item['id'], item)
        
        self.pilha_historico.push(item)
        self.lista_historico_encadeada.append(item)
        return item
    
    def priorizar_agendamento(self, agendamento_id: str):
        # localiza em fila_normais e move para heap
        for i,a in enumerate(self.fila_normais):
            if a.get('id') == agendamento_id:
                a['prioridade'] = 'preferencial'
                self.heap_priorizados.push(a)
                
                del self.fila_normais[i]
                
                # atualiza no repo
                if 'id' in a:
                    self.repo.atualizar_agendamento(a['id'], a)
                return True
        
        # se não estiver na fila_normais, pode estar no repo — atualize diretamente
        ags = self.repo.listar_agendamentos()
        for ag in ags:
            if ag['id'] == agendamento_id:
                ag['prioridade'] = 'preferencial'
                self.repo.atualizar_agendamento(ag['id'], ag)
                self.heap_priorizados.push(ag)
                return True
        return False

    def cancelar_agendamento(self, agendamento_id: str):
        ags = self.repo.listar_agendamentos()
        for ag in ags:
            if ag['id'] == agendamento_id and ag.get('status') not in ('cancelado','concluido'):
                ag['status'] = 'cancelado'
                self.repo.atualizar_agendamento(agendamento_id, ag)
                # remover de estruturas
                self.heap_priorizados.remove_by_id(agendamento_id)
                self.fila_normais = [a for a in self.fila_normais if a.get('id') != agendamento_id]
                return True
        return False
    
    def listar_priorizados(self):
        return self.heap_priorizados.to_list()

    def listar_normais(self):
        return list(self.fila_normais)

    def listar_historico_pilha(self):
        return self.pilha_historico.to_list()

    def listar_historico_encadeado(self):
        return self.lista_historico_encadeada.to_list()