import sys
import traceback
from pathlib import Path
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMessageBox

from repositories.json_repository import JsonRepository
from services.scheduler_service import SchedulerService
from view.MainWindow import MainWindow


def global_exception_handler(exctype, value, tb):
    erro = "".join(traceback.format_exception(exctype, value, tb))

    # log no terminal (ou arquivo futuramente)
    print("Erro não tratado:")
    print(erro)

    # evita crash da aplicação
    app = QtWidgets.QApplication.instance()
    if app:
        QMessageBox.critical(
            None,
            "Erro inesperado",
            "Ocorreu um erro inesperado.\n\n"
            "A aplicação continuará em execução.\n\n"
            f"Detalhes técnicos:\n{value}"
        )


# registra o handler GLOBAL (antes do Qt iniciar)
sys.excepthook = global_exception_handler


def main():
    repo = JsonRepository('data/db.json')
    scheduler = SchedulerService(repo)

    app = QtWidgets.QApplication(sys.argv)

    base_path = Path(__file__).parent
    style_path = base_path / "styles.qss"

    if style_path.exists():
        with open(style_path, "r", encoding="utf-8") as style_file:
            app.setStyleSheet(style_file.read())
    else:
        print(f"Arquivo styles.qss NÃO encontrado em: {style_path}")

    win = MainWindow(scheduler)
    win.show()

    sys.exit(app.exec())

   
   
if __name__ == '__main__':
    main()
