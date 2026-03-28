import pytest
import math
from calculators.pipe_flow import calculate_pipe_flow, calculate_continuity, calculate_pump_power


class TestHagenPoiseuille:

    def test_flow_rate_positive(self):
        result = calculate_pipe_flow(
            density=1000, viscosity=0.001,
            diameter=0.01, pressure_drop=5000, length=10
        )
        assert result["flow_rate_m3_per_s"] > 0

    def test_flow_rate_increases_with_pressure(self):
        """Higher pressure drop → more flow."""
        low  = calculate_pipe_flow(1000, 0.001, 0.01, 1000, 10)
        high = calculate_pipe_flow(1000, 0.001, 0.01, 5000, 10)
        assert high["flow_rate_m3_per_s"] > low["flow_rate_m3_per_s"]

    def test_flow_rate_decreases_with_length(self):
        """Longer pipe → less flow at same pressure drop."""
        short = calculate_pipe_flow(1000, 0.001, 0.01, 5000, 5)
        long  = calculate_pipe_flow(1000, 0.001, 0.01, 5000, 50)
        assert long["flow_rate_m3_per_s"] < short["flow_rate_m3_per_s"]

    def test_d4_relationship(self):
        """
        Flow rate ∝ D^4.
        Doubling diameter → 16× the flow rate.
        """
        r1 = calculate_pipe_flow(1000, 0.001, 0.01, 5000, 10)
        r2 = calculate_pipe_flow(1000, 0.001, 0.02, 5000, 10)
        ratio = r2["flow_rate_m3_per_s"] / r1["flow_rate_m3_per_s"]
        assert abs(ratio - 16.0) < 0.1

    def test_lpm_conversion(self):
        """L/min value should be 60000 × m³/s."""
        result = calculate_pipe_flow(1000, 0.001, 0.01, 5000, 10)
        expected_lpm = result["flow_rate_m3_per_s"] * 60 * 1000
        assert abs(result["flow_rate_lpm"] - expected_lpm) < 0.001

    def test_laminar_warning_when_re_high(self):
        """If Re > 2100 the result should flag the assumption as invalid."""
        result = calculate_pipe_flow(
            density=1000, viscosity=0.001,
            diameter=0.05, pressure_drop=100000, length=1
        )
        if result["reynolds"] > 2100:
            assert result["laminar_assumption_valid"] is False


class TestContinuity:

    def test_flow_rate_conserved(self):
        """A1*v1 must equal A2*v2."""
        result = calculate_continuity(area1=0.01, velocity1=2, area2=0.005)
        assert abs(result["velocity2_m_per_s"] - 4.0) < 0.001

    def test_smaller_area_faster_velocity(self):
        result = calculate_continuity(area1=0.1, velocity1=1, area2=0.01)
        assert result["velocity2_m_per_s"] > 1.0


class TestPumpPower:

    def test_power_positive(self):
        result = calculate_pump_power(density=1000, flow_rate=0.01, head=20)
        assert result["shaft_power_w"] > 0

    def test_lower_efficiency_higher_shaft_power(self):
        """Less efficient pump needs more shaft power for same output."""
        r_good = calculate_pump_power(1000, 0.01, 20, efficiency=0.9)
        r_bad  = calculate_pump_power(1000, 0.01, 20, efficiency=0.5)
        assert r_bad["shaft_power_w"] > r_good["shaft_power_w"]

    def test_kw_conversion(self):
        result = calculate_pump_power(1000, 0.01, 20)
        assert abs(result["shaft_power_kw"] - result["shaft_power_w"] / 1000) < 0.0001