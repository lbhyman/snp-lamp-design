from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
sys.path.append('../snp-lamp-design')
from ga_optimizer import GAOptimizer
app = Flask(__name__)
CORS(app)
optimizer = GAOptimizer()
input = {}

# Update sequences, params, and population size when changed by user
def update_input(data):
    for key in data.keys():
        if data[key] != '':
            input[key] = data[key]

@app.route('/send_input', methods=['GET', 'POST'])
def send_input():
    # POST request
    if request.method == 'POST':
        data = request.get_json()
        update_input(data)
        print(input)
        return 'OK', 200
    
    # GET request
    else:
        return 'OK', 200

@app.route('/start_optimizer', methods=['GET', 'POST'])    
def start_optimizer():
    # POST request
    if request.method == 'POST':
        optimizer = GAOptimizer(input['WT'], input['SNP'], input['params'], input['pop_size'])
        optimizer.run()
        return 'OK', 200
    
    # GET request
    else:
        return 'OK', 200
    
@app.route('/stop_optimizer', methods=['GET', 'POST'])    
def stop_optimizer():
    # POST request
    if request.method == 'POST':
        optimizer.running = False
        return 'OK', 200
    
    # GET request
    else:
        return 'OK', 200
    
@app.route('/get_progress', methods=['GET', 'POST'])    
def get_progress():
    # POST request
    if request.method == 'POST':
        data = min(100.0 * float(optimizer.progress) / float(optimizer.predicted_nupack_calls), 100.0)
        return jsonify({'progress': int(data)}), 200
    
    # GET request
    else:
        data = min(100.0 * float(optimizer.progress) / float(optimizer.predicted_nupack_calls), 100.0)
        return jsonify({'progress': int(data)}), 200
 
@app.route('/get_output', methods=['GET', 'POST'])    
def get_output():
    # POST request
    if request.method == 'POST':
        data = optimizer.output
        return jsonify(data), 200
    
    # GET request
    else:
        data = optimizer.output
        return jsonify(data), 200
    
@app.route('/quit', methods=['GET', 'POST'])    
def quit():
    sys.exit(0)

if __name__ == '__main__':
    app.run(debug=True)