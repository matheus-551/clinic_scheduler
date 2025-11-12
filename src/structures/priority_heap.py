import heapq
from typing import Any


class PriorityHeap:
    def __init__(self):
        self._heap = []
        self._counter = 0

    def _prio_value(self, prioridade_str: str) -> int:
        mapping = {'emergencia': 0, 'preferencial': 1, 'normal': 2}
        return mapping.get(prioridade_str, 2)

    def push(self, agendamento: dict):
        prio = self._prio_value(agendamento.get('prioridade','normal'))
        heapq.heappush(self._heap, (prio, self._counter, agendamento))
        self._counter += 1

    def pop(self) -> Any:
        if not self._heap:
            return None
        
        return heapq.heappop(self._heap)[2]

    def peek(self) -> Any:
        if not self._heap:
            return None
        return self._heap[0][2]

    def to_list(self):
        # retorna cópias ordenadas sem modificar o heap
        return [item[2] for item in sorted(self._heap)]

    def remove_by_id(self, agendamento_id: str):
        # remova por id (marcação preguiçosa: rebuild do heap)
        new = [t for t in self._heap if t[2].get('id') != agendamento_id]
        self._heap = new
        heapq.heapify(self._heap)