import pytest
from calculators.bernoulli import calculate_bernoulli


class TestBernoulli:

    def test_solve_for_v2(self):
        """
        Classic nozzle problem: water speeds up as pipe narrows.
        P1=200000, v1=1, z1=0, P2=100000, z2=0 → solve v2
        """
        result = calculate_bernoulli(
            p1=200000, v1=1, z1=0,
            p2=100000, v2=None, z2=0,
            density=1000
        )
        # v2 must be greater than v1 (pressure dropped, velocity increased)
        assert result["v2"] > result["v1"]

    def test_solve_for_p2(self):
        """If velocity increases, pressure must drop (Bernoulli's principle)."""
        result = calculate_bernoulli(
            p1=200000, v1=1, z1=0,
            p2=None, v2=5, z2=0,
            density=1000
        )
        assert result["p2"] < result["p1"]

    def test_energy_conservation(self):
        """
        Total energy (P + 0.5*rho*v^2 + rho*g*z) must be equal at both points.
        """
        result = calculate_bernoulli(
            p1=101325, v1=2, z1=5,
            p2=None, v2=4, z2=2,
            density=1000
        )
        g = 9.81
        rho = 1000
        e1 = result["p1"] + 0.5*rho*result["v1"]**2 + rho*g*result["z1"]
        e2 = result["p2"] + 0.5*rho*result["v2"]**2 + rho*g*result["z2"]
        assert abs(e1 - e2) < 1.0   # within 1 J/m³

    def test_same_elevation_higher_v_lower_p(self):
        """At same height, faster flow = lower pressure."""
        result = calculate_bernoulli(
            p1=300000, v1=1, z1=0,
            p2=None, v2=10, z2=0,
            density=1000
        )
        assert result["p2"] < result["p1"]

    def test_exactly_one_unknown_required(self):
        """Passing zero unknowns should raise a ValueError."""
        with pytest.raises(Exception):
            calculate_bernoulli(
                p1=100000, v1=2, z1=0,
                p2=80000, v2=4, z2=0,
                density=1000
            )

    def test_solve_for_elevation(self):
        """Solving for z2: higher pressure at lower speed implies higher elevation."""
        result = calculate_bernoulli(
            p1=200000, v1=3, z1=0,
            p2=200000, v2=1, z2=None,
            density=1000
        )
        # v decreased, so z must have increased (energy conservation)
        assert result["z2"] > result["z1"]