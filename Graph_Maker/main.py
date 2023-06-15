import sys
import PySide6.QtWidgets as pq
from PySide6.QtGui import QAction, QIcon, QPixmap
import PySide6.QtCore as pc
from PySide6.QtCore import Qt
import numpy as  np
import matplotlib.pyplot as plt
import pandas as pd
import graph_maker_backend as gf




class MainWindow(pq.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Graph Generator")
        self.setFixedSize(950, 600)
        self.table = pq.QTableView()
        self.model = None
        self.file_path = None
        self.df = None
        self.check_window = None
        self.col_list = None
        
        #Open file button
        self.button = pq.QPushButton("Open File")
        self.button.clicked.connect(self.set_df)

        self.layout = pq.QGridLayout()

        self.layout.addWidget(self.button, 0, 0)
        self.layout.addWidget(self.table, 1, 0, 5, 5)

        #checkbox to change if the first column of the df is to be used as index
        self.checkbox = pq.QCheckBox("Use first column as index")
        self.checkbox.stateChanged.connect(self.index_change)
        self.layout.addWidget(self.checkbox, 6, 0)

        self.check_button = pq.QPushButton("Select columns for Graph")
        self.check_button.clicked.connect(self.open_check_window)
        self.layout.addWidget(self.check_button, 0, 1)


        #combobox to select graph type
        self.combox = pq.QComboBox()
        #types of plots implemented here
        self.combox.addItems(["Line Plot", "Scatter Plot", "Bar Plot", "Step Plot"])
        self.layout.addWidget(self.combox, 6, 1)

        #button to make graph
        self.button_graph_maker = pq.QPushButton("Make Graph")
        self.button_graph_maker.clicked.connect(self.make_graph)
        self.layout.addWidget(self.button_graph_maker, 0, 2)

        


        widget = pq.QWidget()
        widget.setLayout(self.layout)


        self.setCentralWidget(widget)


    #open file dialog and set dataframe. make model and show table in layout
    def set_df(self, e):
        self.open_file(e)
        if self.df.columns[0].lower() == "id" or "index":
            self.checkbox.setCheckState(pc.Qt.CheckState.Checked)
            self.df = self.df.set_index(self.df.columns[0])

        self.model = gf.TableModel(self.df)
        self.table.setModel(self.model)


    def  open_file(self, e):
        self.file_path = pq.QFileDialog.getOpenFileName(None, "Load File", "", "(*.csv)")
    
        file = pd.read_csv(self.file_path[0])

        self.df = pd.DataFrame(file)
        
    #function to redo the df and tableModel to use or not use the first column as index
    def index_change(self, state):
        if state == pc.Qt.CheckState.Checked.value:
            #file = pd.read_csv(self.file_path[0])
            #self.df = pd.DataFrame(file)
            self.df = self.df.set_index(self.df.columns[0])
            self.model = gf.TableModel(self.df)
            self.table.setModel(self.model)
        else:
            #reread the file
            file = pd.read_csv(self.file_path[0])
            self.df = pd.DataFrame(file)
            self.model = gf.TableModel(self.df)
            self.table.setModel(self.model)

    #opens second window with checkboxes
    def open_check_window(self, e):
        self.check_window = gf.Check_Window(gf.graph_availability(self.df))
        self.check_window.show()
        #custom  Signal from class Check_Window
        self.check_window.window_close_Signal.connect(self.set_col_list)

    #making the graph, list refers to the list of checked clomuns
    def make_graph(self, liste):
        for i in range(len(liste)):
            if liste[i].value == pc.Qt.CheckState.Checked.value:
                print(self.df.columns[i])
    
    def set_col_list(self, liste):
        self.col_list = liste





    

        


def main():
    app = pq.QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()


if __name__ == "__main__":
    main()