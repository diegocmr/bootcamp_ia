
import sys

class CatchError:

    def __init__(self,e):      
        raise Exception(e.message)
