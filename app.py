from flask import Flask, render_template, request, session, jsonify
from calculators.reynolds import calculate_reynolds
from calculators.darcy import calculate_darcy
from calculators.bernoulli import calculate_bernoulli
from calculators.pipe_flow import calculate_pipe_flow, calculate_continuity, calculate_pump_power
from calculators.open_channel import calculate_rectangular_channel
from calculators.drag_buoyancy import calculate_drag, check_float_or_sink

app = Flask(__name__)
app.secret_key = "fluid_solver_secret_2024"

# Helpers
def get_float(form, key):
    """Safely parse a float from form data. Returns None if missing or blank."""
    val = form.get(key, "").strip()
    if val == "" or val == "None":
        return None
    return float(val)


def init_history():
    if "history" not in session:
        session["history"] = []


def add_history(calc_type, inputs, result):
    init_history()
    session["history"].insert(0, {
        "type": calc_type,
        "inputs": inputs,
        "result": result,
    })
    session["history"] = session["history"][:10]
    session.modified = True


# Routes

@app.route("/")
def index():
    init_history()
    return render_template("index.html", history=session["history"])


@app.route("/calculate/reynolds", methods=["POST"])
def route_reynolds():
    try:
        density   = get_float(request.form, "density")
        velocity  = get_float(request.form, "velocity")
        diameter  = get_float(request.form, "diameter")
        viscosity = get_float(request.form, "viscosity")

        if any(v is None or v <= 0 for v in [density, velocity, diameter, viscosity]):
            return render_template("index.html",
                                   active_tab="reynolds",
                                   error="All values must be positive numbers.",
                                   history=session.get("history", []))

        reynolds, flow_type = calculate_reynolds(density, velocity, diameter, viscosity)
        result = {"reynolds": reynolds, "flow_type": flow_type,
                  "density": density, "velocity": velocity,
                  "diameter": diameter, "viscosity": viscosity}

        add_history("Reynolds Number", result, result)
        return render_template("index.html", active_tab="reynolds",
                               reynolds_result=result,
                               history=session["history"])
    except Exception as e:
        return render_template("index.html", active_tab="reynolds",
                               error=str(e), history=session.get("history", []))


@app.route("/calculate/darcy", methods=["POST"])
def route_darcy():
    try:
        density    = get_float(request.form, "density")
        velocity   = get_float(request.form, "velocity")
        diameter   = get_float(request.form, "diameter")
        viscosity  = get_float(request.form, "viscosity")
        length     = get_float(request.form, "pipe_length")
        roughness  = get_float(request.form, "roughness")

        if any(v is None or v <= 0 for v in [density, velocity, diameter, viscosity, length, roughness]):
            return render_template("index.html", active_tab="darcy",
                                   error="All values must be positive numbers.",
                                   history=session.get("history", []))

        result = calculate_darcy(density, velocity, diameter, viscosity, length, roughness)
        add_history("Darcy-Weisbach", {"density": density, "velocity": velocity,
                                        "diameter": diameter, "length": length}, result)
        return render_template("index.html", active_tab="darcy",
                               darcy_result=result, history=session["history"])
    except Exception as e:
        return render_template("index.html", active_tab="darcy",
                               error=str(e), history=session.get("history", []))


@app.route("/calculate/bernoulli", methods=["POST"])
def route_bernoulli():
    try:
        density = get_float(request.form, "density")
        p1 = get_float(request.form, "p1")
        v1 = get_float(request.form, "v1")
        z1 = get_float(request.form, "z1")
        p2 = get_float(request.form, "p2")
        v2 = get_float(request.form, "v2")
        z2 = get_float(request.form, "z2")

        # Count how many are None — exactly one must be unknown
        unknowns = [x for x in [p1, v1, z1, p2, v2, z2] if x is None]
        if len(unknowns) != 1:
            return render_template("index.html", active_tab="bernoulli",
                                   error="Leave exactly ONE field blank — that is the unknown to solve for.",
                                   history=session.get("history", []))
        if density is None or density <= 0:
            return render_template("index.html", active_tab="bernoulli",
                                   error="Density is required and must be positive.",
                                   history=session.get("history", []))

        result = calculate_bernoulli(p1, v1, z1, p2, v2, z2, density)
        add_history("Bernoulli", {"density": density}, result)
        return render_template("index.html", active_tab="bernoulli",
                               bernoulli_result=result, history=session["history"])
    except Exception as e:
        return render_template("index.html", active_tab="bernoulli",
                               error=str(e), history=session.get("history", []))


