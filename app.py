from flask import Flask, request, jsonify
from db import Database as db

# Init app
app = Flask(__name__)

# Init db
db.init()


@app.route('/sort/selection', methods=['POST'])
def selection_sort():
    file = request.files['file']
    column = int(request.form.get("column"))
    order = request.form.get('order')


if __name__ == "__main__":
    app.run(debug=True)
