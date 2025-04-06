# duct.py
# duct calculations
# MVC - this is the M part ie modeller

import math  # for maths like pi etc

# this is our Duct calculation class
class Duct:
    def __init__ (self, 
                  width=None,
                  height=None,
                  diameter=None,
                  flow_rate=None,
                  velocity=None,
                  pressure_drop=None,
                  duct_type="Rectangular"):
        
        # all parameters (except duct_type) are optional
        self.duct_type = duct_type  # rectangular or round (dropdown selection toggle)
        self.width = width  # rectangular: duct width (mm)
        self.height = height  # rectangular: duct height (mm)
        self.diameter = diameter  # round: diameter (mm)
        self.flow_rate = flow_rate  # duct flow rate (L/s)
        self.velocity = velocity  # airflow velocity (m/s)
        self.pressure_drop = pressure_drop  # pressure drop per unit meter (Pa/m)

        # Calculate and store area if we have enough information
        self.area = None
        # if rect OR round has sufficient inputs
        if (self.duct_type == "Rectangular" and self.width is not None and self.height is not None) or \
           (self.duct_type == "Round" and self.diameter is not None):
            self.area = self.calculate_area()  # proceed with calculation
        

    # basic calculation of cross-sectional area A = pi(d/2)^2 or W*H
    def calculate_area(self):
        # input validation
        if self.duct_type not in ["Rectangular", "Round"]:  # neither of these two
            raise ValueError("Invalid duct type!")
        
        # for rect duct type
        if self.duct_type == "Rectangular":
            # check if atleast width AND height is input
            if self.width is None or self.height is None:
                raise ValueError("Width and height must be provided for rectangular duct!")
            area = self.width * self.height * 1e-6  # convert to m²
            return area  # A = W*H (m²)
        
        # otherwise it's round
        # check if atleast diameter is input
        if self.diameter is None:
            raise ValueError("Diameter must be provided for round duct!")
        
        # continue with area calculation
        area = math.pi * (self.diameter/2)**2 * 1e-6  # convert to m²
        return area  # A = pi(d/2)^2 (m²)


    # basic calculation of Q=VA -> V = Q/A
    def calculate_velocity(self):
        # check if flowrate AND area is provided
        if self.flow_rate is None:
            raise ValueError("Flow rate must be provided!")
        if self.area is None:
            # try to calculate area first if possible
            self.area = self.calculate_area()
            # if this cannot happen, raise an error!
            if self.area is None:
                raise ValueError("Area must be provided!")

        # input validation
        if self.flow_rate <= 0:  # flowrate ceck
            raise ValueError("Invalid flow rate!")
        if self.area <= 0:  # area check
            raise ValueError("Invalid area!")
        
        # proceed with velocity calculation
        velocity = (self.flow_rate * 1e-3) / self.area  # convert L/s to m3/s
        return velocity  # V = Q/A (m/s)


# Main guard
# This runs only when duct.py is executed directly
if __name__ == "__main__":
    # Create a test instance of the Duct class
    duct_type = "Rectangular"
    width = 400  # mm
    height = 200  # mm
    diameter = None  # Not needed for rectangular
    flow_rate = 300  # L/s
    velocity = None  # Will calculate this
    pressure_drop = None  # Not using this for now

    # Create Duct Instance
    rect_duct = Duct(width=width, 
                     height=height, 
                     duct_type=duct_type, 
                     flow_rate=flow_rate)

    # Calculate Area
    area = rect_duct.calculate_area()  # get Ac
    print(f"A: {area} m²")  # debug print Area

    # Calculate Velocity
    velocity = rect_duct.calculate_velocity()  # get V
    print(f"V: {velocity} m/s")
