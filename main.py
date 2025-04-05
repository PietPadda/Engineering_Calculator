# main.py
# main application loop
from ui import UI  # our tkinter GUI

def main():
    # create tkinter window
    window = UI(600, 480)  # set width & height in pixels

    # call close method on clicking X
    window.wait_for_close()


# Main guard
# Need this to run!
if __name__ == "__main__":
    main()
