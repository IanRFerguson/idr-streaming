import os
import time

from flask import Flask, make_response, redirect, render_template, url_for

from utilities.logger import logger
from utilities.mapping import rebuild_map

#####

api = Flask(__name__)
api.logger = logger

# Disable template caching for development
api.config["TEMPLATES_AUTO_RELOAD"] = True
api.jinja_env.auto_reload = True


@api.route("/")
def index():
    if not os.path.exists(os.path.join(api.template_folder, "index.html")):
        return redirect("/refresh")

    return render_template("index.html")


@api.route("/refresh")
def refresh():
    logger.info("Rebuilding the map...")
    OUTPUT_PATH = os.path.join(api.template_folder, "index.html")
    rebuild_map(output_path=OUTPUT_PATH)
    logger.info("Map rebuilt successfully")

    return redirect(url_for("index"))
