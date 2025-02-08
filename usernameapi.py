from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/user-name")
def user_name():
    # Retrieve the X-MS-CLIENT-PRINCIPAL-NAME header
    principal_name = request.headers.get("X-MS-CLIENT-PRINCIPAL-NAME")
    if principal_name:
        return jsonify({"principal_name": principal_name})
    else:
        return jsonify({"error": "X-MS-CLIENT-PRINCIPAL-NAME header not found"}), 404

if __name__ == "__main__":
    # When running locally, use a debug port.
    app.run(host="0.0.0.0", port=5000)
