from flask import Blueprint, render_template

modl = Blueprint('modl', __name__, template_folder="templates")

@modl.route('/modl/')
def modlpage():
    return render_template("modl/modl.html")

