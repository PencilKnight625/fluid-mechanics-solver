def calculate_bernoulli(p1, v1, z1, p2, v2, z2, density):
    """
    Bernoulli's equation: P1 + 0.5*rho*v1^2 + rho*g*z1 = P2 + 0.5*rho*v2^2 + rho*g*z2

    Leave exactly ONE of the six variables as None — that is the unknown to solve.

    p1, p2: pressure in Pa
    v1, v2: velocity in m/s
    z1, z2: elevation in m
    density: fluid density in kg/m³
    """
    g = 9.81

    unknowns = [x for x in [p1, v1, z1, p2, v2, z2] if x is None]
    if len(unknowns) != 1:
        raise ValueError(
            f"Exactly one variable must be None (unknown). "
            f"You provided {len(unknowns)} unknowns."
        )

    def bernoulli_lhs(p, v, z):
        return p + 0.5 * density * v**2 + density * g * z

    if p1 is None:
        rhs = bernoulli_lhs(p2, v2, z2)
        p1 = rhs - 0.5 * density * v1**2 - density * g * z1
    elif v1 is None:
        rhs = bernoulli_lhs(p2, v2, z2)
        ke1 = rhs - p1 - density * g * z1
        if ke1 < 0:
            raise ValueError("No real solution: energy at point 1 is insufficient.")
        v1 = (2 * ke1 / density) ** 0.5
    elif z1 is None:
        rhs = bernoulli_lhs(p2, v2, z2)
        pe1 = rhs - p1 - 0.5 * density * v1**2
        z1 = pe1 / (density * g)
    elif p2 is None:
        lhs = bernoulli_lhs(p1, v1, z1)
        p2 = lhs - 0.5 * density * v2**2 - density * g * z2
    elif v2 is None:
        lhs = bernoulli_lhs(p1, v1, z1)
        ke2 = lhs - p2 - density * g * z2
        if ke2 < 0:
            raise ValueError("No real solution: energy at point 2 is insufficient.")
        v2 = (2 * ke2 / density) ** 0.5
    elif z2 is None:
        lhs = bernoulli_lhs(p1, v1, z1)
        pe2 = lhs - p2 - 0.5 * density * v2**2
        z2 = pe2 / (density * g)

    total_energy = bernoulli_lhs(p1, v1, z1)

    return {
        "p1": round(p1, 2),
        "v1": round(v1, 4),
        "z1": round(z1, 4),
        "p2": round(p2, 2),
        "v2": round(v2, 4),
        "z2": round(z2, 4),
        "total_energy_j_per_m3": round(total_energy, 2),
        "pressure_head_1_m": round(p1 / (density * 9.81), 4),
        "velocity_head_1_m": round(v1**2 / (2 * 9.81), 4),
        "pressure_head_2_m": round(p2 / (density * 9.81), 4),
        "velocity_head_2_m": round(v2**2 / (2 * 9.81), 4),
    }