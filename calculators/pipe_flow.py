import math

def calculate_pipe_flow(density, viscosity, diameter, pressure_drop, length):
    """
    Hagen-Poiseuille equation (laminar flow only):
    Q = (pi * D^4 * delta_P) / (128 * mu * L)

    Returns flow rate Q in m³/s and mean velocity.
    Also checks if laminar assumption is valid.
    """
    radius = diameter / 2
    Q = (math.pi * radius**4 * pressure_drop) / (8 * viscosity * length)
    area = math.pi * radius**2
    velocity = Q / area
    reynolds = (density * velocity * diameter) / viscosity

    valid = reynolds < 2100  # Hagen-Poiseuille only valid for laminar

    return {
        "flow_rate_m3_per_s": round(Q, 8),
        "flow_rate_lpm": round(Q * 1000 * 60, 4),   # litres per minute
        "mean_velocity_m_per_s": round(velocity, 6),
        "reynolds": round(reynolds, 2),
        "laminar_assumption_valid": valid,
        "note": "Valid (Re < 2100)" if valid else "WARNING: Re > 2100, flow may not be laminar. Use Darcy-Weisbach instead."
    }


def calculate_continuity(area1, velocity1, area2):
    """
    Continuity equation for incompressible flow: A1*v1 = A2*v2
    Given area1, velocity1, area2 — finds velocity2.
    """
    velocity2 = (area1 * velocity1) / area2
    flow_rate = area1 * velocity1

    return {
        "velocity2_m_per_s": round(velocity2, 6),
        "flow_rate_m3_per_s": round(flow_rate, 8),
        "flow_rate_lpm": round(flow_rate * 60000, 4),
    }


def calculate_pump_power(density, flow_rate, head, efficiency=0.75):
    """
    Pump power: P = (rho * g * Q * H) / eta

    flow_rate: m³/s
    head: total head in meters
    efficiency: pump efficiency (0 to 1), default 75%

    Returns shaft power in Watts and kW.
    """
    g = 9.81
    hydraulic_power = density * g * flow_rate * head
    shaft_power = hydraulic_power / efficiency

    return {
        "hydraulic_power_w": round(hydraulic_power, 2),
        "shaft_power_w": round(shaft_power, 2),
        "shaft_power_kw": round(shaft_power / 1000, 4),
        "efficiency_pct": round(efficiency * 100, 1),
    }