import pytest
from calculators.drag_buoyancy import calculate_drag, calculate_buoyancy, check_float_or_sink


class TestDragForce:

    def test_drag_positive(self):
        result = calculate_drag(density=1.2, velocity=10, area=0.5, drag_coefficient=0.47)
        assert result["drag_force_n"] > 0

    def test_drag_v_squared_relationship(self):
        """Drag ∝ v². Doubling velocity → 4× drag."""
        r1 = calculate_drag(1.2, velocity=10, area=0.5, drag_coefficient=0.47)
        r2 = calculate_drag(1.2, velocity=20, area=0.5, drag_coefficient=0.47)
        ratio = r2["drag_force_n"] / r1["drag_force_n"]
        assert abs(ratio - 4.0) < 0.01

    def test_drag_zero_velocity(self):
        """Zero velocity → zero drag."""
        result = calculate_drag(1000, 0, 1.0, 0.47)
        assert result["drag_force_n"] == 0.0

    def test_higher_cd_more_drag(self):
        """Cube (Cd≈1.05) has more drag than sphere (Cd≈0.47)."""
        sphere = calculate_drag(1.2, 20, 0.5, drag_coefficient=0.47)
        cube   = calculate_drag(1.2, 20, 0.5, drag_coefficient=1.05)
        assert cube["drag_force_n"] > sphere["drag_force_n"]

    def test_known_value(self):
        """
        F_D = 0.5 * 1.2 * 10^2 * 0.47 * 0.5 = 14.1 N
        """
        result = calculate_drag(density=1.2, velocity=10, area=0.5, drag_coefficient=0.47)
        assert abs(result["drag_force_n"] - 14.1) < 0.1


class TestBuoyancy:

    def test_buoyant_force_positive(self):
        result = calculate_buoyancy(fluid_density=1000, volume=0.001)
        assert result["buoyant_force_n"] > 0

    def test_archimedes_known_value(self):
        """F_B = 1000 * 9.81 * 0.001 = 9.81 N"""
        result = calculate_buoyancy(fluid_density=1000, volume=0.001)
        assert abs(result["buoyant_force_n"] - 9.81) < 0.01


class TestFloatOrSink:

    def test_light_object_floats(self):
        """Wood block (low density) should float in water."""
        result = check_float_or_sink(
            object_mass=0.5,       # 0.5 kg
            fluid_density=1000,
            volume=0.001           # 1 litre → would weigh 1 kg if water
        )
        assert result["verdict"] == "Floats"

    def test_heavy_object_sinks(self):
        """Steel block: very heavy for its volume."""
        result = check_float_or_sink(
            object_mass=10.0,
            fluid_density=1000,
            volume=0.001
        )
        assert result["verdict"] == "Sinks"

    def test_net_force_direction_floats(self):
        result = check_float_or_sink(0.5, 1000, 0.001)
        assert result["net_direction"] == "upward"

    def test_net_force_direction_sinks(self):
        result = check_float_or_sink(10.0, 1000, 0.001)
        assert result["net_direction"] == "downward"