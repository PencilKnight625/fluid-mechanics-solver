# utils/converters.py

class UnitConverter:
    # Mapping units to their multiplier to reach SI (meters, kg/m3, Pa-s)
    FACTORS = {
        'length': {'m': 1.0, 'cm': 0.01, 'mm': 0.001, 'in': 0.0254, 'ft': 0.3048},
        'density': {'kg/m3': 1.0, 'g/cm3': 1000.0, 'lb/ft3': 16.0185},
        'viscosity': {'Pa-s': 1.0, 'cP': 0.001, 'P': 0.1}
    }

    @classmethod
    def to_si(cls, value, unit, category):
        """Converts a value from a given unit to its SI base."""
        if not unit or category not in cls.FACTORS:
            return float(value)
        
        factor = cls.FACTORS[category].get(unit, 1.0)
        return float(value) * factor