## Clinic Scheduler

Projeto acadêmico (uso educacional) desenvolvido para a disciplina de Estruturas de Dados. O objetivo é aplicar conceitos da disciplina construindo um sistema simples de agendamento clínico — pretende-se ser um projeto didático, não uma solução para produção.

### Estrutura de pastas adotada

```
readme.md
src/
	ClinicScheduler.py
	styles.qss
	data/
		db.json
	helpers/
		tts_helper.py
	models/
		agendamento.py
		paciente.py
	repositories/
		json_repository.py
	services/
		scheduler_service.py
	structures/
		linked_list.py
		priority_heap.py
		stack.py
	view/
		CreateAgendamentoView.py
		MainWindow.py
```

### Pré-requisitos

- Python 3.10+ (ou versão compatível).
- Recomenda-se usar um ambiente virtual (`venv`).

Bibliotecas utilizadas (principais): `PyQt6` (interface gráfica) e `pyttsx3` (TTS). Se preferir, instale as dependências via `pip` conforme abaixo.

### Configuração (primeira vez)

No Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install PyQt6 pyttsx3
```

No Windows (cmd):

```cmd
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install PyQt6 pyttsx3
```

Se você preferir um arquivo `requirements.txt`, crie-o com as bibliotecas acima e rode `pip install -r requirements.txt`.

### Como executar

Execute a aplicação a partir da raiz do projeto:

```bash
python src/ClinicScheduler.py
```

Isso inicializa a aplicação gráfica (`PyQt6`). Se houver problemas com o TTS (`pyttsx3`), a aplicação continuará funcionando sem a funcionalidade de voz.

### Observações educacionais

- Este projeto foi criado como material de apoio para a disciplina de Estruturas de Dados; implementações nas pastas `structures/` (por exemplo `linked_list.py`, `priority_heap.py` e `stack.py`) servem para demonstrar estruturas e algoritmos.
- O foco é didático: clareza de código e exemplos de uso são mais importantes do que otimizações para produção.

Se quiser, posso gerar um `requirements.txt` e/ou adicionar instruções para empacotar a aplicação em um executável.
