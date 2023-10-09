"""
    Title: PearceWyattFinalProject - TimeForge (A To-Do List Manager application)
    Author: Wyatt Henry Pearce
    Date: 10/08/2023 (MM/DD/YYYY)

    Description of File:
    The primary file for running the program TimefForge.
    The purpose of TimeForge is to assist users in creating, 
    managing, and organizing their tasks and to-do lists efficiently.
"""

from breezypythongui import EasyFrame # Lambert's shell
from item import Item                 # Import Item class for itemList
import re                             # Import regular expressions for validating the date input field
from tkinter import PhotoImage        # Import class for image display
import os                             # Import os for getting the files lastModified value for footer label
from datetime import datetime         # Import dateTime for lastModified footer label

# Global list of item objects
itemList = []

# Creating the primary class of the program
class TimeForge(EasyFrame):
    # Program Constructor that sets the initial state
    def __init__(self):
        EasyFrame.__init__(self, width=500, height=350, title="TimeForge v1.0 - To Do List Manager")  # Create the window
        self.setResizable(False)                                                                      # Disable window resizing
        
        # Index of the most recently selected item (used throughout the program)
        self.selectedItemIndex = 0

        # Initialize images used for each item property label
        self.indexImage = PhotoImage(file="Images/indexImage.png")
        self.nameImage = PhotoImage(file="Images/nameImage.png")
        self.dateImage = PhotoImage(file="Images/dateImage.png")
        self.statusImage = PhotoImage(file="Images/statusImage.png")

        # Partition the program into four panels
        self.panel1 = self.addPanel(row=0, column=0)                      # Panel for the list
        self.panel2 = self.addPanel(row=6, column=0)                      # Panel for information labels
        self.panel3 = self.addPanel(row=7, column=0)                      # Panel for command buttons
        self.panel4 = self.addPanel(row=9, column=0, background="grey90") # Panel for program footer

        # Set up a listBox to display all items within the itemList[] variable visually
        self.listBox = self.panel1.addListbox(row=0, column=0, rowspan=10, listItemSelected=self.selectItem)

        # Add labels for the index, name, date, and completion status of item selected
        # These will be overlayed with images, but still have text attributes defined
        # If the images cannot be loaded, This functions as alternate text
        self.indexLabel = self.panel2.addLabel(text="Index", row=0, column=0)
        self.nameLabel = self.panel2.addLabel(text="Name", row=1, column=0)
        self.dateLabel = self.panel2.addLabel(text="Due-Date", row=2, column=0)
        self.statusLabel = self.panel2.addLabel(text="Status", row=3, column=0)

        # Add images to labels (to fullfill project requirements, otherwise images are not needed)
        # This is technically four images, which fullfills project requirements
        self.indexLabel["image"]=self.indexImage
        self.nameLabel["image"]=self.nameImage
        self.dateLabel["image"]=self.dateImage
        self.statusLabel["image"]=self.statusImage

        # Add display fields for index, name, date, and completion status of item selected
        self.indexField = self.panel2.addIntegerField(value=None, row=0, column=1, width=30, state="readonly")
        self.nameField = self.panel2.addTextField(text=None, row=1, column=1, width=30)
        self.dateField = self.panel2.addTextField(text=None, row=2, column=1, width=30)
        self.statusField = self.panel2.addTextField(text=None, row=3, column=1, width=30, state="readonly")

        # Add command buttons for adding, removing, and editing items on the list
        self.addItemButton = self.panel3.addButton(text="Add Item", row=0, column=0, command=lambda: self.addItemToList(len(itemList), Item("Default Task", "00/00/0000", "Not Complete")))
        self.removeItemButton = self.panel3.addButton(text="Remove Item", row=0, column=1, state="disabled", command=lambda: self.removeItemFromList(self.selectedItemIndex))
        self.statusItemButton = self.panel3.addButton(text="Change Status", row=0, column=2, state="disabled", command=lambda: self.changeItemStatus(self.selectedItemIndex))
        self.saveItemButton = self.panel3.addButton(text="Save", row=0, column=3, state="disabled", command=self.saveChanges)
        self.moveUpButton = self.panel3.addButton(text="Move Up", row=1, column=0, state="disabled", command=lambda: self.moveItem(self.selectedItemIndex, "up"))
        self.moveDownButton = self.panel3.addButton(text="Move Down", row=1, column=1, state="disabled", command=lambda: self.moveItem(self.selectedItemIndex, "down"))

        # Footer labels
        self.footer1 = self.panel4.addLabel(text="Created by:", row=0, column=0, background="grey90")
        self.footer2 = self.panel4.addLabel(text="Wyatt H. Pearce", row=0, column=1, background="grey90")
        self.footer4 = self.panel4.addLabel(text="Version: 1.0", row=0, column=2, background="grey90")
        # LastUpdated footer label
        timeStamp = os.path.getmtime(os.path.basename(os.path.abspath(__file__)))                                          # Get the file's modification timestamp
        lastUpdatedDate = datetime.fromtimestamp(timeStamp).strftime("%m/%d/%Y")                                           # Convert the timestamp to a human-readable date format
        self.footer3 = self.panel4.addLabel(text=f"Last Updated: {lastUpdatedDate}", row=0, column=3, background="grey90") # Displays the currentDate variable

        # Updates item display to match itemList[] (I do this once at the begining because data might have been loaded in)
        self.syncLists()

    # This method is called when an item on the listBox item display is selected
    def selectItem(self, index):
        self.selectedItemIndex = index # Update selectedItemIndex to the selectedItem

        # Update all display fields to display the properties of the currently selected item
        self.indexField.setValue(self.selectedItemIndex)
        self.nameField.setText(itemList[self.selectedItemIndex].name)
        self.dateField.setText(itemList[self.selectedItemIndex].date)
        self.statusField.setText(itemList[self.selectedItemIndex].status)

        # Enable mutator buttons now that an item is selected and ready to be edited
        self.moveUpButton["state"] = "normal"
        self.moveDownButton["state"] = "normal"
        self.saveItemButton["state"] = "normal"
        self.removeItemButton["state"] = "normal"
        self.statusItemButton["state"] = "normal"

    # This method adds an item instance to itemList[] at a givin index
    def addItemToList(self, index, item):
        itemList.insert(index, item) # Add the givin item to the itemList[]
        self.selectItem(index)       # Set the most recently added item to be the currently selected item
        self.syncLists()             # Update listBox display to match the items in itemList[]

    # This method removes an item from itemList[] at a givin index
    def removeItemFromList(self, index):
        # Remove currently selected item from itemList[]
        itemList.pop(index) 
        self.syncLists() # Update listBox display to match the items in itemList[]

        # Clear all display fields since the item selected has been removed
        self.indexField.setValue(None)
        self.nameField.setText(None)
        self.dateField.setText(None)
        self.statusField.setText(None)

        # Disable mutator buttons since the currently selected item has been deleted (there is nothing for them to edit)
        self.saveItemButton["state"] = "disabled"
        self.removeItemButton["state"] = "disabled"
        self.statusItemButton["state"] = "disabled"
        self.moveUpButton["state"] = "disabled"
        self.moveDownButton["state"] = "disabled"

    # This method changes the completion status of an item at the givin index
    def changeItemStatus(self, index):
        if itemList[index].getStatus() == "Not Complete": # Toggle items completion status
            itemList[index].setStatus("Complete")         # Set it to complete
            self.syncLists()                              # Update the listBox item display to match itemList[]
            self.statusField.setText("Complete")          # # Update the statusField right away so the user gets visual feedback
        else:                                             # Toggle items completion status
            itemList[index].setStatus("Not Complete")
            self.syncLists()
            self.statusField.setText("Not Complete")

    # This method swaps the item at a givin index with the item directly above or below that index
    def moveItem(self, index, direction):
        if direction == "up" and index > 0:
            # Swap the items
            tempItem = itemList[index]
            itemList[index] = itemList[index - 1]
            itemList[index - 1] = tempItem

            self.selectedItemIndex -= 1             # Update the currently selected item index
            self.selectItem(self.selectedItemIndex) # Re-select the current item so the display fields stay updated
        elif direction == "down" and index < len(itemList) - 1:
            # Swap the items
            tempItem = itemList[index]
            itemList[index] = itemList[index + 1]
            itemList[index + 1] = tempItem

            self.selectedItemIndex += 1             # Update the currently selected item index
            self.selectItem(self.selectedItemIndex) # Re-select the current item so the display fields stay updated
        self.syncLists()

    # This method validates input/display field values and pushes that data to itemList[]
    # If the data is not valid, an error message box is displayed
    def saveChanges(self):
        # Get the name and date values from input fields
        name_text = self.nameField.getText()
        date_text = self.dateField.getText()

        # Check name length
        if len(name_text) > 30 or len(name_text) < 1:
            # Display a error box because name was not valid
            self.messageBox(title="Task Name", message="Task name must be between 1 and 30 characters long.")
            self.selectItem(self.selectedItemIndex)
        else:
            itemList[self.selectedItemIndex].setName(name_text) # Push valid input data to the itemList[]

        # Check date format
        if re.match(r"\d{2}/\d{2}/\d{4}", date_text):
            itemList[self.selectedItemIndex].setDate(date_text) # Push valid input data to the itemList[]
        else:
            # Display a error box because date was not valid
            self.messageBox(title="Date format", message="Task date must be in the format mm/dd/yyyy")
            self.selectItem(self.selectedItemIndex)

        # Save current list to file
        saveListData("todolist.txt")
        # Update listBox display to match itemList[]
        self.syncLists()
            

    def syncLists(self):
        # Clear the list box
        self.listBox.delete(0, "end")

        for i in range(len(itemList)):
            self.listBox.insert(self.listBox.size(), itemList[i].getName())

            # Change the display item's background based on the completion status
            if itemList[i].getStatus() == "Not Complete":
                self.listBox.itemconfig(i, {"bg": "indianred"})
            elif itemList[i].getStatus() == "Complete":
                self.listBox.itemconfig(i, {"bg": "darkolivegreen1"})

