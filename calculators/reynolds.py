def calculate_reynolds(density, velocity, diameter, viscosity):
    """
    Calculate Reynolds number.
    Re = (rho * v * D) / mu

    All inputs must already be in SI units:
        density   — kg/m³
        velocity  — m/s
        diameter  — m
        viscosity — Pa·s

    Returns: (reynolds_number: float, flow_type: str)
    """
    reynolds = (density * velocity * diameter) / viscosity

    if reynolds < 2000:
        flow_type = "Laminar"
    elif reynolds <= 4000:
        flow_type = "Transitional"
    else:
        flow_type = "Turbulent"

    return round(reynolds, 4), flow_type