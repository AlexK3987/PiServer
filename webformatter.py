import json
from collections import defaultdict

class WebFormatter:
    #formats sudoku json into html table for viewing
    box_size=40
    tbl="table { margin:1em auto; border-collapse: collapse;}"
    td= "td {height:"+str(box_size)+"px; width: "+str(box_size)+"px; border:.1px solid; text-align:center;}"
    tdf = "td:first-child { border-left:solid;}"
    tdn = "td:nth-child(3n){ border-right: solid;}"
    trf = "tr:first-child { border-top: solid;}"
    trn = "tr:nth-child(3n) td{ border-bottom:solid;}"
    @staticmethod

    def sudokuStyle():
        text="<style>"
        #table
        text+=WebFormatter.tbl
        text+=WebFormatter.td
        text+=WebFormatter.tdf
        text+=WebFormatter.tdn
        text+=WebFormatter.trf
        text+=WebFormatter.trn
        text+="</style>"
        return text
    

    @staticmethod
    def sudokuTable(json_in):
        data_dict= defaultdict(dict)
        data = json.loads(json_in);
        for square in data['squares']:
            data_dict[square['x']][square['y']]=square['value']
        text="<table>"
        for i in range(9):
            text+="<tr>"
            for j in range(9):
                text+="<td>"
                if i in data_dict and j in data_dict[i]:
                    text+=str(data_dict[i][j])
                text+="</td>"
            text+="</tr>"
        text+="</table>"
        return text


    @staticmethod
    def formatSudoku(s):
        style=WebFormatter.sudokuStyle()
        table=WebFormatter.sudokuTable(s)
        return style+table

    @staticmethod
    def formatSudokuJson(s):
        with open(s,"r") as f:
            data=f.read();
        style=WebFormatter.sudokuStyle()
        table=WebFormatter.sudokuTable(data)
        return style+table

