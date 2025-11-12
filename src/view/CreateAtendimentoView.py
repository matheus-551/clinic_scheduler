from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox


class CreateAtendimentoView(QWidget):
    
    def __init__(self, scheduler_service, go_back_callback):
        super().__init__()
        self.scheduler = scheduler_service
        self.go_back = go_back_callback
        self.setWindowTitle("Criar Atendimento Sem Agendamento")

        layout = QVBoxLayout()

        self.nome_input = QLineEdit()
        self.nome_input.setPlaceholderText("Nome do paciente")

        self.tipo_input = QLineEdit()
        self.tipo_input.setPlaceholderText("Tipo (recepção / consultório)")

        btn_salvar = QPushButton("Gerar Ficha e Criar Atendimento")
        btn_salvar.clicked.connect(self.gerar_atendimento)

        layout.addWidget(QLabel("Nome do Paciente:"))
        layout.addWidget(self.nome_input)
        layout.addWidget(QLabel("Tipo do Atendimento:"))
        layout.addWidget(self.tipo_input)
        layout.addWidget(btn_salvar)

        self.setLayout(layout)


    def gerar_atendimento(self):
        nome = self.nome_input.text()
        tipo = self.tipo_input.text().lower()


        if nome == "" or tipo == "":
            QMessageBox.warning(self, "Erro", "Preencha todos os campos.")
            return


        ficha = self.scheduler.criar_atendimento_sem_agendamento(nome, tipo)
        QMessageBox.information(self, "Ficha Gerada", f"Ficha nº {ficha} criada com sucesso!")
        self.go_back()