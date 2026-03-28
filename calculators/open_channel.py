import math

def calculate_manning(Manning_n, area, wetted_perimeter, slope):
    """
    Manning's equation: Q = (1/n) * A * R^(2/3) * S^(1/2)

    Manning_n: Manning's roughness coefficient (dimensionless)
    area: cross-sectional area of flow in m²
    wetted_perimeter: length of channel boundary in contact with fluid (m)
    slope: channel bed slope (dimensionless, e.g. 0.001)

    Returns flow rate Q and mean velocity.
    """
    hydraulic_radius = area / wetted_perimeter
    velocity = (1 / Manning_n) * (hydraulic_radius ** (2/3)) * (slope ** 0.5)
    flow_rate = velocity * area

    return {
        "flow_rate_m3_per_s": round(flow_rate, 6),
        "flow_rate_cumecs": round(flow_rate, 6),   # m³/s, common unit in hydrology
        "mean_velocity_m_per_s": round(velocity, 6),
        "hydraulic_radius_m": round(hydraulic_radius, 6),
    }


def calculate_rectangular_channel(width, depth, Manning_n, slope):
    """
    Shortcut for rectangular open channels.
    Computes area and wetted perimeter automatically.
    """
    area = width * depth
    wetted_perimeter = width + 2 * depth
    result = calculate_manning(Manning_n, area, wetted_perimeter, slope)
    result["area_m2"] = round(area, 6)
    result["wetted_perimeter_m"] = round(wetted_perimeter, 6)
    return result