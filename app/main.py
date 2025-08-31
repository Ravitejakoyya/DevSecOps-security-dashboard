import os
import subprocess
from flask import Flask, request

app = Flask(__name__)

@app.route("/run", methods=["POST"])
def run():
    cmd = request.json.get("cmd")
    output = subprocess.check_output(cmd, shell=True)
    return {"output": output.decode()}

if __name__ == "__main__":
    app.run(debug=True)