@app.route("/calculate/pipeflow", methods=["POST"])
def route_pipeflow():
    try:
        density       = get_float(request.form, "density")
        viscosity     = get_float(request.form, "viscosity")
        diameter      = get_float(request.form, "diameter")
        pressure_drop = get_float(request.form, "pressure_drop")
        length        = get_float(request.form, "length")

        if any(v is None or v <= 0 for v in [density, viscosity, diameter, pressure_drop, length]):
            return render_template("index.html", active_tab="pipeflow",
                                   error="All values must be positive numbers.",
                                   history=session.get("history", []))

        result = calculate_pipe_flow(density, viscosity, diameter, pressure_drop, length)
        add_history("Pipe Flow (Hagen-Poiseuille)", {}, result)
        return render_template("index.html", active_tab="pipeflow",
                               pipeflow_result=result, history=session["history"])
    except Exception as e:
        return render_template("index.html", active_tab="pipeflow",
                               error=str(e), history=session.get("history", []))


@app.route("/calculate/openchannel", methods=["POST"])
def route_openchannel():
    try:
        width    = get_float(request.form, "width")
        depth    = get_float(request.form, "depth")
        manning_n = get_float(request.form, "manning_n")
        slope    = get_float(request.form, "slope")

        if any(v is None or v <= 0 for v in [width, depth, manning_n, slope]):
            return render_template("index.html", active_tab="openchannel",
                                   error="All values must be positive numbers.",
                                   history=session.get("history", []))

        result = calculate_rectangular_channel(width, depth, manning_n, slope)
        add_history("Manning's (Open Channel)", {"width": width, "depth": depth}, result)
        return render_template("index.html", active_tab="openchannel",
                               openchannel_result=result, history=session["history"])
    except Exception as e:
        return render_template("index.html", active_tab="openchannel",
                               error=str(e), history=session.get("history", []))


@app.route("/calculate/drag", methods=["POST"])
def route_drag():
    try:
        fluid_density   = get_float(request.form, "fluid_density")
        velocity        = get_float(request.form, "velocity")
        area            = get_float(request.form, "area")
        drag_coeff      = get_float(request.form, "drag_coeff")
        object_mass     = get_float(request.form, "object_mass")
        object_volume   = get_float(request.form, "object_volume")

        if any(v is None or v <= 0 for v in [fluid_density, velocity, area, drag_coeff]):
            return render_template("index.html", active_tab="drag",
                                   error="Fluid density, velocity, area and drag coefficient are required.",
                                   history=session.get("history", []))

        drag_result = calculate_drag(fluid_density, velocity, area, drag_coeff)
        buoyancy_result = None

        if object_mass is not None and object_volume is not None and object_mass > 0 and object_volume > 0:
            buoyancy_result = check_float_or_sink(object_mass, fluid_density, object_volume)

        add_history("Drag & Buoyancy", {}, drag_result)
        return render_template("index.html", active_tab="drag",
                               drag_result=drag_result,
                               buoyancy_result=buoyancy_result,
                               history=session["history"])
    except Exception as e:
        return render_template("index.html", active_tab="drag",
                               error=str(e), history=session.get("history", []))


@app.route("/clear_history", methods=["POST"])
def clear_history():
    session["history"] = []
    return render_template("index.html", history=[])


# REST API endpoints

@app.route("/api/reynolds", methods=["POST"])
def api_reynolds():
    """
    JSON API endpoint.
    POST body: { "density": 1000, "velocity": 2, "diameter": 0.05, "viscosity": 0.001 }
    """
    data = request.get_json()
    try:
        reynolds, flow_type = calculate_reynolds(
            data["density"], data["velocity"], data["diameter"], data["viscosity"]
        )
        return jsonify({"reynolds": reynolds, "flow_type": flow_type})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)