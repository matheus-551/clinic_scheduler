from PyQt6 import QtWidgets
from PyQt6.QtGui import QIcon, QCursor
from PyQt6.QtCore import Qt
import pyttsx3

from view.CreateAtendimentoView import CreateAtendimentoView
from view.CreateAgendamentoView import CreateAgendamentoView        

from services.scheduler_service import SchedulerService

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, scheduler_service: SchedulerService):
        super().__init__()
        self.scheduler = scheduler_service
        self.setWindowTitle("Clinic Scheduler")
        self.setFixedSize(800, 600)
        self.tts = pyttsx3.init()
        self.tts.setProperty("rate", 170)  # velocidade da fala
        self.tts.setProperty("volume", 1.0)  # volume máximo
        self._build_ui()
    
    def _build_ui(self):
        central = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()

        header = QtWidgets.QLabel('<h1>Clinic Scheduler</h1>')
        layout.addWidget(header)

        # area de filtro
        filtro_layout = QtWidgets.QHBoxLayout()
        self.input_filtro = QtWidgets.QLineEdit()
        self.input_filtro.setPlaceholderText('Buscar por nome, número ou atendimento...')
        
        btn_buscar = QtWidgets.QPushButton('Buscar')
        btn_buscar.clicked.connect(self.on_buscar)
        btn_buscar.setObjectName("btn_search")
        btn_buscar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        filtro_layout.addWidget(self.input_filtro)
        filtro_layout.addWidget(btn_buscar)
        layout.addLayout(filtro_layout)


        # botoes de navegacao
        botoes_layout = QtWidgets.QHBoxLayout()
        
        btn_novo_agendamento = QtWidgets.QPushButton('Novo Agendamento')
        btn_novo_agendamento.clicked.connect(self.on_novo_agendamento)
        btn_novo_agendamento.setObjectName("btn_primary")
        btn_novo_agendamento.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        btn_atendimento_sem = QtWidgets.QPushButton('Atendimento sem Agendamento')
        btn_atendimento_sem.clicked.connect(self.on_atendimento_sem)
        btn_atendimento_sem.setObjectName("btn_primary")
        btn_atendimento_sem.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        botoes_layout.addWidget(btn_novo_agendamento)
        botoes_layout.addWidget(btn_atendimento_sem)
        layout.addLayout(botoes_layout)
        
        # area de selecao de lista (Priorizados / Normais / Histórico)
        tabs_layout = QtWidgets.QHBoxLayout()
        self.btn_prio = QtWidgets.QPushButton('Priorizados')
        self.btn_normais = QtWidgets.QPushButton('Normais')
        self.btn_historico = QtWidgets.QPushButton('Histórico')
        self.btn_prio.setCheckable(True)
        self.btn_normais.setCheckable(True)
        self.btn_historico.setCheckable(True)
        self.btn_prio.setChecked(True)
        self.btn_prio.clicked.connect(lambda: self.mudar_lista('priorizados'))
        self.btn_normais.clicked.connect(lambda: self.mudar_lista('normais'))
        self.btn_historico.clicked.connect(lambda: self.mudar_lista('historico'))
        
        for btn in [self.btn_prio, self.btn_normais, self.btn_historico]:
            btn.setProperty("class", "tabButton")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)

        for btn in [self.btn_prio, self.btn_normais, self.btn_historico]:
            btn.style().unpolish(btn)
            btn.style().polish(btn)
        
        tabs_layout.addWidget(self.btn_prio)
        tabs_layout.addWidget(self.btn_normais)
        tabs_layout.addWidget(self.btn_historico)
        layout.addLayout(tabs_layout)


        # lista
        self.table = QtWidgets.QTableWidget()
        self.table.setObjectName("advancedTable")  # para estilizar via QSS
        self.table.setColumnCount(4)  # quantidade de colunas
        self.table.setHorizontalHeaderLabels(["Paciente", "Horário", "Prioridade", "Status"])

        self.table.setSelectionBehavior(QtWidgets.QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QtWidgets.QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)

        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

        layout.addWidget(self.table)

        # botoes chamar
        chamar_layout = QtWidgets.QHBoxLayout()
        
        btn_chamar_prio = QtWidgets.QPushButton('Chamar próximo priorizado')
        btn_chamar_prio.clicked.connect(self.on_chamar_prio)
        btn_chamar_prio.setObjectName("btnDanger")
        btn_chamar_prio.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        btn_chamar_normal = QtWidgets.QPushButton('Chamar próximo normal')
        btn_chamar_normal.clicked.connect(self.on_chamar_normal)
        btn_chamar_normal.setObjectName("btn_primary")
        btn_chamar_normal.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        chamar_layout.addWidget(btn_chamar_prio)
        chamar_layout.addWidget(btn_chamar_normal)
        
        layout.addLayout(chamar_layout)

        central.setLayout(layout)
        self.setCentralWidget(central)


        # preencher lista inicial
        self.atualizar_lista()
        
    def mudar_lista(self, tipo):
        # atualiza estado dos botões checkable
        self.btn_prio.setChecked(tipo=='priorizados')
        self.btn_normais.setChecked(tipo=='normais')
        self.btn_historico.setChecked(tipo=='historico')
        self.lista_atual = tipo
        self.atualizar_lista()
            
    def atualizar_lista(self):
        # limpa a tabela (remove todas as linhas)
        self.table.setRowCount(0)

        if getattr(self, 'lista_atual', 'priorizados') == 'priorizados':
            items = self.scheduler.listar_priorizados()
        elif self.lista_atual == 'normais':
            items = self.scheduler.listar_normais()
        else:
            items = self.scheduler.listar_historico_encadeado()

        for it in items:
            row = self.table.rowCount()
            self.table.insertRow(row)

            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(it.get("paciente_id", "(sem paciente)"))))
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(it.get("numero", "-"))))
            self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(it.get("prioridade", "Normal")).capitalize()))
            self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(it.get("status", ""))))
                
    def on_buscar(self):
        termo = self.input_filtro.text()
        
        # implementacao de busca simples: filtra listas em memoria
        resultados = []
        
        for a in self.scheduler.listar_priorizados() + self.scheduler.listar_normais():
            if termo.lower() in (str(a.get('numero','')).lower() + ' ' + str(a.get('paciente_id','')).lower() + ' ' + str(a.get('status','')).lower()):
                resultados.append(a)
        self.lista_widget.clear()
        for it in resultados:
            self.lista_widget.addItem(QtWidgets.QListWidgetItem(f"#{it.get('numero','-')} - {it.get('paciente_id')} - {it.get('prioridade')}"))
            
    def on_novo_agendamento(self):
        self.setCentralWidget(CreateAgendamentoView(self.scheduler, self.back_to_main))


    def on_atendimento_sem(self):
        self.setCentralWidget(CreateAtendimentoView(self.scheduler, self.back_to_main))


    def on_chamar_prio(self):
        item = self.scheduler.chamar_proximo_priorizado()
        
        if item:
            QtWidgets.QMessageBox.information(self, 'Chamando', f"Chamando: {item.get('paciente_id')} - Nº {item.get('numero','-')}")
            self.falar_chamada(item.get('paciente_id'), item.get('numero'))
            self.atualizar_lista()
        else:
            QtWidgets.QMessageBox.warning(self, 'Vazio', 'Não há pacientes priorizados')


    def on_chamar_normal(self):
        item = self.scheduler.chamar_proximo_normal()
        
        if item:
            QtWidgets.QMessageBox.information(self, 'Chamando', f"Chamando: {item.get('paciente_id')} - Nº {item.get('numero','-')}")
            self.falar_chamada(item.get('paciente_id'), item.get('numero'))
            self.atualizar_lista()
        else:
            QtWidgets.QMessageBox.warning(self, 'Vazio', 'Não há pacientes na fila normal')
            
    def back_to_main(self):
        self._build_ui()
        
    def falar_chamada(self, nome_paciente, ficha = None):
        texto = f"Paciente {nome_paciente}, ficha número {ficha}. Favor dirigir-se ao atendimento."
        self.tts.say(texto)
        self.tts.runAndWait()
        