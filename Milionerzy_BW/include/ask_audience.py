from PyQt5.QtWidgets import QMainWindow
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


matplotlib.use('Qt5Agg')


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class AskAudienceWindow(QMainWindow):
    def __init__(self, window_title, *args, **kwargs):
        super(AskAudienceWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle(window_title)

    def show_bar_graph(self, votes_for_a: int, votes_for_b: int, votes_for_c: int, votes_for_d: int):
        x = ["A", "B", "C", "D"]
        y = [votes_for_a, votes_for_b, votes_for_c, votes_for_d]
        sc = MplCanvas(self, width=5, height=4, dpi=100)
        sc.axes.bar(x, y, color='b')
        sc.axes.grid(axis='y')
        self.setCentralWidget(sc)
        self.show()

