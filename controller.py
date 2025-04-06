# controller.py
# passing duct.py calculations to the UI in ui.py
# MVC - this is the C part ie controller

from duct import Duct  # our duct calculations

# this is our Duct controller class to pass info to ui
class DuctController:
    # CORE: no init as we're not maintaining any state -- this is purely an intermediary class between duct.py and ui.py

    # get all the duct information from duct.py
    def duct_properties(self, 
                        duct_type, 
                        width, 
                        height, 
                        diameter, 
                        flow_rate):
        # all calcs have been done, we'll just "try" to get the info and respresent it
        # so we'll use a try-except block: if it fails, we WON'T raise an error and just output error info clearly
        try:
            # match:case blocks look so much neater than ifs
            match (duct_type):  # duct_type is our match case input
                case "Rectangular":  # for a rect duct
                    # create a rect duct instance
                    duct = Duct(width=int(width),  # set all int, noone's got time for floats here!
                                height=int(height),
                                flow_rate=int(flow_rate),
                                duct_type=duct_type  # same as case
                                )
                case "Round":  # for a round duct
                    # create a round duct instance
                    duct = Duct(diameter=int(diameter),  # set all int, noone's got time for floats here!
                                flow_rate=int(flow_rate),
                                duct_type=duct_type  # same as case
                                )
                case _:  # default case if another type is input
                    # raise error to alert user
                    raise ValueError(f"Unsupported duct type: {duct_type}")
            
            # with duct_type found and instance created, proceed with cals
            area = duct.calculate_area()  # get Ac
            velocity = duct.calculate_velocity()  # get V
            
            # now return the calculated values as DICT
            return {
                "Area": f"{area:.3f} m²",  # max 3 demical
                "Velocity": f"{velocity:.3f} m/s",
                "Success": True,
                "Error": None
            }
        
        # if the try block fails, output error info
        except ValueError as e:
            return {  # return as DICT
                "Area:": "N/A",
                "Velocity:": "N/A",
                "Success:": False,
                "Error:": str(e)  # string output of error message
            }

# Main guard
# This runs only when controller.py is executed directly
if __name__ == "__main__":
    # Create a controller instance
    controller = DuctController()  # "passes" info to "ui"
    
    # Test rectangular duct
    print("Testing Rectangular Duct:")  # console step printout
    # return DICT as rect_result (for Rectangular case)
    rect_result = controller.duct_properties(  # input sample values from duct.py to controller.py
        duct_type="Rectangular",
        width=700,
        height=400,
        diameter=None,
        flow_rate=2000
    )
    # loop through DICT and print each key:value pair from the results
    for key, value in rect_result.items():
        print(f"{key} {value}")
    
    print("\nTesting Round Duct:")  # console step printout
    # return DICT as round_result (for Round case)
    round_result = controller.duct_properties(  # input sample values from duct.py to controller.py
        duct_type="Round",
        width=None,
        height=None,
        diameter=250,
        flow_rate=1000
    )
    # loop through DICT and print each key:value pair from the results
    for key, value in round_result.items():
        print(f"{key} {value}")
    
    print("\nTesting Invalid Duct Type:")  # console step printout
    # return DICT as ValueError (for EXCEPT case)
    invalid_result = controller.duct_properties(
        duct_type="Triangle",  # all invalid inputs, but "Triangle" will trigger the error
        width=-50,
        height="rth",
        diameter=-300,
        flow_rate=-9000
    )
    # loop through DICT and print each key:value pair from the results (ERROR results)
    for key, value in invalid_result.items():
        print(f"{key} {value}")
