from PyQt6 import QtWidgets
from PyQt6.QtGui import QIcon, QCursor
from PyQt6.QtCore import Qt

from models.agendamento import Prioridade
from view.CreateAgendamentoView import CreateAgendamentoView        

from helpers.tts_helper import tts
from services.scheduler_service import SchedulerService

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, scheduler_service: SchedulerService):
        super().__init__()
        self.scheduler = scheduler_service
        self.setWindowTitle("Clinic Scheduler")
        self.setMinimumSize(800, 600)
        self._build_ui()
    
    def _build_ui(self):
        central = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()

        header = QtWidgets.QLabel('<h1>Clinic Scheduler</h1>')
        layout.addWidget(header)

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

        botoes_layout = QtWidgets.QHBoxLayout()
        
        btn_novo_agendamento = QtWidgets.QPushButton('Novo Agendamento')
        btn_novo_agendamento.clicked.connect(self.on_novo_agendamento)
        btn_novo_agendamento.setObjectName("btn_primary")
        btn_novo_agendamento.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        botoes_layout.addWidget(btn_novo_agendamento)
        layout.addLayout(botoes_layout)
        
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
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Ficha", "Paciente", "Horário", "Prioridade", "Status"
        ])

        self.table.setSelectionBehavior(QtWidgets.QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QtWidgets.QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)

        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

        layout.addWidget(self.table)
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

        self.table.itemDoubleClicked.connect(self.on_detalhes)
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.abrir_menu_contexto)
        self.atualizar_lista()
        
    def mudar_lista(self, tipo):
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
            items = self.scheduler.listar_historico ()

        for it in items:
            row = self.table.rowCount()
            self.table.insertRow(row)

            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(it.get("numero", "-"))))
            item_ficha = QtWidgets.QTableWidgetItem(str(it.get("numero", "-")))
            item_ficha.setData(Qt.ItemDataRole.UserRole, it.get("id"))

            self.table.setItem(row, 0, item_ficha)
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(it.get("paciente_id", "(sem paciente)"))))
            self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(it.get("horario", ""))))
            self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(it.get("prioridade", "Normal")).capitalize()))
            self.table.setItem(row, 4, QtWidgets.QTableWidgetItem(str(it.get("status", ""))))
                
    def on_buscar(self):
        termo = self.input_filtro.text().strip().lower()

        # limpa tabela
        self.table.setRowCount(0)

        if not termo:
            self.atualizar_lista()
            return

        # busca em priorizados + normais
        todos = self.scheduler.listar_priorizados() + self.scheduler.listar_normais()

        resultados = []
        for a in todos:
            texto = (
                f"{a.get('numero','')} "
                f"{a.get('paciente_id','')} "
                f"{a.get('status','')}"
            ).lower()

            if termo in texto:
                resultados.append(a)

        # popula tabela com resultados
        for it in resultados:
            row = self.table.rowCount()
            self.table.insertRow(row)

            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(it.get("numero", "-"))))
            item_ficha = QtWidgets.QTableWidgetItem(str(it.get("numero", "-")))
            item_ficha.setData(Qt.ItemDataRole.UserRole, it.get("id"))

            self.table.setItem(row, 0, item_ficha)
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(it.get("paciente_id", "(sem paciente)"))))
            self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(it.get("horario", ""))))
            self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(it.get("prioridade", "normal")).capitalize()))
            self.table.setItem(row, 4, QtWidgets.QTableWidgetItem(str(it.get("status", ""))))
    
    def abrir_menu_contexto(self, pos):
        item = self.table.itemAt(pos)
        if not item:
            return

        row = item.row()
        agendamento_id = self.table.item(row, 0).data(Qt.ItemDataRole.UserRole)
        ag = self.buscar_agendamento_por_id(agendamento_id)

        menu = QtWidgets.QMenu(self)
        menu.setObjectName("contextMenu")

        ac_chamar = menu.addAction("📢 Chamar este paciente")
        ac_priorizar = menu.addAction("⭐ Tornar preferencial")
        ac_cancelar = menu.addAction("❌ Cancelar agendamento")

        acao = menu.exec(self.table.mapToGlobal(pos))

        if acao == ac_chamar:
            self.chamar_especifico(ag)
        elif acao == ac_priorizar:
            self.priorizar_agendamento(agendamento_id)
        elif acao == ac_cancelar:
            self.cancelar_agendamento(agendamento_id)

    def buscar_agendamento_por_id(self, agendamento_id):
        for a in (
            self.scheduler.listar_priorizados() +
            self.scheduler.listar_normais() +
            self.scheduler.listar_historico()
        ):
            if a.get("id") == agendamento_id:
                return a
        return None

            
    def on_novo_agendamento(self):
        self.setCentralWidget(CreateAgendamentoView(self.scheduler, self.back_to_main))

    def on_chamar_prio(self):
        item = self.scheduler.chamar_proximo_priorizado()
        
        if item:
            self.falar_chamada(item.get("paciente_id"), item.get("numero"))
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
           
    def on_detalhes(self, item):
        row = item.row()
        agendamento_id = self.table.item(row, 0).data(Qt.ItemDataRole.UserRole)

        ag = self.buscar_agendamento_por_id(agendamento_id)
 

        if not ag:
            return

        msg = QtWidgets.QMessageBox(self)
        msg.setObjectName("detailsBox")
        msg.setWindowTitle("Detalhes do Agendamento")
        msg.setText(f"""
            Paciente: {ag.get('paciente_id')}
            Ficha: {ag.get('numero')}
            Horário: {ag.get('horario')}
            Prioridade: {ag.get('prioridade')}
            Status: {ag.get('status')}
        """)
        msg.exec()
        
    def back_to_main(self):
        self._build_ui()
        
    def falar_chamada(self, nome_paciente, ficha=None):
        texto = f"Paciente {nome_paciente}, ficha número {ficha}. Favor dirigir-se ao atendimento."
        tts.speak(texto)
        
    def chamar_especifico(self, ag):
        if ag.get("status") != "agendado":
            QtWidgets.QMessageBox.warning(self, "Aviso", "Este agendamento já foi chamado.")
            return
        
        QtWidgets.QMessageBox.information(self, 'Chamando', f"Chamando: {ag['paciente_id']} - Nº {ag['numero']}")
        self.falar_chamada(ag["paciente_id"], ag["numero"])

        ag["status"] = "chamado"
        self.scheduler.repo.atualizar_agendamento(ag["id"], ag)
        self.atualizar_lista()
        
    def priorizar_agendamento(self, agendamento_id):
        if self.scheduler.priorizar_agendamento(agendamento_id):
            self.atualizar_lista()
            
    def cancelar_agendamento(self, agendamento_id):
        msg = QtWidgets.QMessageBox(self)
        msg.setObjectName("cancelBox")
        msg.setWindowTitle("Confirmar cancelamento")
        msg.setText("Deseja cancelar este agendamento?")
        msg.setStandardButtons(
            QtWidgets.QMessageBox.StandardButton.Yes |
            QtWidgets.QMessageBox.StandardButton.No
        )

        resp = msg.exec()

        if resp == QtWidgets.QMessageBox.StandardButton.Yes:
            self.scheduler.cancelar_agendamento(agendamento_id)
            self.atualizar_lista()


