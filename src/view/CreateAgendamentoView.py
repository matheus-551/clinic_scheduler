from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QComboBox, QTextEdit,
    QGroupBox, QPushButton, QMessageBox, QHBoxLayout, QApplication
)
from PyQt6.QtGui import QIcon, QCursor
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QRect
from PyQt6.QtWidgets import QDateEdit, QTimeEdit
from PyQt6.QtCore import QDate, QTime

from models.agendamento import Prioridade

class MaskedLineEdit(QLineEdit):
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.setCursorPosition(0)

class CreateAgendamentoView(QWidget):
    def __init__(self, scheduler_service, go_back_callback):
        super().__init__()
        self.scheduler = scheduler_service
        self.go_back = go_back_callback

        self.setWindowTitle("Criar Agendamento")

        self.create_group_box_patient()
        self.create_group_box_appointment()
        self.create_box_buttons()
        self.build_ui()

    # -----------------------------------------
    def build_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 10, 15, 10)

        layout.addWidget(self.group_patient)
        layout.addWidget(self.group_appointment)
        layout.addLayout(self.container_buttons)
        
        self.setLayout(layout)

    def create_group_box_patient(self):
        self.group_patient = QGroupBox("Dados do Paciente")
        form = QFormLayout()

        self.name_input = QLineEdit()
        self.name_input.setProperty("formInput", True)

        self.dataNascimento_input = QLineEdit()
        self.dataNascimento_input.setPlaceholderText("DD/MM/AAAA")
        self.dataNascimento_input.setProperty("formInput", True)

        self.documento_input = MaskedLineEdit()
        self.documento_input.setInputMask("000.000.000-00")
        self.documento_input.setPlaceholderText("CPF")
        self.documento_input.setProperty("formInput", True)

        self.telefone_input = MaskedLineEdit()
        self.telefone_input.setInputMask("(00) 00000-0000")
        self.telefone_input.setPlaceholderText("Telefone")
        self.telefone_input.setProperty("formInput", True)

        form.addRow("Nome:", self.name_input)
        form.addRow("Data de Nascimento:", self.dataNascimento_input)
        form.addRow("CPF:", self.documento_input)
        form.addRow("Telefone:", self.telefone_input)

        self.group_patient.setLayout(form)
        
    # -----------------------------------------
    def create_group_box_appointment(self):
        self.group_appointment = QGroupBox("Dados do Agendamento")
        form = QFormLayout()

        self.prioridade_dropdown = QComboBox()
        self.prioridade_dropdown.setProperty("formInput", True)

        for prioridade in Prioridade:
            self.prioridade_dropdown.addItem(prioridade.name.capitalize(), prioridade)

        self.data_input = QDateEdit()
        self.data_input.setCalendarPopup(True)
        self.data_input.setDate(QDate.currentDate())
        self.data_input.setDisplayFormat("dd/MM/yyyy")
        self.data_input.setProperty("formInput", True)

        self.hora_dropdown = QComboBox()
        self.hora_dropdown.setProperty("formInput", True)
        
        self.data_input.setFixedWidth(140)
        self.hora_dropdown.setFixedWidth(90)

        for h in range(0, 24):
            for m in (0, 30):
                self.hora_dropdown.addItem(f"{h:02d}:{m:02d}")

        self.motivo_input = QLineEdit()
        self.motivo_input.setProperty("formInput", True)
        self.motivo_input.setProperty("asTextarea", True)

        # comportamento visual
        self.motivo_input.setFixedHeight(90)
        self.motivo_input.setAlignment(Qt.AlignmentFlag.AlignTop)
        form.addRow("Prioridade:", self.prioridade_dropdown)

        layout_data_hora = QHBoxLayout()
        layout_data_hora.setSpacing(8)
        layout_data_hora.setContentsMargins(0, 0, 0, 0)
        layout_data_hora.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.data_input.setFixedWidth(140)
        self.hora_dropdown.setFixedWidth(90)

        layout_data_hora.addWidget(self.data_input)
        layout_data_hora.addWidget(QLabel("Hora:"))
        layout_data_hora.addWidget(self.hora_dropdown)

        form.addRow("Data:", layout_data_hora)
        form.addRow("Motivo:", self.motivo_input)

        self.group_appointment.setLayout(form)

    def create_box_buttons(self):
        self.container_buttons = QHBoxLayout()

        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setIcon(QIcon("icons/cancel.png"))
        btn_cancelar.clicked.connect(self.go_back)
        btn_cancelar.setObjectName("btnDanger")
        btn_cancelar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    
        btn_salvar = QPushButton("Salvar Agendamento")
        btn_salvar.setIcon(QIcon("icons/save.png"))
        btn_salvar.clicked.connect(self.salvar_agendamento)
        btn_salvar.setObjectName("btnSuccess")  
        btn_salvar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        self.container_buttons.addWidget(btn_cancelar)
        self.container_buttons.addWidget(btn_salvar)

    def show_messagebox(self, message, type="info"):
        msg = QMessageBox(self)

        msg.setStyleSheet("""
            QMessageBox {
                color: #000;
                font-size: 14px;
            }
            QLabel {
                color: #000;
                padding: 10px;
            }
            QPushButton {
                color: #000;
                border: 1px solid;
                border-radius: 6px;
                padding: 6px 14px;
                min-width: 80px;
            }
            
            QPushButton:hover {
                background: #BFD5F8;
            }
        """)

        match type:
            case "info":
                msg.setWindowTitle("Informação")
                msg.setIcon(QMessageBox.Icon.Information)

            case "warning":
                msg.setWindowTitle("Atenção")
                msg.setIcon(QMessageBox.Icon.Warning)

            case "error":
                msg.setWindowTitle("Erro")
                msg.setIcon(QMessageBox.Icon.Critical)

        msg.setText(message)
        msg.exec()
    
    def salvar_agendamento(self):
        try:
            nome = self.name_input.text().strip()
            data = self.data_input.date().toString("yyyy-MM-dd")
            hora = self.hora_dropdown.currentText()
            motivo = self.motivo_input.text().strip()

            prioridade_enum = self.prioridade_dropdown.currentData()

            if nome == "" or data == "" or hora == "":
                self.show_messagebox("Preencha todos os campos obrigatórios!", type="error")
                return

            horario = f"{data}T{hora}:00"
            paciente_id = nome

            self.scheduler.criar_agendamento(
                paciente_id=paciente_id,
                horario=horario,
                motivo=motivo if motivo else None,
                prioridade=prioridade_enum
            )

            self.go_back()

        except Exception as e:
            print(e)
            self.show_messagebox(f"Erro ao salvar agendamento: {e}", type="error")
