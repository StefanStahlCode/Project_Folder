import sys
import PySide6.QtWidgets as pq
from PySide6.QtGui import QAction, QIcon, QPixmap
import PySide6.QtCore as pc
from PySide6.QtCore import Qt
import numpy as  np
import matplotlib.pyplot as plt
import pandas as pd

class MainWindow(pq.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Graph Generator")
        self.setFixedSize(950, 600)
        self.table = pq.QTableView()
        self.model = None
        self.file_path = None
        self.df = None
        
        
        self.button = pq.QPushButton("Open File")
        self.button.clicked.connect(self.set_df)

        self.layout = pq.QGridLayout()

        self.layout.addWidget(self.button, 0, 0)
        self.layout.addWidget(self.table, 1, 1, 5, 5)

        #checkbox to change if the first column of the df is to be used as index
        self.checkbox = pq.QCheckBox("Use first column as index")
        self.checkbox.stateChanged.connect(self.index_change)
        self.layout.addWidget(self.checkbox)

        widget = pq.QWidget()
        widget.setLayout(self.layout)


        self.setCentralWidget(widget)

    def set_df(self, e):
        self.open_file(e)
        if self.df.columns[0].lower() == "id" or "index":
            self.checkbox.setCheckState(pc.Qt.CheckState.Checked)
            self.df = self.df.set_index(self.df.columns[0])

        self.model = TableModel(self.df)
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
            self.model = TableModel(self.df)
            self.table.setModel(self.model)
        else:
            #reread the file
            file = pd.read_csv(self.file_path[0])
            self.df = pd.DataFrame(file)
            self.model = TableModel(self.df)
            self.table.setModel(self.model)
        

#creating a class for a dataframe table widget
class TableModel(pc.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        #_data from parent class 
        self._data = data

    #the functions data, rowCount, columnCount and headerData are needed to be named this way from the parent class QAbstractTableModel
    #if more functionability is needed, then implement:
    # -setData() for being editable
    # -flags() to return a value containing ItemIsEditable
    # -insertRows() , removeRows() , insertColumns() , and removeColumns() to provide an interface for a resizebale data structure
    def data (self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)
        
    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]
    
    def headerData(self, section, orientation, role):
        if role == pc.Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])


    

        


def main():
    app = pq.QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()


if __name__ == "__main__":
    main()