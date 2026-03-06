import sys
from ui.main_window import MainWindow


def main():

    # file passed by OS drag-drop onto exe
    dropped_file = None

    if len(sys.argv) > 1:
        dropped_file = sys.argv[1]

    app = MainWindow(startup_file=dropped_file)
    app.run()


if __name__ == "__main__":
    main()
