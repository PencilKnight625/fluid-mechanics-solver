import math

def calculate_drag(density, velocity, area, drag_coefficient):
    """
    Drag force: F_D = 0.5 * rho * v^2 * C_D * A

    density: fluid density in kg/m³
    velocity: object velocity relative to fluid in m/s
    area: projected frontal area in m²
    drag_coefficient: dimensionless (e.g. 0.47 for sphere, 1.05 for cube)

    Returns drag force in Newtons.
    """
    drag_force = 0.5 * density * velocity**2 * drag_coefficient * area
    drag_kgf = drag_force / 9.81  # convert to kgf for intuition

    return {
        "drag_force_n": round(drag_force, 4),
        "drag_force_kgf": round(drag_kgf, 4),
        "dynamic_pressure_pa": round(0.5 * density * velocity**2, 4),
    }


def calculate_buoyancy(fluid_density, volume):
    """
    Archimedes' principle: F_B = rho * g * V

    fluid_density: density of the fluid in kg/m³
    volume: volume of displaced fluid in m³

    Returns buoyant force in Newtons and whether the object floats
    (you also pass object_mass to check float/sink).
    """
    g = 9.81
    buoyant_force = fluid_density * g * volume

    return {
        "buoyant_force_n": round(buoyant_force, 4),
        "buoyant_force_kgf": round(buoyant_force / g, 4),
        "displaced_mass_kg": round(fluid_density * volume, 4),
    }


def check_float_or_sink(object_mass, fluid_density, volume):
    """
    Determines if an object floats or sinks.

    object_mass: mass of object in kg
    Returns buoyancy result + float/sink verdict.
    """
    result = calculate_buoyancy(fluid_density, volume)
    object_weight = object_mass * 9.81
    buoyant_force = result["buoyant_force_n"]

    if buoyant_force > object_weight:
        verdict = "Floats"
        net_force = buoyant_force - object_weight
        direction = "upward"
    elif buoyant_force < object_weight:
        verdict = "Sinks"
        net_force = object_weight - buoyant_force
        direction = "downward"
    else:
        verdict = "Neutrally buoyant"
        net_force = 0
        direction = "none"

    result["verdict"] = verdict
    result["net_force_n"] = round(net_force, 4)
    result["net_direction"] = direction
    result["object_weight_n"] = round(object_weight, 4)
    return result