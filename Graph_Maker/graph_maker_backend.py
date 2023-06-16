import sys
import PySide6.QtWidgets as pq
from PySide6.QtGui import QAction, QIcon, QPixmap
import PySide6.QtCore as pc
from PySide6.QtCore import Qt
import numpy as  np
import matplotlib.pyplot as plt
import pandas as pd


#custom global signal to trigger certain actions once the temp window appears and hides






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
            
#class containing a checkbox for every suited column
class Check_Window(pq.QWidget):
    #custom signal to transport list of checked states
    window_close_Signal = pc.Signal(list)
    def __init__(self, col_list):
        super().__init__()
        self.col_list = col_list
        self.setWindowTitle("Select Columns")

        layout = pq.QGridLayout()
        #list for checkboxes
        self.check_list = []
        #temp variables to keep track of grid
        #m = row,   n = column
        m = 0
        n = 0
        for i in range(len(self.col_list)):
            self.check_list.append(None)
            self.check_list[i] = pq.QCheckBox(col_list[i])
            layout.addWidget(self.check_list[i], m, n)
            m = m + 1
            if m == 16:
                m = 0
                n = n + 1
            if n == 11:
                print("Too many Columns to display, window closes")
                self.close()
            
        
        self.button_confirm = pq.QPushButton("Confirm Selection")
        self.button_confirm.clicked.connect(self.close_window)
        layout.addWidget(self.button_confirm)

        self.setLayout(layout)

        

    def test(self, list):
        print("test", list)

    #close the window and send signal with the checked_list
    def close_window(self, e):
        checked_list = []
        for i in self.check_list:
            checked_list.append(i.checkState())



        #print(checked_list)
        self.window_close_Signal.emit(checked_list)
        self.close()
        
        

        



#function to make list for a checkbox containing columns that can be used for a Graph
    #no complicated selection logic here, as every graph type would need its own logic
def graph_availability(df):
    #data types to check columns with, can be expanded if necessary 
    number_types = ["int64", "int32", "int16", "int8", "float", "float16", "float23", "float64"]
    #list to return names of columns
    ret_list = []
    for col in df.columns:
        if df.dtypes[col] in number_types:
            ret_list.append(col)

    return ret_list

class LineDialog(pq.QDialog):
    window_close_Signal = pc.Signal(list)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.info_list = []
        self.setWindowTitle("Dialog Window")

        
        button_box = pq.QDialogButtonBox.Ok | pq.QDialogButtonBox.Cancel


        self.buttonBox = pq.QDialogButtonBox(button_box)
        #connecting accepetd and rejected methods to buttons ok and cancel
        self.buttonBox.accepted.connect(self.pressed_ok)
        self.buttonBox.rejected.connect(self.reject)
        
        self.layout = pq.QGridLayout()

        message = pq.QLabel("Please give more info for the Graph")

        #info needed: xlabel, yalabel, x-axis, titele
        self.xlabel = pq.QLineEdit()
        self.ylabel = pq.QLineEdit()
        self.combox = pq.QComboBox()
        self.combox.addItems(["Use Index as x x-axis", "Use index with Offset as x-axis"])
        self.combox.currentIndexChanged.connect(self.offset_enable)
        self.offset = pq.QLineEdit()
        self.offset.setEnabled(False)
        self.title = pq.QLineEdit()
        self.file_name = pq.QLineEdit()
        

        self.xlabel.setPlaceholderText("Insert x label")
        self.ylabel.setPlaceholderText("Insert y label")
        self.offset.setPlaceholderText("Set offset for index")
        self.title.setPlaceholderText("Set graph title")
        self.file_name.setPlaceholderText("Graph")

        self.layout.addWidget(self.xlabel, 1, 0)
        self.layout.addWidget(self.ylabel, 2, 0)
        self.layout.addWidget(self.combox, 3, 0)
        self.layout.addWidget(self.offset, 3, 1)
        self.layout.addWidget(self.title, 4, 0)
        self.layout.addWidget(self.file_name, 5, 0)
        self.layout.addWidget(message, 0, 0)
        self.layout.addWidget(self.buttonBox, 6, 0)
        self.setLayout(self.layout)
    
    def pressed_ok(self):
        self.info_list.append(self.xlabel.text())
        self.info_list.append(self.ylabel.text())
        #self.info_list.append(self.combox.currentIndex())
        try:
            self.info_list.append(int(self.offset.text()))
        except ValueError:
            print("Offset needs to be a integer, set to 0")
            self.info_list.append(0)

        self.info_list.append(self.title.text())
        self.info_list.append(self.file_name.text())
        self.window_close_Signal.emit(self.info_list)
        self.close()

    def offset_enable(self, id):
        if id == 0:
            self.offset.setEnabled(False)
        else:
            self.offset.setEnabled(True)


