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
        Label(input_frame, text="Duct Type", bg="white").grid(row=0, column=0, sticky="w", pady=5)
        # first row/col, aligned to West, X px vertical pad
        # create tkinter var that holds dropdown selection
        self.duct_type_var = StringVar(value="Rectangular")  # defaults to Rect
        duct_types = ["Rectangular", "Round"]  # list of options
        # create dropdown menu
        dropdown = OptionMenu(input_frame, self.duct_type_var, *duct_types)
        # menu in frame, StringVar for updating, * = UNPACK the list as separate args
        # position the dropdown menu
        dropdown.grid(row=0, column=1, sticky="w", pady=5)  # row1/col2, WEST, X px vertical pad


        # ENTRIES -- input typing text fields
        # DUCT WIDTH
        # text label with white background
        Label(input_frame, text="Duct Width", bg="white").grid(row=1, column=0, sticky="w", pady=5)
        self.width_var = StringVar()
        # creates a user entry widget for duct width
        width_entry = Entry(input_frame, textvariable=self.width_var, width=7)  # auto updates when user types in field
        # widht = x --> how wide the field is
        # positions entry widget
        width_entry.grid(row=1, column=1, sticky="w", pady=5)
        Label(input_frame, text="(mm)", bg="white").grid(row=1, column=2, sticky="e", pady=5)  # Unit label

        # DUCT HEIGHT
        # text label with white background
        Label(input_frame, text="Duct Height", bg="white").grid(row=1, column=3, sticky="w", pady=5)
        self.height_var = StringVar()
        # creates a user entry widget for duct width
        width_entry = Entry(input_frame, textvariable=self.height_var, width=7)  # auto updates when user types in field
        # positions entry widget
        width_entry.grid(row=1, column=4, sticky="w", pady=5)
        Label(input_frame, text="(mm)", bg="white").grid(row=1, column=5, sticky="e", pady=5)  # Unit label

        # FLOW RATE
        # text label with white background
        Label(input_frame, text="Flow Rate", bg="white").grid(row=2, column=0, sticky="w", pady=5)
        self.flow_rate_var = StringVar()
        # creates a user entry widget for duct width
        width_entry = Entry(input_frame, textvariable=self.flow_rate_var, width=7)  # auto updates when user types in field
        # positions entry widget
        width_entry.grid(row=2, column=1, sticky="w", pady=5)
        Label(input_frame, text="(L/s)", bg="white").grid(row=2, column=2, sticky="e", pady=5)  # Unit label

        # BUTTONS -- input by clicking
        # CALCULATE
        # Create the Calculate/Run button
        calculate_button = Button(input_frame,  # our button's frame
                                  text="Calculate",  # text in button
                                  command=self.run_calculation,  # this calls run calc
                                  padx=10,  # button x & y padding
                                  pady=5    
                                  )
        # grid -- apply button to our field gird position
        calculate_button.grid(row=3, column=0, columnspan=2, pady=10, sticky="w")

    # this method is what's called when clicking the calculate/run button
    def run_calculation(self):
        # get the input values
        duct_type = self.duct_type_var.get()  # use get() to fetch our input fields

        # use a try-except block in case an input is missing
        try:
            # all fields are strs, need to convert to correct types
            width = int(self.width_var.get())  # duct width
            height = int(self.height_var.get())  # duct height
            diameter = width  # DIAMETER (TODO: Placeholder for when implementing Roudn calcs)
            flow_rate = int(self.flow_rate_var.get())  # duct flow rate

            # call the controller to provide us with the calculated results
            results = self.controller.duct_properties(duct_type, width, height, diameter, flow_rate)
            
            # now that we have the inputs & calculations successfully, let's display the results!
            self.display_results(results)

        except ValueError:
            # need an error to print if we cannot reach the input fields
             print("Missing input fields!")

    # this method is what's called when clicking the calculate/run button
    def display_results(self, results):
        # create a results frame for placing on the canvas
        self.results_frame = Frame(self.__root, bg="white", padx=10, pady=10)
        self.results_frame.pack(fill=BOTH, expand=1)  # expand=1, need to fit to window

        # clear all old results on clicking the run button
        # loop through results frame to find each widget
        for widget in self.results_frame.winfo_children():
            widget.destroy()
            # .winfo_children() -- tkinter method getting all widgets inside the frame
            # .destroy() -- tkinter method to clear (DESTROY!) the widget

        # now that we've got a clean slate, let's display the results!
        row = 0  # we'll place it at top of canvas
        # next loop through each key:value pair of our results dictionary
        for key, value in results.items():
            # how to present? create labels
            Label(self.results_frame, text=f"{key}:", bg="white").grid(row=row, column=0, sticky="w", pady=5)  # key:
            Label(self.results_frame, text=str(value), bg="white").grid(row=row, column=1, sticky="w", pady=5)  # value
            row += 1  # row++ for each loop to print out each dict result per iteration


# Main guard
# This runs only when ui.py is executed directly
if __name__ == "__main__":
    # Create a test instance of the UI
    test_ui = UI(800, 600, bg="pink")  # pink window
    print("UI test window created. Close the window to exit.")
    test_ui.wait_for_close()
