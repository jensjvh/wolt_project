from flask import Flask, jsonify, request
app = Flask(__name__)

@app.route('/', methods=['POST'])
def main():
    values = request.get_json()
    return str(values["cart_value"])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)