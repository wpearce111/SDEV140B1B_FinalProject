"""
    Title: PearceWyattFinalProject - item.py
    Author: Wyatt Henry Pearce
    Date: 10/08/2023 (MM/DD/YYYY)
    
    Description of File:
    This file contains the code defining the item class.
"""

# Creating the Item object
class Item:
    def __init__(self, name, date, status):
        self.name = name
        self.date = date
        self.status = status

    # Accessor methods to getting, name, date, and status
    def getName(self):
        return self.name
    
    def getDate(self):
        return self.date
    
    def getStatus(self):
        return self.status
    
    # Mutator methods for mutating, name, date, and status
    def setName(self, newName):
        self.name = newName
    
    def setDate(self, newDate):
        self.date = newDate

    def setStatus(self, newStatus):
        self.status = newStatus