import pytest
from calculators.open_channel import calculate_manning, calculate_rectangular_channel


class TestManning:

    def test_flow_rate_positive(self):
        result = calculate_rectangular_channel(
            width=2.0, depth=0.8, Manning_n=0.013, slope=0.001
        )
        assert result["flow_rate_m3_per_s"] > 0

    def test_steeper_slope_more_flow(self):
        """Steeper slope → faster flow → more discharge."""
        gentle = calculate_rectangular_channel(2.0, 0.8, 0.013, 0.0005)
        steep  = calculate_rectangular_channel(2.0, 0.8, 0.013, 0.005)
        assert steep["flow_rate_m3_per_s"] > gentle["flow_rate_m3_per_s"]

    def test_wider_channel_more_flow(self):
        narrow = calculate_rectangular_channel(1.0, 0.8, 0.013, 0.001)
        wide   = calculate_rectangular_channel(4.0, 0.8, 0.013, 0.001)
        assert wide["flow_rate_m3_per_s"] > narrow["flow_rate_m3_per_s"]

    def test_rougher_channel_less_flow(self):
        """Higher Manning's n (rougher) → slower flow."""
        smooth = calculate_rectangular_channel(2.0, 0.8, 0.009, 0.001)
        rough  = calculate_rectangular_channel(2.0, 0.8, 0.035, 0.001)
        assert rough["flow_rate_m3_per_s"] < smooth["flow_rate_m3_per_s"]

    def test_hydraulic_radius_formula(self):
        """R = A / P = (w*d) / (w + 2d)"""
        result = calculate_rectangular_channel(2.0, 0.5, 0.013, 0.001)
        expected_r = (2.0 * 0.5) / (2.0 + 2 * 0.5)
        assert abs(result["hydraulic_radius_m"] - expected_r) < 0.0001

    def test_area_and_perimeter_correct(self):
        result = calculate_rectangular_channel(3.0, 1.0, 0.013, 0.001)
        assert abs(result["area_m2"] - 3.0) < 0.0001
        assert abs(result["wetted_perimeter_m"] - 5.0) < 0.0001