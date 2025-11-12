import json
from pathlib import Path
from threading import Lock
from typing import Any, Dict

class JsonRepository: 
    def __init__(self, caminho: str = 'data/db.json'):
        self.caminho = Path(caminho)
        self._lock = Lock()
        
        if not self.caminho.exists():
            self._inicializa_db()
        
    def _inicializa_db(self):
        inicial = {
        "pacientes": [],
        "agendamentos": [],
        "atendimentos": [],
        "ultimo_numero_agendamento": 0
        }
        self._write(inicial)
        
    def _read(self) -> Dict[str, Any]:
        with self._lock:
            with open(self.caminho, 'r', encoding='utf-8') as f:
                return json.load(f)
            
    def _write(self, data: Dict[str, Any]):
        with self._lock:
            with open(self.caminho, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
    def salvar_paciente(self, paciente_dict: Dict[str,Any]):
        db = self._read()
        db['pacientes'].append(paciente_dict)
        self._write(db)
        
    def listar_pacientes(self):
        return self._read()['pacientes']


    def salvar_agendamento(self, agendamento_dict: Dict[str,Any]):
        db = self._read()
        db['agendamentos'].append(agendamento_dict)
        db['ultimo_numero_agendamento'] = max(db.get('ultimo_numero_agendamento', 0), agendamento_dict.get('numero', 0))
        self._write(db)


    def atualizar_agendamento(self, agendamento_id: str, novo_dict: Dict[str,Any]):
        db = self._read()
        for i, a in enumerate(db['agendamentos']):
            if a['id'] == agendamento_id:
                db['agendamentos'][i] = novo_dict
                self._write(db)
                return True
        return False


    def listar_agendamentos(self):
        return self._read()['agendamentos']


    def salvar_atendimento(self, atendimento_dict: Dict[str,Any]):
        db = self._read()
        db['atendimentos'].append(atendimento_dict)
        self._write(db)

    def listar_atendimentos(self):
        return self._read()['atendimentos']


    def buscar_paciente_por_id(self, paciente_id: str):
        pacientes = self._read()['pacientes']
        for p in pacientes:
            if p['id'] == paciente_id:
                return p
        return None


    def obter_proximo_numero_agendamento(self):
        db = self._read()
        proximo = db.get('ultimo_numero_agendamento', 0) + 1
        db['ultimo_numero_agendamento'] = proximo
        self._write(db)
        return proximo