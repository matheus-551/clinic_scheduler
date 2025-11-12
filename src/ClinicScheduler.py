import sys
from pathlib import Path
from PyQt6 import QtWidgets

from repositories.json_repository import JsonRepository
from services.scheduler_service import SchedulerService
from view.MainWindow import MainWindow

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