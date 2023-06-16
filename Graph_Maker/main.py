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

        
        #self.check_button = pq.QPushButton("Select columns for Graph")
        #self.check_button.clicked.connect(self.open_check_window)
        #self.layout.addWidget(self.check_button, 0, 1)


        #combobox to select graph type
        self.combox = pq.QComboBox()
        #types of plots implemented here
        self.combox.addItems(["Line Plot", "Scatter Plot"])
        self.layout.addWidget(self.combox, 6, 1)

        #button to make graph
        self.button_graph_maker = pq.QPushButton("Make Graph")
        self.button_graph_maker.clicked.connect(self.make_graph)
        self.layout.addWidget(self.button_graph_maker, 0, 1)

        


        widget = pq.QWidget()
        widget.setLayout(self.layout)


        self.setCentralWidget(widget)


    #open file dialog and set dataframe. make model and show table in layout
    def set_df(self, e):
        self.open_file(e)
        #commented out because this triggers twice
        #if self.df.columns[0].lower() == "id" or "index":
        #    self.checkbox.setCheckState(pc.Qt.CheckState.Checked)
        #    self.df = self.df.set_index(self.df.columns[0])

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
    def open_check_window_line(self):
        self.check_window = gf.Check_Window(gf.graph_availability(self.df))
        self.check_window.show()
        #custom  Signal from class Check_Window
        self.check_window.window_close_Signal.connect(self.set_col_list)

    def open_check_window_scatter(self):
        pass
        

    #making the graph, list refers to the list of checked columns
    def make_graph(self):
        if self.combox.currentText() == "Line Plot":
            self.open_check_window_line()
        elif self.combox.currentText() == "Scatter Plot":
            self.open_check_window_scatter()
            
    #set column list and open window for additional graph data
    def set_col_list(self, liste):
        actual_list = []
        for i in range(len(liste)):
            if liste[i].value == 2:
                actual_list.append(self.df.columns[i])
        self.col_list = actual_list

        dia = gf.LineDialog(self)
        dia.window_close_Signal.connect(self.make_graph_line)
        dia.exec()
        
    #making a line graph
    def make_graph_line(self, liste):
        print(int(liste[2]))
        print(self.col_list)
        #liste: xlabel, yalabel, offset (offset default = 0), title
        fig, ax = plt.subplots(figsize=(16, 9))
        for col in self.col_list:
            ax.plot((self.df.index + int(liste[2])), self.df[col], label=col)
    
        ax.set_xlabel(liste[0])
        ax.set_ylabel(liste[1])
        ax.set_title(liste[3])
        ax.legend()
        if liste[4] == "":
            graph_name= "graph.jpg"
        else:
            graph_name = liste[4] + ".jpg"
        plt.savefig(graph_name, dpi=150)

        
    





    

        


def main():
    app = pq.QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()


if __name__ == "__main__":
    main()