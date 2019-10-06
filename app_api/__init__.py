from flask import Flask
app = Flask(__name__)
import app_api.config as config
app.config["SQLALCHEMY_DATABASE_URI"] = config.msSqlConn
app.config["SQLALCHEMY_BINDS"] = {
    'mySQL':config.mySqlConn
} 

import app_api.modelsMSSQL as modelsMSSQL
import app_api.modelsMySQL as modelsMySQL
from .api import init_app
from .commands import init_app as init_commands
modelsMSSQL.init(app) # Init MS SQL
modelsMySQL.init(app) # Init My SQL
init_app(app) # Init API
init_commands(app) # Init flask commands

@app.route("/heartbeat")
def home():
    return "alive"

if __name__ == "__main__":
    app.run(debug=True)