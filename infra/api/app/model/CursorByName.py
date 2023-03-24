import sys
class CursorByName():
    def __init__(self, cursor):
        self._cursor = cursor
        self.row = True
    
    def __iter__(self):    
        return self

    def __next__(self):       
        self.row = self._cursor.fetchone()
     
        if self.row == None:
            raise StopIteration            
       
        return { description[0]: self.row[col] for col, description in enumerate(self._cursor.description) }
    def one(self):       
        self.row = self._cursor.fetchone()
     
        if self.row == None:
            return False           
       
        return { description[0]: self.row[col] for col, description in enumerate(self._cursor.description) }