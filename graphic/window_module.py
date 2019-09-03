import tkinter

def createColumnNameLabel(tk : tkinter.Tk, columnNames : list):
    col = 0
    for name in columnNames:
        yield tkinter.Entry(tk, textvariable = tkinter.StringVar(tk, name[0])).grid(row = 0, column = col)
        col += 1

def createRowLabel(tk : tkinter.Tk, rows : list):
    colMax = len(rows[0])
    row_index = 0
    for row in rows:
        col_index = 0
        for col in row:
            yield tkinter.Entry(tk, textvariable = tkinter.StringVar(tk, str(col))).grid(row = 1 + row_index, column = col_index)
            col_index += 1
        row_index += 1


class TableWindow:
    """"""
    def __init__(self, columnNames : list, rows, title = "TableWindow"):
        self.tk = tkinter.Tk(title)
        self.tk.title(title)
        self.columnNames = columnNames
        self.columnNamesWidget = list(createColumnNameLabel(self.tk, columnNames))

        self.rows = rows
        self.rowsWidget = list(createRowLabel(self.tk, rows))

    def mainloop(self):
        self.tk.mainloop()
    
    def __del__(self):
        self.tk.destroy()