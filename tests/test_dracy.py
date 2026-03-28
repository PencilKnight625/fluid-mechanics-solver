import pytest
from calculators.darcy import (
    friction_factor_laminar,
    friction_factor_turbulent,
    calculate_head_loss,
    calculate_darcy,
)


class TestFrictionFactor:

    def test_laminar_friction_factor_formula(self):
        """f_laminar = 64 / Re"""
        f = friction_factor_laminar(reynolds=1000)
        assert abs(f - 0.064) < 0.0001

    def test_laminar_friction_at_re_500(self):
        f = friction_factor_laminar(500)
        assert abs(f - 0.128) < 0.0001

    def test_turbulent_friction_factor_range(self):
        """Turbulent friction factor for steel pipe should be between 0.01 and 0.05."""
        f = friction_factor_turbulent(
            reynolds=100000, roughness=0.000046, diameter=0.05
        )
        assert 0.01 < f < 0.05

    def test_smoother_pipe_lower_friction(self):
        """PVC pipe (smoother) should have lower friction factor than steel."""
        f_steel = friction_factor_turbulent(100000, roughness=0.000046, diameter=0.05)
        f_pvc   = friction_factor_turbulent(100000, roughness=0.0000015, diameter=0.05)
        assert f_pvc < f_steel


class TestHeadLoss:

    def test_head_loss_increases_with_length(self):
        """Longer pipe → more head loss."""
        h_short = calculate_head_loss(friction_factor=0.02, length=10, diameter=0.05, velocity=2)
        h_long  = calculate_head_loss(friction_factor=0.02, length=100, diameter=0.05, velocity=2)
        assert h_long > h_short

    def test_head_loss_increases_with_velocity(self):
        """Higher velocity → more head loss (v² relationship)."""
        h_slow = calculate_head_loss(friction_factor=0.02, length=50, diameter=0.05, velocity=1)
        h_fast = calculate_head_loss(friction_factor=0.02, length=50, diameter=0.05, velocity=2)
        # v doubles → head loss quadruples
        assert abs(h_fast - 4 * h_slow) < 0.01

    def test_head_loss_known_value(self):
        """
        Manual check: f=0.02, L=100, D=0.05, v=2
        h_f = 0.02 * (100/0.05) * (4 / 19.62) = 0.02 * 2000 * 0.2039 ≈ 8.155 m
        """
        h = calculate_head_loss(
            friction_factor=0.02, length=100, diameter=0.05, velocity=2
        )
        assert abs(h - 8.155) < 0.05


class TestDarcyFull:

    def test_laminar_uses_laminar_formula(self):
        """When Re < 2000, friction factor should equal 64/Re."""
        result = calculate_darcy(
            density=1000, velocity=0.001, diameter=0.05,
            viscosity=0.001, pipe_length=10, roughness=0.000046
        )
        expected_f = 64 / result["reynolds"]
        assert abs(result["friction_factor"] - expected_f) < 0.0001
        assert result["flow_regime"] == "Laminar"

    def test_turbulent_regime_detected(self):
        result = calculate_darcy(
            density=1000, velocity=2, diameter=0.05,
            viscosity=0.001, pipe_length=100, roughness=0.000046
        )
        assert result["flow_regime"] == "Turbulent"

    def test_pressure_drop_positive(self):
        """Pressure drop should always be positive."""
        result = calculate_darcy(
            density=1000, velocity=1, diameter=0.05,
            viscosity=0.001, pipe_length=50, roughness=0.000046
        )
        assert result["pressure_drop_pa"] > 0

    def test_pressure_drop_equals_rho_g_h(self):
        """delta_P = rho * g * h_f should hold."""
        result = calculate_darcy(
            density=1000, velocity=1, diameter=0.05,
            viscosity=0.001, pipe_length=50, roughness=0.000046
        )
        expected_dp = 1000 * 9.81 * result["head_loss_m"]
        assert abs(result["pressure_drop_pa"] - expected_dp) < 1.0