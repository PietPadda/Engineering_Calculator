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
        input_frame = Frame(self.__root, bg="white", padx=10, pady=10)
        # frame is placed inside window, padding pixels for the frame around the input
        # canvas not used here as it's for graphics!
        input_frame.pack(fill=BOTH, expand=0)  # DON'T expand the frame, but do fill with colour


        # DROPDOWN -- input by selection
        # DUCT TYPE SELECTOR
        # text label with white background
        self.duct_types_label = Label(input_frame, text="Duct Type", bg="white")  # label instance
        self.duct_types_label.grid(row=0, column=0, sticky="w", pady=5)  # grid position of label instance
        # first row/col, aligned to West, X px vertical pad
        # create tkinter var that holds dropdown selection
        self.duct_type_var = StringVar(value="Rectangular")  # defaults to Rect
        duct_types = ["Rectangular", "Round"]  # list of options
        # create dropdown menu
        self.dropdown = OptionMenu(input_frame, self.duct_type_var, *duct_types)
        # menu in frame, StringVar for updating, * = UNPACK the list as separate args
        # position the dropdown menu
        self.dropdown.grid(row=0, column=1, sticky="w", pady=5)  # row1/col2, WEST, X px vertical pad
        # link toggle_duct_type_fields to the dropdown selector using trace
        self.duct_type_var.trace_add("write", self.toggle_duct_type_fields)
        # write = write operation watch, method to call on it



        # ENTRIES -- input typing text fields
        # DUCT WIDTH / DUCT DIAMETER (reuse same field for both entries)
        # text label with white background
        self.width_label = Label(input_frame, text="Duct Width", bg="white")  # label instance
        self.width_label.grid(row=1, column=0, sticky="w", pady=5)  # grid position of label instance
        self.width_var = StringVar()
        # creates a user entry widget for duct width
        self.width_entry = Entry(input_frame, textvariable=self.width_var, width=7)  # auto updates when user types in field
        # widht = x --> how wide the field is
        # positions entry widget
        self.width_entry.grid(row=1, column=1, sticky="w", pady=5)
        self.width_unit = Label(input_frame, text="(mm)", bg="white")  # unit instance
        self.width_unit.grid(row=1, column=2, sticky="e", pady=5)  # grid position of unit instance

        # DUCT HEIGHT
        # text label with white background
        self.height_label = Label(input_frame, text="Duct Height", bg="white")  # label instance
        self.height_label.grid(row=1, column=3, sticky="w", pady=5)  # grid position of label instance
        self.height_var = StringVar()
        # creates a user entry widget for duct width
        self.height_entry = Entry(input_frame, textvariable=self.height_var, width=7)  # auto updates when user types in field
        # positions entry widget
        self.height_entry.grid(row=1, column=4, sticky="w", pady=5)
        self.height_unit = Label(input_frame, text="(mm)", bg="white")  # unit instance
        self.height_unit.grid(row=1, column=5, sticky="e", pady=5)  # grid position of unit instance

        # FLOW RATE
        # text label with white background
        self.flow_rate_label = Label(input_frame, text="Flow Rate", bg="white")  # label instance
        self.flow_rate_label.grid(row=2, column=0, sticky="w", pady=5)  # grid position of label instance
        self.flow_rate_var = StringVar()
        # creates a user entry widget for duct width
        self.flow_rate_entry = Entry(input_frame, textvariable=self.flow_rate_var, width=7)  # auto updates when user types in field
        # positions entry widget
        self.flow_rate_entry.grid(row=2, column=1, sticky="w", pady=5)
        self.flow_rate_unit = Label(input_frame, text="(L/s)", bg="white")  # unit instance
        self.flow_rate_unit.grid(row=2, column=2, sticky="e", pady=5)  # grid position of unit instance

        # BUTTONS -- input by clicking
        # CALCULATE
        # Create the Calculate/Run button
        self.calculate_button = Button(input_frame,  # our button's frame
                                  text="Calculate",  # text in button
                                  command=self.run_calculation,  # this calls run calc
                                  padx=10,  # button x & y padding
                                  pady=5    
                                  )
        # grid -- apply button to our field gird position
        self.calculate_button.grid(row=3, column=0, columnspan=2, pady=10, sticky="w")


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
                self.height_label.grid(row=1, column=3, sticky="w", pady=5)
                self.height_entry.grid(row=1, column=4, sticky="w", pady=5)
                self.height_unit.grid(row=1, column=5, sticky="e", pady=5)

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
        self.terminal.pack(fill=BOTH, expand=1, padx=10, pady=10)

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
