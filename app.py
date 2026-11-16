import os
import ipaddress
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configuration by environment variables, with default values
APP_MESSAGE = os.environ.get("APP_MESSAGE", "Hello from subnet-app v1.0.1")
MAX_ADDRESSES = int(os.environ.get("MAX_ADDRESSES", "1024"))

@app.route("/")
def home():
    return jsonify(message=APP_MESSAGE,
                   usage="/subnet?cidr=192.168.1.0/28")

@app.route("/subnet")
def subnet():
    cidr = request.args.get("cidr")
    try:
        net = ipaddress.ip_network(cidr, strict=False)
    except (ValueError, TypeError):
        return jsonify(error="invalid CIDR, example: 192.168.1.0/28"), 400
    if net.num_addresses > MAX_ADDRESSES:
        return jsonify(error=f"subnet too big, max {MAX_ADDRESSES} addresses"), 400
    hosts = [str(h) for h in net.hosts()]
    return jsonify(network=str(net), netmask=str(net.netmask),
                   broadcast=str(net.broadcast_address),
                   total_hosts=len(hosts), hosts=hosts)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
