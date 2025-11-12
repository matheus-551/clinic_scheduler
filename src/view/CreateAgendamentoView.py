from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QComboBox, QTextEdit,
    QGroupBox, QPushButton, QMessageBox, QHBoxLayout, QApplication
)
from PyQt6.QtGui import QIcon, QCursor
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QRect
from models.agendamento import Prioridade


class Toast(QWidget):
    def __init__(self, message, success=True):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # color = "#4CAF50" if success else "#FF4C4C"

        # self.setStyleSheet(f"""
        #     background-color: {color};
        #     color: white;
        #     padding: 10px;
        #     border-radius: 10px;
        #     font-size: 14px;
        # """)

        self.label = QLabel(message, self)
        self.adjustSize()

        screen = QApplication.primaryScreen().availableGeometry()
        self.move(screen.width() - self.width() - 20, screen.height() - self.height() - 50)

        # Fade animation and auto close
        QTimer.singleShot(2000, self.close)


class CreateAgendamentoView(QWidget):
    def __init__(self, scheduler_service, go_back_callback):
        super().__init__()
        self.scheduler = scheduler_service
        self.go_back = go_back_callback

        self.setWindowTitle("Criar Agendamento")
        self.setFixedSize(650, 500)

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

    # -----------------------------------------
    def create_group_box_patient(self):
        self.group_patient = QGroupBox("Dados do Paciente")
        form = QFormLayout()

        self.name_input = QLineEdit()
        self.dataNascimento_input = QLineEdit()
        self.documento_input = QLineEdit()
        self.telefone_input = QLineEdit()

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
        for prioridade in Prioridade:
            self.prioridade_dropdown.addItem(prioridade.name.capitalize(), prioridade)

        self.data_input = QLineEdit()
        self.hora_input = QLineEdit()
        self.motivo_input = QTextEdit()
        self.motivo_input.setFixedHeight(70)

        form.addRow("Prioridade:", self.prioridade_dropdown)

        # Data + Hora na mesma linha
        layout_data_hora = QHBoxLayout()
        layout_data_hora.addWidget(self.data_input)
        layout_data_hora.addWidget(QLabel("Hora:"))
        layout_data_hora.addWidget(self.hora_input)

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

    # -----------------------------------------
    def salvar_agendamento(self):
        try:
            nome = self.name_input.text().strip()
            data = self.data_input.text().strip()
            hora = self.hora_input.text().strip()
            motivo = self.motivo_input.toPlainText().strip()
            prioridade_enum = self.prioridade_dropdown.currentData()

            if nome == "" or data == "" or hora == "":
                Toast("Preencha todos os campos obrigatórios!", success=False).show()
                return

            self.scheduler.criar_agendamento(
                nome=nome,
                data=data,
                hora=hora,
                motivo=motivo,
                prioridade=prioridade_enum.value
            )

            Toast("Agendamento salvo com sucesso! ✅", success=True).show()
            self.go_back()

        except Exception as e:
            Toast(f"Erro ao salvar: {e}", success=False).show()

