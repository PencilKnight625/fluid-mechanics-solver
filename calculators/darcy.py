import math

def friction_factor_laminar(reynolds):
    """Laminar friction factor: f = 64 / Re"""
    return 64 / reynolds


def friction_factor_turbulent(reynolds, roughness, diameter):
    """
    Colebrook-White equation (solved iteratively).
    This is the real engineering formula used in industry.
    roughness = pipe roughness in meters (e.g. 0.000046 for steel)
    """
    relative_roughness = roughness / diameter
    # Initial guess using Swamee-Jain approximation
    f = 0.25 / (math.log10(relative_roughness / 3.7 + 5.74 / (reynolds ** 0.9))) ** 2

    # Iterate Colebrook-White 50 times for convergence
    for _ in range(50):
        f = (-2 * math.log10(relative_roughness / 3.7 + 2.51 / (reynolds * math.sqrt(f)))) ** -2

    return round(f, 6)


def calculate_head_loss(friction_factor, length, diameter, velocity):
    """
    Darcy-Weisbach equation: h_f = f * (L/D) * (v^2 / 2g)
    Returns head loss in meters.
    """
    g = 9.81  # gravitational acceleration m/s²
    head_loss = friction_factor * (length / diameter) * (velocity ** 2 / (2 * g))
    return round(head_loss, 4)


def calculate_darcy(density, velocity, diameter, viscosity,
                    pipe_length, roughness):
    """
    Full Darcy-Weisbach calculation.
    Automatically picks laminar or turbulent friction factor.

    Returns a dict with all results.
    """
    reynolds = (density * velocity * diameter) / viscosity

    if reynolds < 2000:
        flow_regime = "Laminar"
        f = friction_factor_laminar(reynolds)
    elif reynolds <= 4000:
        flow_regime = "Transitional"
        # Use turbulent formula as conservative estimate
        f = friction_factor_turbulent(reynolds, roughness, diameter)
    else:
        flow_regime = "Turbulent"
        f = friction_factor_turbulent(reynolds, roughness, diameter)

    h_loss = calculate_head_loss(f, pipe_length, diameter, velocity)

    # Pressure drop: delta_P = rho * g * h_f
    g = 9.81
    pressure_drop = round(density * g * h_loss, 2)

    return {
        "reynolds": round(reynolds, 2),
        "flow_regime": flow_regime,
        "friction_factor": f,
        "head_loss_m": h_loss,
        "pressure_drop_pa": pressure_drop,
    }