from flask import Flask
app = Flask(__name__)
import app_api.config as config
app.config["SQLALCHEMY_DATABASE_URI"] = config.msSqlConn

import app_api.modelsSQL as modelsSQL
from .api import init_app
from .commands import init_app as init_commands
modelsSQL.init(app)
init_app(app)
init_commands(app)

@app.route("/")
def hello():
    peliculas = modelsSQL.Pelicula.query.all()
    return str(peliculas)

if __name__ == "__main__":
    app.run(debug=True)