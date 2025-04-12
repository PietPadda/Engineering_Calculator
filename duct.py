# duct.py
# duct calculations
# MVC - this is the M part ie modeller

import math  # for maths like pi etc

# this is our Duct calculation class
class Duct:
    def __init__ (self,
                  # Core inputs from UI/Controller
                  duct_type: str,
                  flow_rate: float,
                  roughness: float,
                  temperature: float,
                  relative_humidity: float,
                  elevation: float,
                  noise_direction_factor: int,
                  noise_distance: float,

                  # Dimension inputs from UI/Controller: int OR None type, default = None
                  width: int | None = None,
                  height: int | None = None,
                  diameter: int | None = None,
                  ):

        # store the duct type and dimensions
        self.duct_type = duct_type  # rectangular or round (dropdown selection toggle)
        self.width = width  # rectangular: duct width (mm)
        self.height = height  # rectangular: duct height (mm)
        self.diameter = diameter  # round: diameter (mm)

        # store flow rate
        self.flow_rate = flow_rate  # duct flow rate (L/s)
        
        # store environment and material properties
        self.roughness = roughness  # absolute roughness (mm)
        self.temperature = temperature  # ambient temperature (°C)
        self.relative_humidity = relative_humidity  # ambient relative humidity (%)
        self.elevation = elevation  # elevation (m)

        # store noise parameters
        self.noise_direction_factor = noise_direction_factor  # noise direction factor (N/A)
        self.noise_distance = noise_distance  # noise distance (m)

        # use memoisation (caching) to only need to calculate each variable once
        # we're calling each function possible multiple times, so prevents
        # need to calculate the same thing over and over again!
        # Note: use single _ to indicate "internal" use (mangling __ is overkill!)
        self._area = None  # cross-sectional area (m2)
        self._velocity = None  # velocity (m/s)
        self._perimeter = None  # duct perimeter length (m)
        self._D_equivalent = None  # equivalent diameter (m)
        self._hydraulic_diameter = None  # duct hydraulic diameter (m)
        self._dynamic_viscosity = None  # dynamic viscosity (kg/m.s)
        self._air_density = None  # air density (kg/m^3)
        self._reynolds = None  # reynold's number (N/A)
        self._flow_state = None  # flow state (N/A)
        self._friction_factor = None  # friction factor
        self._static_pressure = None  # static pressure drop (per unit m) (Pa/m)
        self._dynamic_pressure = None  # dynamic pressure drop (per unit m) (Pa/m)
        self._total_pressure = None  # total pressure drop (per unit m) (Pa/m)
        self._loss_coefficient = None  # loss coefficient (N/A)
        self._SWL = None  # sound power level (dB)
        self._SPL = None  # sound pressure level (dB)
        # CORE: in each func: cache check? -> if false, calc -> store (cache check = true) -> return


    # basic calculation of cross-sectional area A = pi(d/2)^2 or rect: W*H
    def calculate_area(self):
        # cache check
        if self._area is not None:
            return self._area  # already calcd, reuse when func is called!

        # input validation
        if self.duct_type not in ["Rectangular", "Round"]:  # neither of these two
            raise ValueError("Invalid duct type!")
        
        # for rect duct type
        if self.duct_type == "Rectangular":
            # check if atleast width AND height is input
            if self.width is None or self.height is None:
                raise ValueError("Width and height must be provided for rectangular duct!")
            self._area = self.width * self.height * 1e-6  # convert to m²
            return self._area  # A = W*H (m²)
        
        # otherwise it's round
        # check if atleast diameter is input
        if self.diameter is None:
            raise ValueError("Diameter must be provided for round duct!")
        
        # continue with area calculation
        self._area = math.pi * (self.diameter/2)**2 * 1e-6  # convert to m²
        return self._area  # A = pi(d/2)^2 (m²)

    # basic calculation of Q=VA -> V = Q/A
    def calculate_velocity(self):
        # cache check
        if self._velocity is not None:
            return self._velocity # already calcd, reuse when func is called!
        
        Q = self.flow_rate
        A = self.calculate_area()  # cache call

        # check if flowrate AND area is provided
        if Q is None:
            raise ValueError("Flow rate must be provided!")

        # input validation
        if Q <= 0:  # flowrate ceck
            raise ValueError("Invalid flow rate!")
        if A <= 0:  # area check
            raise ValueError("Invalid area!")
        
        # proceed with velocity calculation
        self._velocity = (Q * 1e-3) / A  # convert L/s to m3/s
        return self._velocity  # V = Q/A (m/s)

    # perimeter is required for Deq (only for rectangular really as Dh = D_round!)
    # P = 2 * (W + H) / pi * D
    def calculate_duct_perimeter(self):
        # cache check
        if self._perimeter is not None:
            return self._perimeter # already calcd, reuse when func is called!
        
        W = self.width
        H = self.height
        D = self.diameter
        duct_type = self.duct_type

        # rectangular duct
        if duct_type == "Rectangular":
            self._perimeter = 2 * (W + H) * 1e-3  # convert to m
            return self._perimeter
        # round duct
        if duct_type == "Round":
            self._perimeter =  math.pi * D * 1e-3  # convert to m
            return self._perimeter

    # equivalent diameter is for rounding rectangular ducts (need for hydraulic diameter)
    # Deq = (1.3 * Ac^0.625) / [ (P/2)^0.25 ]  or round: D lol
    def calculate_equivalent_diameter(self):
        # cache check
        if self._D_equivalent is not None:
            return self._D_equivalent # already calcd, reuse when func is called!
        
        A = self.calculate_area()  # cache call
        p = self.calculate_duct_perimeter()  # cache call
        duct_type = self.duct_type
        D = self.diameter
    
        # rectangular duct
        if duct_type == "Rectangular":
            self._D_equivalent = (1.3 * A**0.625) / ( (p / 2)**0.25 )
            return self._D_equivalent
        # round duct
        if duct_type == "Round":
            self._D_equivalent = D * 1e-3  # yeah, self explanatory! Deq = D!
            return self._D_equivalent

    # hydraulic diameter is creitical for fluid mechanics calculations
    # Dh = 4*Ac / P  or round: D
    def calculate_hydraulic_diameter(self):
        # cache check
        if self._hydraulic_diameter is not None:
            return self._hydraulic_diameter # already calcd, reuse when func is called!
        
        A = self.calculate_area()  # cache call
        p = self.calculate_duct_perimeter()  # cache call
        duct_type = self.duct_type
        D = self.diameter

        # rectangular duct
        if duct_type == "Rectangular":
            self._hydraulic_diameter = 4 * A / p
            return self._hydraulic_diameter
        
        # round duct
        if duct_type == "Round":
            self._hydraulic_diameter = D * 1e-3  # yeah, self explanatory! Dh = D!
            return self._hydraulic_diameter
            

    # dynamic viscosity is critical for friction calcs
    # We'll do this using Sutherland's law
    def calculate_dynamic_viscosity(self):
        # cache check
        if self._dynamic_viscosity is not None:
            return self._dynamic_viscosity # already calcd, reuse when func is called!
        
        # Standard air
        Sutherlands_constant = 120
        Centipoise = 0.01827
        T_ref_R = 524.07  # reference T (°R)
        T_amb_R = self.temperature*9/5+491.67  # ambient air °C to °R conversion
        constant_A = 0.555*T_ref_R+Sutherlands_constant  # first constant in the calc
        constant_B = 0.555*T_amb_R+Sutherlands_constant  # second constant in the calc

        # store cache
        self._dynamic_viscosity = Centipoise*(constant_A/constant_B)*(T_amb_R/T_ref_R)**(3/2)/1000  # (kg/ms)
        return self._dynamic_viscosity

    # air density is critical for friction calcs
    def calculate_air_density(self):
        # cache check
        if self._air_density is not None:
            return self._air_density # already calcd, reuse when func is called!
        
        # Standard air
        elevation = self.elevation
        temp = self.temperature
        Rh = self.relative_humidity

        Rd = 287.057  # specific gas constant for dry air (J/kg.K)
        Rv = 461.495  # specific gas constant for water vapour (J/kg.K)
        P = 101325 * (1 - 2.25577 * (10**-5) * elevation) ** 5.25588  # air pressure at elevation (Pa)
        P1 = 6.1078 * 10 ** (7.5 * temp /(temp + 237.3))  # Saturated Vapour Pressure at given Temperature (Pa)
        Pv = Rh * P1  # Actual Vapour Pressure (Pa)
        Pd = P - Pv  # Dry air pressure (Pa)
        T_K = temp + 273.15  # air temp in kelvin (K)

        # cache store
        self._air_density = (Pd / (Rd * T_K)) + (Pv / (Rv * T_K))  # air density (kg/m3)
        return self._air_density

    # Reynold's number is critical for friction calcs
    def calculate_reynolds_number(self):
        # cache check
        if self._reynolds is not None:
            return self._reynolds # already calcd, reuse when func is called!
        
        u = self.calculate_dynamic_viscosity()  # cache call
        p = self.calculate_air_density()  # cache call
        Dh = self.calculate_hydraulic_diameter()  # cache call
        V = self.calculate_velocity()  # cache call

        # calculate kinematic viscosity
        v = u / p  # kinematic viscosity (m^2/s)

        # cache store
        self._reynolds = V * Dh / v  # Reynold's number (N/A)
        return self._reynolds

    # Flow state of air is calculated via the Reynold's number
    def calculate_flow_state(self):
        # cache check
        if self._flow_state is not None:
            return self._flow_state # already calcd, reuse when func is called!
        
        Re = self.calculate_reynolds_number()  # cache call
        

        if Re >= 4000:  # turbulent is 4000+ (99.9999% of our cases)
            # store cache
            self._flow_state = "Turbulent"
        elif Re >= 2000:  # transitional is 2000-4000 (probably never...)
            # store cache
            self._flow_state = "Transitional"
        else:
            # store cache
            self._flow_state = "Laminar"  # laminar is 0 -2000 (probably never...)
        return self._flow_state

    # Altshul-Tsal friction factor is calulated via Reynold's number
    def calculate_altshul_tsal(self):
        # cache check
        if self._friction_factor is not None:
            return self._friction_factor # already calcd, reuse when func is called!
        
        r = self.roughness
        Re = self.calculate_reynolds_number()  # cache call
        Dh = self.calculate_hydraulic_diameter()  # cache call
        state = self.calculate_flow_state()  # cache call
        
        match (state):
            case "Turbulent":  # this will be our case 99.9999% of the time
                # first calc f' factor
                f_temp = 0.11*((r/1000)/Dh+68/Re)**0.25  # f' factpr

                if f_temp >= 0.018:  # if f' > 0.018
                    # cache store
                    self._friction_factor = f_temp  # f = f'
                else:  # otherwise
                    # cache store
                    self._friction_factor = f_temp * 0.85 + 0.0028  # f = f`*0.85 + 0.0028
                return self._friction_factor
                
            case "Transitional":
                # cache store
                self._friction_factor = 0  # transitional f = 0
                return self._friction_factor
            
            case "Laminar":
                # cache store
                self._friction_factor = 64 / Re  # laminar 64/Re
                return self._friction_factor

    # Static pressure drop is a factor of altshul-tsal friction factor
    # delP= f * (L / Dh) * p * [ (Vc^2) / 2 ]
    def calculate_static_pressure_drop(self):
        # cache check
        if self._static_pressure is not None:
            return self._static_pressure # already calcd, reuse when func is called!
        
        f = self.calculate_altshul_tsal()  # cache call
        Dh = self.calculate_hydraulic_diameter()  # cache call
        p = self.calculate_air_density()  # cache call
        V = self.calculate_velocity()  # cache call

        # cache store
        self._static_pressure = f * (1 / Dh) * p * ((V**2) / 2)
        return  self._static_pressure

    # Dynamic pressure drop is a factor of V & p
    # P_v= 0.5 * p * V_c^2
    def calculate_dynamic_pressure_drop(self):
        # cache check
        if self._dynamic_pressure is not None:
            return self._dynamic_pressure # already calcd, reuse when func is called!
        
        p = self.calculate_air_density()  # cache call
        V = self.calculate_velocity()  # cache call

        # cache store
        self._dynamic_pressure = 0.5 * p * V**2
        return self._dynamic_pressure

    # Total pressure is the sum of static and dynamic
    def calculate_total_pressure_drop(self):
        # cache check
        if self._total_pressure is not None:
            return self._total_pressure # already calcd, reuse when func is called!
        
        Ps = self.calculate_static_pressure_drop()  # cache call
        Pd = self.calculate_dynamic_pressure_drop()  # cache call

        # cache store
        self._total_pressure = Ps + Pd
        return self._total_pressure

    # Loss coefficient is a ratio of dynamic and static pressure
    def calculate_loss_coefficient(self):
        # cache check
        if self._loss_coefficient is not None:
            return self._loss_coefficient # already calcd, reuse when func is called!
        
        Ps = self.calculate_static_pressure_drop()  # cache call
        Pd = self.calculate_dynamic_pressure_drop()  # cache call

        # cache store
        self._loss_coefficient = Ps / Pd
        return self._loss_coefficient

    # Sound power level is a factor of area and velocity
    def calculate_SWL(self):
        # cache check
        if self._SWL is not None:
            return self._SWL # already calcd, reuse when func is called!
        
        V = self.calculate_velocity()  # cache call
        A = self.calculate_area()  # cache call
        
        # cache store
        self._SWL = 10 + 50 * math.log10(V) + 10 * math.log10(A)
        return self._SWL

    # Sound pressure level is a factor of SWL, directivity and distance to source
    def calculate_SPL(self):
        # cache check
        if self._SPL is not None:
            return self._SPL # already calcd, reuse when func is called!
        
        SWL = self.calculate_SWL()  # cache call
        dir = self.noise_direction_factor
        dist = self.noise_distance

        # cache store
        self._SPL = SWL - abs(10 * math.log10(dir / (4 * math.pi * (dist**2))))
        return self._SPL


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