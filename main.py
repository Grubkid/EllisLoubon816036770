from flask import Flask, request, jsonify
import json

app = Flask(__name__)

global data

# read data from file and store in global variable data
with open('data.json') as f:
        data = json.load(f)

@app.route('/')
def hello_world():
    return 'Hello, World!' # return 'Hello World' in response

# route variables
@app.route('/students/<id>')
def get_student(id):
  for student in data: 
    if student['id'] == id: # filter out the students without the specified id
      return jsonify(student)


@app.route('/students')
def get_students():
    """Returns all students or filters them by meal preference."""
    pref = request.args.get('pref')

    if pref:
        filtered_students = [student for student in data if student.get('pref') == pref]
        if filtered_students:
            return jsonify(filtered_students)
        else:
            return jsonify({"message": f"No students found with preference '{pref}'"}), 404

    return jsonify(data)

@app.route('/stats')
def get_stats():
    """Returns a count of various meal preferences and programmes."""
    stats = {}

    for student in data:
        # Count meal preferences
        pref = student.get('pref')
        if pref:
            stats[pref] = stats.get(pref, 0) + 1

        # Count programmes
        programme = student.get('programme')
        if programme:
            stats[programme] = stats.get(programme, 0) + 1

    return jsonify(stats)

# Calculation
@app.route('/add/<int:a>/<int:b>')
def add(a, b):
    """Returns the sum of a and b."""
    return jsonify({"operation": "addition", "a": a, "b": b, "result": a + b})

@app.route('/subtract/<int:a>/<int:b>')
def subtract(a, b):
    """Returns the difference between a and b."""
    return jsonify({"operation": "subtraction", "a": a, "b": b, "result": a - b})

@app.route('/multiply/<int:a>/<int:b>')
def multiply(a, b):
    """Returns the product of a and b."""
    return jsonify({"operation": "multiplication", "a": a, "b": b, "result": a * b})

@app.route('/divide/<int:a>/<int:b>')
def divide(a, b):
    """Returns the result of dividing a by b (handles division by zero)."""
    if b == 0:
        return jsonify({"error": "Division by zero is not allowed"}), 400
    return jsonify({"operation": "division", "a": a, "b": b, "result": a / b})


app.run(host='0.0.0.0', port=8080)