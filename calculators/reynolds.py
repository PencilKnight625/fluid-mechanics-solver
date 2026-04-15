from utils.converters import UnitConverter
def calculate_reynolds(density, velocity, diameter, viscosity):
    """
    Calculate Reynolds number.
    Re = (rho * v * D) / mu
    """
    reynolds = (density * velocity * diameter) / viscosity

    if reynolds < 2000:
        flow_type = "Laminar"
    elif reynolds <= 4000:
        flow_type = "Transitional"
    else:
        flow_type = "Turbulent"

    return {"reynolds": round(re, 4), "type": flow_type}