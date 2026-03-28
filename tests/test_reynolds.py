import pytest
from calculators.reynolds import calculate_reynolds


class TestReynoldsNumber:

    def test_laminar_flow_classification(self):
        re, flow_type = calculate_reynolds(
            density=1000, velocity=0.01, diameter=0.05, viscosity=0.001
        )
        assert flow_type == "Laminar"
        assert re < 2000

    def test_turbulent_flow_classification(self):
        re, flow_type = calculate_reynolds(
            density=1000, velocity=2.0, diameter=0.05, viscosity=0.001
        )
        assert flow_type == "Turbulent"
        assert re > 4000

    def test_transitional_flow_classification(self):
        re, flow_type = calculate_reynolds(
            density=1000, velocity=0.06, diameter=0.05, viscosity=0.001
        )
        assert flow_type == "Transitional"
        assert 2000 <= re <= 4000

    def test_known_value_water(self):
        re, flow_type = calculate_reynolds(
            density=998, velocity=1.0, diameter=0.05, viscosity=0.001002
        )
        assert abs(re - 49800.4) < 1.0
        assert flow_type == "Turbulent"

    def test_formula_correctness(self):
        density, velocity, diameter, viscosity = 800, 3.0, 0.1, 0.002
        expected_re = (density * velocity * diameter) / viscosity
        re, _ = calculate_reynolds(density, velocity, diameter, viscosity)
        assert abs(re - expected_re) < 0.01

    def test_result_is_rounded(self):
        re, _ = calculate_reynolds(
            density=999, velocity=1.337, diameter=0.049, viscosity=0.001001
        )
        assert isinstance(re, float)
        assert len(str(re).split(".")[-1]) <= 4

    def test_zero_velocity(self):
        re, flow_type = calculate_reynolds(
            density=1000, velocity=0.0, diameter=0.05, viscosity=0.001
        )
        assert re == 0.0
        assert flow_type == "Laminar"

    def test_boundary_exactly_2000(self):
        re, flow_type = calculate_reynolds(
            density=1000, velocity=0.02, diameter=0.1, viscosity=0.001
        )
        assert re == 2000.0
        assert flow_type == "Transitional"

    def test_high_reynolds_number(self):
        re, flow_type = calculate_reynolds(
            density=1.2, velocity=50, diameter=1.0, viscosity=0.0000181
        )
        assert re > 1_000_000
        assert flow_type == "Turbulent"