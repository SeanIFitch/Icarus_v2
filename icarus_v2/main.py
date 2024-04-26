from ConfigurationManager import ConfigurationManager
from MainWindow import MainWindow
from DataHandler import DataHandler
from PySide6.QtWidgets import QApplication


# Application entry point
if __name__ == "__main__":
    config_manager = ConfigurationManager("settings.json")

    app = QApplication([])
    window = MainWindow(config_manager)
    window.show()

    data_handler = DataHandler(config_manager)
    window.set_device(data_handler)

    window.init_loader()

    app.exec()
