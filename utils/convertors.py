def convert_density(value, from_unit):
    """Convert density to kg/m³."""
    if from_unit == "kg/m3":
        return value
    elif from_unit == "g/cm3":
        return value * 1000
    elif from_unit == "lb/ft3":
        return value * 16.0185
    else:
        return value


def convert_diameter(value, from_unit):
    """Convert diameter to meters."""
    if from_unit == "m":
        return value
    elif from_unit == "cm":
        return value / 100
    elif from_unit == "mm":
        return value / 1000
    elif from_unit == "in":
        return value * 0.0254
    elif from_unit == "ft":
        return value * 0.3048
    else:
        return value


def convert_viscosity(value, from_unit):
    """Convert dynamic viscosity to Pa·s."""
    if from_unit == "Pa-s":
        return value
    elif from_unit == "cP":
        return value / 1000
    elif from_unit == "P":
        return value / 10
    else:
        return value