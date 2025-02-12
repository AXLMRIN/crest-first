import json

class FigureParameters : 
    def __init__(self, filename : str) : 
        with open(filename, "r") as file :
            self.data = json.load(file)
    
    def __getitem__(self, key) : return self.data[key]