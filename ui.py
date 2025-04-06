# ui.py
# tkinter graphical user interface
# MVC - this is the V part ie viewer

# WINDOW IMPORT
from tkinter import Tk, BOTH, Canvas  # import tkinter
# Tk = main window object container for application
# BOTH = constant for pack() to fill the window/expand widgets in both x & y directions
# Canvas = drawing area for graphics and visuals

# INTERACTIVITY IMPORT
from tkinter import Frame, Label, Entry, StringVar, OptionMenu, Button
# Frame = container widget that holds other widgets
# Label = widget that displays text/images
# Entry = text input field to type
# StringVar = this connects to widgets and updates them
# OptionMenu = dropdown menu widget
# Button = clickable widget

# "TERMINAL" TEXT IMPORT
from tkinter import Text, DISABLED, END
# Text = multiline text editing widget
# DISABLED = constant for making a widget non-editable
# END = constant for end position in a text widget

# CONTROLLER IMPORT (getting model data to viewer via controller, MVC)
from controller import DuctController  # our controller


# CORE - tkinter geometry managers:
# pack() - Packs widgets in blocks before placing them in the parent widget
# grid() - Places widgets in a cell of a conceptual table/grid
# place() - Places widgets using precise coordinates


# this is our GUI class
class UI:
    def __init__ (self, width, height, bg="black"):
        self.__root = Tk()  # our widget data member
        self.__root.title("Engineering Solver")  # UI title
        self.__root.protocol( "WM_DELETE_WINDOW", self.close)  # X button linked to close method
        self.__canvas = Canvas(self.__root, bg=bg, width=width, height=height)  # canvas in window container
        self.__canvas.pack(fill=BOTH, expand=1)  # pack the canvas to fill x&y and with window resizing
        self.__running = False  # UI window running flag

        # Create Controller instance to link model files to viewer
        self.controller = DuctController()  # "passes" info to "ui"

        # Add this line to create the input fields (instead of in main)
        # Create Input Fields in viewer
        self.create_input_fields()

        # after inputs, call the "terminal" output method
        self.create_terminal_output()

        # once init is done, call toggle duct type fields
        self.toggle_duct_type_fields()

    # WINDOW METHODS
    # need a method to update the visuals
    def redraw(self):
        self.__root.update_idletasks()  # process tasks in event queue
        self.__root.update()  # process of task

    # keep running and wait until flag is set false (via X button)
    def wait_for_close(self):
        self.__running = True  # window is running
        while self.__running:  # keep redrawing as long as flag is true
            self.redraw()

    # finally, a method to close it all down when flag is set false
    # add an X button in init to link to this method
    def close(self):  
        self.__running = False

    # INPUT METHODS
    # need a method to create input text fields and dropdowns
    def create_input_fields(self):
        # FRAMES -- to hold input widgets
        input_frame = Frame(self.__root, bg="white", padx=0, pady=0)
        # frame is placed inside window, padding pixels for the frame around the input
        # canvas not used here as it's for graphics!
        input_frame.pack(fill=BOTH, expand=0)  # DON'T expand the frame, but do fill with colour


        # DROPDOWN -- input by selection
        # DUCT TYPE SELECTOR
        # text label with white background
        self.duct_types_label = Label(input_frame, text="Duct Type", bg="white", font=("Arial", 8))  # label instance
        self.duct_types_label.grid(row=0, column=0, sticky="w", pady=0)  # grid position of label instance
        # first row/col, aligned to West, X px vertical pad
        # create tkinter var that holds dropdown selection
        self.duct_type_var = StringVar(value="Rectangular")  # defaults to Rect
        duct_types = ["Rectangular", "Round"]  # list of options
        # create dropdown menu
        self.dropdown = OptionMenu(input_frame, self.duct_type_var, *duct_types)
        # menu in frame, StringVar for updating, * = UNPACK the list as separate args
        self.dropdown.config(font=("Arial", 8))  # update dropdown font
        # position the dropdown menu
        self.dropdown.grid(row=0, column=1, sticky="w", pady=0)  # row1/col2, WEST, X px vertical pad
        # link toggle_duct_type_fields to the dropdown selector using trace
        self.duct_type_var.trace_add("write", self.toggle_duct_type_fields)
        # write = write operation watch, method to call on it


        # ENTRIES -- input typing text fields
        # DUCT WIDTH / DUCT DIAMETER (reuse same field for both entries)
        (self.width_label,
        self.width_var,
        self.width_entry,
        self.width_unit) = (self.input_entry_helper(
                            input_frame, "Duct Width", "white", 1, 
                            unit="(mm)"))
        
        # DUCT HEIGHT
        (self.height_label,
        self.height_var,
        self.height_entry,
        self.height_unit) = (self.input_entry_helper(
                            input_frame, "Duct Height", "white", 1, 3,  # same row as duct width, next col
                            unit="(mm)"))
        
        # FLOW_RATE
        (self.flow_rate_label,
        self.flow_rate_var,
        self.flow_rate_entry,
        self.flow_rate_unit) = (self.input_entry_helper(
                            input_frame, "Flow Rate", "white", 2, 
                            unit="(L/s)"))


        # BUTTONS -- input by clicking
        # CALCULATE
        # Create the Calculate/Run button
        self.calculate_button = Button(input_frame,  # our button's frame
                                  text="Calculate",  # text in button
                                  command=self.run_calculation,  # this calls run calc
                                  padx=0,  # button x & y padding
                                  pady=0,
                                  font=("Arial", 8)    
                                  )
        # grid -- apply button to our field gird position
        self.calculate_button.grid(row=3, column=0, columnspan=2, pady=0, sticky="w")

    # HELPER method to reduce DRY code (less repetitive...)
    # basically makes the label, grid, var & unit, grid = one fell swoop!
    # input row = X, column = default 0, and every entry thereafter just adds 1!
    def input_entry_helper(self, frame, text, bg, row, col=0, sticky="w", pady=0, width=7, unit=None):
        # text label with white background
        label = Label(frame, text=text, bg=bg, font=("Arial", 8))  # label instance
        label.grid(row=row, column=col, sticky=sticky, pady=pady)  # grid position of label instance
        
        # creates a user entry widget for duct width
        var = StringVar()  # holds the tkinter var
        entry = Entry(frame, textvariable=var, width=width)  # auto updates when user types in field
        entry.grid(row=row, column=col+1, sticky=sticky, pady=pady)  # grid position of entry instance
        # NOTE: width = x --> how wide the field is
        
        # if Unit text is entered, created a unit entry
        if unit is not None:
            unit = Label(frame, text=unit, bg=bg, font=("Arial", 8))  # unit instance
            unit.grid(row=row, column=col+2, sticky=sticky, pady=pady)  # grid position of unit instance

        # now return this to new entry
        return label, var, entry, unit


    # hides and renames fields to appropriate duct type
    # this is linked to our duct_type dropdown
    def toggle_duct_type_fields(self, *args):
        # *args = we unpack all the instance's args instead of trying to add all back in
        # first we get the duct type
        duct_type = self.duct_type_var.get()  # use .get() to "get" it

        # now we hide/add fields based on selected duct type in dropdown
        match (duct_type):  # duct_type is our match case input
            case "Rectangular":  # for a rect duct
                # set width label to duct width using config()
                self.width_label.config(text="Duct Width")

                # show the height field
                self.height_label.grid(row=1, column=3, sticky="w", pady=0)
                self.height_entry.grid(row=1, column=4, sticky="w", pady=0)
                self.height_unit.grid(row=1, column=5, sticky="e", pady=0)

            case "Round":  # for a round duct
                # set width label to duct width using config()
                self.width_label.config(text="Duct Diameter")

                # HIDE the height field for round ducts using .grid_remove()
                self.height_label.grid_remove()
                self.height_entry.grid_remove()
                self.height_unit.grid_remove()


    # this method is what's called when clicking the calculate/run button
    def run_calculation(self):
        # get the input values
        duct_type = self.duct_type_var.get()  # use get() to fetch our input fields

        # use a try-except block in case an input is missing
        try:
            # all fields are strs, need to convert to correct types
            # common fields to ALL duct types
            flow_rate = int(self.flow_rate_var.get())  # duct flow rate

            # now let's only valid inputs that are required for each duct type
            # no height for round etc.
            match (duct_type):  # duct_type is our match case input
                case "Rectangular":  # rect duct type
                    width = int(self.width_var.get())  # duct width
                    height = int(self.height_var.get())  # duct height
                    diameter = None  # not used
                case "Round":  # round duct type
                    diameter = int(self.width_var.get())  # duct diameter
                    width = diameter  # Not really used, but keep for API compatibility
                    height = None  # not used

            # now that we've validated the correct duct types, let's process the results
            # call the controller to provide us with the calculated results (from duct.py)
            results = self.controller.duct_properties(duct_type, width, height, diameter, flow_rate)
            
            # now that we have the inputs & calculations successfully, let's display the results!
            self.display_results(results)

        except ValueError:
            # need an error to print if we cannot reach the input fields
            # let's do this to terminal, using DICT struct
            error_message = {"Error": "Missing input fields or invalid input!"}
            self.display_results(error_message)

    
    # make a new Text widget below fields for "terminal" output simulation
    def create_terminal_output(self):
        # Create a terminal-like text area
        self.terminal = Text(self.__root, bg="black", fg="green", font=("Courier", 10), height=10)
        # bg = background colour, fg = text colour "foreground", font = font + textheight, height = TEXT block height
        # now place it on the canvas using pack()
        self.terminal.pack(fill=BOTH, expand=1, padx=0, pady=0)

    # this method is what's called when clicking the calculate/run button
    def display_results(self, results):
        # clear previous results
        self.terminal.config(state="normal")  # set editable temporarily to delete
        # config() = widget options, state = editable, "normal" = allows editing
        self.terminal.delete(1.0, END)  # delete and then set uneditable
        # delete() = clear text from widget, 1.0 = start at line1 char 0, END = (delete from start to END of text)

        # loop through result key:value's and print to "terminal" (use insert() for text widgets)
        for key, value in results.items():  # .items() = just returns pairs from a dict
            self.terminal.insert(END, f"{key}: {value}\n")  # insert at END position

        # after clearing and inserting text, remove editing
        self.terminal.config(state=DISABLED)


# Main guard
# This runs only when ui.py is executed directly
if __name__ == "__main__":
    # Create a test instance of the UI
    test_ui = UI(800, 600, bg="pink")  # pink window
    print("UI test window created. Close the window to exit.")
    test_ui.wait_for_close()
