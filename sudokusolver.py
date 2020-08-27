import json
import copy
from collections import defaultdict

class SudokuSolver:
    def __init__(self,json_in):
        self.data_dict = defaultdict(dict)
        self.soln = defaultdict(dict)
        self.json_in=json_in
        self.dep_index=self.getAllDeps()
        data = json.loads(json_in);
        for square in data['squares']:
            self.data_dict[square['x']][square['y']]=square['value']
    
    #csp algo?
    def solve(self):
        #solve puzzle
        return self.solveSoduku(self.data_dict,self.getAllValid(self.data_dict))


    def saveSoln(self,name):
        out = self.convert(self.soln)
        with open(name,'w') as f:
            json.dump(out,f)

    def convert(self,to_convert):
        squares=[]
        for i in range(9):
            for j in range(9):
                obj = {}
                obj['x']=i
                obj['y']=j
                obj['value'] = to_convert[i][j]
                squares.append(obj)
        out={}
        out['squares']=squares
        return out



    def solveSoduku(self,grid, valid_entries):
        #base case: no more valid entries to fill out
        #print(valid_entries)
        if len(valid_entries)==0:
            self.soln=grid
            return True
        #find most constrained value 
        min_ls = list(range(1,10))
        min_loc = (-1,-1)
        for entry in valid_entries:
            loc = entry['loc']#tuple of i,j
            ls = entry['ls']#list of possible values at location loc
            if len(ls)==0:
                return False
            if len(ls)<len(min_ls):
                min_ls=ls
                min_loc=loc



        #chose the smallest ls
        #if empty return false
        #this means there is a box with no valid vals
        #iterate through the most constrained box
        for val in min_ls:
            #update value with this value
            new_grid = copy.deepcopy(grid)
            new_valid_entries=copy.deepcopy(valid_entries)


            new_grid[min_loc[0]][min_loc[1]]=val
            new_valid_entries= self.updateValid(new_valid_entries,min_loc,val)
            """
            n_valid_entries=self.getAllValid(new_grid)

            if new_valid_entries!=n_valid_entries:
                print("WTAF")
                print(new_valid_entries)
                print(n_valid_entries)
            print("COOLLL")
            """
            #if a recursive step reached the solution return true
            if self.solveSoduku(new_grid,new_valid_entries):
                return True
        return False
            



    #returns list of all possible values at each location
    #should only be called once
    #iterates through all non-filled entries
    def getAllValid(self,grid):
        valid_entries=list()
        for i in range(9):
            for j in range(9):
                if not j in grid[i]:
                    valid_entries.append(self.getValid(grid,i,j)) 
        return valid_entries       

    #returns object loc: i,j and ls: list of possible vals
    def getValid(self,grid, i, j):
        posvals= list(range(1,10))
        for x,y in self.dep_index[i][j]:
            try:
                cur_val = grid[x][y]
                posvals.remove(cur_val)
            except:
                pass
        return {'loc':(i,j),'ls':posvals}
                
    @staticmethod
    def closestBox(i):
        if i/3 < 1:#0,1,2 -> range(0,3)
           return range(3)
        if i/3 <2:#3,4,5 -> range(3,6)
            return range(3,6)
        return range(6,9)#6,7,8


    def updateValid(self,valid_vals, loc, val):
        dep_index=self.dep_index[loc[0]][loc[1]]
        new_vals = list()
        for elem in valid_vals:
            cur_loc=elem['loc']
            if cur_loc != loc:#remove this location from values 
                e=copy.deepcopy(elem)
                if cur_loc in dep_index:
                    try:
                        e['ls'].remove(val)
                    except:
                        pass
                new_vals.append(e)
        
        return new_vals


    #caching all of the dependent indicies
    def getAllDeps(self):
        out = defaultdict(dict)
        for i in range(9):
            for j in range(9):
                out[i][j]=self.getDependentIndex((i,j))
        return out


    def getDependentIndex(self,loc):
        i=loc[0]
        j=loc[1]
        locs = set()
        #rows and cols
        for x in range(9):
            if (i,x)!=loc:
                locs.add((i,x))
            if (x,j)!=loc:
                locs.add((x,j))
            
        for x in SudokuSolver.closestBox(i): 
            for y in SudokuSolver.closestBox(j):
                if (x,y) != loc:
                    locs.add((x,y))
        return locs

    
