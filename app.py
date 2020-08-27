from flask import Flask
from flask import request
from urllib.request import urlopen
import os
from os import path

from datetime import datetime

from webformatter import WebFormatter
from sudokusolver import SudokuSolver

curdir = '~/webapp'
dev_port = 5001
soln_file="curpuzzsoln.json"
puzz_file="curpuzz.json"


proddir = "~/prodwebapp"
prod_port = 5000

app = Flask(__name__)

@app.route('/')#base
def index():
    return 'Hello world'

#Sudoku aplication: gets a new puzzle and displays on webpage
#use this api?  http://cs.utep.edu/cheon/ws/sudoku/new/?size=9&level=3
#cache problem json
#run solver and cache answer json

@app.route('/sudoku')
def sudoku():
    #get a new puzzle from the api
    
    with urlopen('http://cs.utep.edu/cheon/ws/sudoku/new/?size=9&level=3') as r:
        text=r.read() 
    
    
    #cache curpuzz.json if it exists arady
    """
    if path.exists("curpuzz.json"):
        with open("curpuzz.json","r"): as cur:
            with open("archive/"+datetime.now(),'wb') as archive:
                archive.write(cur.read)
    """

            

    #store puzzle
    with open(puzz_file, 'wb') as f:
        f.write(text)

    #run puzzle solver on curpuzz.json
    #writes solution to curpuzzsoln.json
    #os.system("./sudokusolver "+puzzfile);
    solver = SudokuSolver(text) 
    if solver.solve():
        solver.saveSoln(soln_file)
    
    
    #return formatted puzzle
    return WebFormatter.formatSudoku(text)

@app.route('/sudoku/solution')
def sudoku_soln():
    #display puzzle solver's solution
    #reads solution from curpuzzsoln.json
    
    return WebFormatter.formatSudokuJson(soln_file);

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port = dev_port)
