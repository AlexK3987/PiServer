from flask import Flask
from flask import request
from urllib.request import urlopen
import os

from webformatter import WebFormatter

curdir = '~/webapp'

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

    #store puzzle
    with open("curpuzz.json", 'wb') as f:
        f.write(text)

    #run c++ puzzle solver on curpuzz.json
    #os.system("solvepuzz "+curdir+"/curpuzz.json");
    
    #return formatted puzzle
    return WebFormatter.formatSudoku("curpuzz.json")

@app.route('/sudoku/solution')
def sudoku_soln():
    #display puzzle solver's solution
    return "SOLUTION:"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