# This function saves the item list to a text file
def saveListData(filename):
    try:
        file = open(filename, "w")                                                # Open the file
        for item in itemList:                                                     # Loop through each item in itemList[]
            file.write(f"{item.getName()},{item.getDate()},{item.getStatus()}\n") # Save each items properties on a single line, delaminated by a comma
        file.close()                                                              # Close the file
    except Exception as exception:
        print(f"Error saving data: {str(exception)}") # Print an error if data could not be saved

# This function loads new data from a text file, if it exists, to itemList[]
def loadListData(filename):
    try:
        file = open(filename, "r")              # Open the file
        lines = file.readlines()
        for line in lines:                      # Loop through each line of the file
            data = line.strip().split(",")      # Split up each line at the commas
            if len(data) == 3:                  # Make sure there are only three properties saved on the line
                name, date, status = data       # Save the three properies to a new item
                item = Item(name, date, status)
                itemList.append(item)           # Populate the itemList[] with the new items
        file.close()                            # Close the file
    except FileNotFoundError:
        print("File not found. No data loaded.")       # Print an error if the file could not be found
    except Exception as exception:
        print(f"Error loading data: {str(exception)}") # Print an error if data could not be loaded
 
# Main function
def main():
    loadListData("todolist.txt")  # Load data from the file if it exists
    TimeForge().mainloop()        # Call the mainloop method inherited by EasyFrame on TimeForge class
    saveListData("todolist.txt")  # Save data to the file when the program exits

# Execute main() module if the script is being run as the main program, not imported.
if __name__ == "__main__":
    main()