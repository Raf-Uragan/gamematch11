from flask import Flask, render_template, request

from services.matcher import get_form_options, match_games

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", options=get_form_options())


@app.route("/match", methods=["POST"])
def match():
    cpu = request.form.get("cpu", "")
    gpu = request.form.get("gpu", "")
    ram = request.form.get("ram", "")
    storage = request.form.get("storage", "ssd")

    if not all([cpu, gpu, ram]):
        return render_template(
            "index.html",
            options=get_form_options(),
            error="Заполните процессор, видеокарту и объём RAM.",
        ), 400

    profile, playable, blocked = match_games(cpu, gpu, ram, storage)
    return render_template(
        "results.html",
        profile=profile,
        playable=playable,
        blocked=blocked,
        form_data={"cpu": cpu, "gpu": gpu, "ram": ram, "storage": storage},
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
