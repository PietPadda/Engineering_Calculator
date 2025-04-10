# controller.py
# passing duct.py calculations to the UI in ui.py
# MVC - this is the C part ie controller

from duct import Duct  # our duct calculations

# this is our Duct controller class to pass info to ui
class DuctController:
    # CORE: no init as we're not maintaining any state -- this is purely an intermediary class between duct.py and ui.py

    # get all the duct information from duct.py
    def duct_properties(
        self, 
        duct_type: str,
        flow_rate: int,
        roughness: float,
        temperature: float,
        relative_humidity: float,
        elevation: float,
        noise_direction_factor: int,
        noise_distance: float,
        width: int | None,
        height: int | None,
        diameter: int | None
        ):

        # input validation
        # all calcs have been done, we'll just "try" to get the info and respresent it
        # so we'll use a try-except block: if it fails, we WON'T raise an error and just output error info clearly
        try:
            # match:case blocks look so much neater than ifs
            match (duct_type):  # duct_type is our match case input
                case "Rectangular":  # for a rect duct
                    # create a rect duct instance
                    duct = Duct(duct_type=duct_type,  # same as case
                                flow_rate=int(flow_rate),  # set int... we don't work in float rates
                                roughness=roughness,
                                temperature=temperature,
                                relative_humidity=relative_humidity,
                                elevation=elevation,
                                noise_direction_factor=noise_direction_factor,
                                noise_distance=noise_distance,
                                width=int(width),  # set int... we don't work in float dims
                                height=int(height),  # set int... we don't work in float dims
                                diameter=None  # not needed for rectangular
                                )
                    
                case "Round":  # for a round duct
                    # create a round duct instance
                    duct = Duct(duct_type=duct_type,  # same as case
                                flow_rate=int(flow_rate),  # set int... we don't work in float rates
                                roughness=roughness,
                                temperature=temperature,
                                relative_humidity=relative_humidity,
                                elevation=elevation,
                                noise_direction_factor=noise_direction_factor,
                                noise_distance=noise_distance,
                                width=None,  # not needed for round
                                height=None,  # not needed for round
                                diameter=int(diameter)  # set int... we don't work in float dims
                                )
                    
                case _:  # default case if another type is input
                    # raise error to alert user
                    raise ValueError(f"Unsupported duct type: {duct_type}")
            
            # Duct instances have been made!
            # Now we just call the functions from duct.py in our return outputs!
            
            # now return the calculated values as DICT
            return {
                "Area": f"{duct.calculate_area():.3f} m²",  # max 3 demical
                "Velocity": f"{duct.calculate_velocity():.3f} m/s",
                "Perimeter": f"{duct.calculate_duct_perimeter():.3f} m",
                "Equivalent Diameter": f"{duct.calculate_equivalent_diameter():.3f} m",
                "Hydraulic Diameter": f"{duct.calculate_hydraulic_diameter():.3f} m",
                "Dynamic Viscosity": f"{duct.calculate_dynamic_viscosity():.3f} kg/m.s",
                "Air Density": f"{duct.calculate_air_density():.3f} kg/m³",
                "Reynold's Number": f"{duct.calculate_reynolds_number():.3f} N/A",
                "Flow State": duct.calculate_flow_state(),
                "Friction Factor": f"{duct.calculate_altshul_tsal():.3f}",
                "Static Pressure Drop": f"{duct.calculate_static_pressure_drop():.3f} Pa/m",
                "Dynamic Pressure Drop": f"{duct.calculate_dynamic_pressure_drop():.3f} Pa/m",
                "Total Pressure Drop": f"{duct.calculate_total_pressure_drop():.3f} Pa/m",
                "Loss Coefficient": f"{duct.calculate_loss_coefficient():.3f}",
                "Sound Power Level": f"{duct.calculate_SWL():.3f} dB",
                "Sound Pressure Level": f"{duct.calculate_SPL():.3f} dB",
            }
        
        # if the try block fails, output error info
        except ValueError as e:
            return {  # return as DICT
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
