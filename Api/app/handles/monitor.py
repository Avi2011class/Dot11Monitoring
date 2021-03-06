import itertools
import random
import json
import functools
import operator

try:
    from ...app import app, db
    from ...app import graph_builder
    from ..models import Ap
except Exception:
    from app import app, db
    from app import graph_builder
    from app.models import Ap
from flask import render_template, flash, abort, request
from flask_login import login_required, current_user


@app.route("/monitor", methods=["GET"])
@login_required
def monitor():
    if not current_user.is_viewer:
        flash("You aren't viewer")
        abort(403)

    return render_template("monitor.html", seed=random.randint(1, 10000000), title="Monitor")


@app.route("/get_graph", methods=["GET"])
@login_required
def get_graph():
    if not current_user.is_viewer:
        return json.dumps({"status": "denied"})
    workspace = request.args.get("workspace")
    print(workspace)
    data = graph_builder.get(workspace=workspace)

    return json.dumps({"status": "ok", "data": data})


@app.route("/get_workspaces", methods=["GET"])
@login_required
def get_workspaces():
    if not current_user.is_viewer:
        return json.dumps({"status": "denied"})
    workspaces = db.session.query(Ap.workspace).distinct().order_by(Ap.workspace).all()
    workspaces = functools.reduce(operator.add, map(list, workspaces), [])
    return json.dumps({"status": "ok", "data": workspaces})
