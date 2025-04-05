# ui.py
# tkinter graphical user interface

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

# this is our GUI class
class UI:
    def __init__ (self, width, height, bg="black"):
        self.__root = Tk()  # our widget data member
        self.__root.title("Engineering Solver")  # UI title
        self.__root.protocol( "WM_DELETE_WINDOW", self.close)  # X button linked to close method
        self.__canvas = Canvas(self.__root, bg=bg, width=width, height=height)  # canvas in window container
        self.__canvas.pack(fill=BOTH, expand=1)  # pack the canvas to fill x&y and with window resizing
        self.__running = False  # UI window running flag

        # Add this line to create the input fields (instead of in main)
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

        # TEXT FIELDS -- input typing
        # DUCT WIDTH
        # text label with white background
        Label(input_frame, text="Duct Width", bg="white").grid(row=1, column=0, sticky="w", pady=5)
        self.width_var = StringVar()
        # creates a user entry widget for duct width
        width_entry = Entry(input_frame, textvariable=self.width_var)  # auto updates when user types in field
        # positions entry widget
        width_entry.grid(row=1, column=1, sticky="w", pady=5)

        # DUCT HEIGHT
        # text label with white background
        Label(input_frame, text="Duct Height", bg="white").grid(row=2, column=0, sticky="w", pady=5)
        self.height_var = StringVar()
        # creates a user entry widget for duct width
        width_entry = Entry(input_frame, textvariable=self.height_var)  # auto updates when user types in field
        # positions entry widget
        width_entry.grid(row=2, column=1, sticky="w", pady=5)

        # FLOW RATE
        # text label with white background
        Label(input_frame, text="Flow Rate", bg="white").grid(row=3, column=0, sticky="w", pady=5)
        self.flow_rate_var = StringVar()
        # creates a user entry widget for duct width
        width_entry = Entry(input_frame, textvariable=self.flow_rate_var)  # auto updates when user types in field
        # positions entry widget
        width_entry.grid(row=3, column=1, sticky="w", pady=5)


# Main guard
# This runs only when ui.py is executed directly
if __name__ == "__main__":
    # Create a test instance of the UI
    test_ui = UI(800, 600, bg="pink")  # pink window
    print("UI test window created. Close the window to exit.")
    test_ui.wait_for_close()