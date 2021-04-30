from flask import Flask, jsonify, request
from flask_cors import CORS
import subprocess as sub
import json
import sys
import os

# Initial Setup
sys.path.append('../snp-lamp-design')
from ga_optimizer import GAOptimizer
app = Flask(__name__)
CORS(app)
optimizer = GAOptimizer()
running = False
finished = False
process = None
progress = 0.0
input = {'WT':'', 'SNP':'', 'params':{'temperature':21, 'sodium':0.065, 'magnesium': 0.008}, 'pop_size':128}
output = {}
try:
    os.remove('../data/log.txt')
except:
    pass
log = open('../data/log.txt', 'a')

# Update sequences, params, and population size when changed by user
def update_input(data):
    for key in data.keys():
        if data[key] != '':
            input[key] = data[key]
            
def check_progress(process):
    global progress, running, finished, output, log
    progress_list = [-1.0]
    try:
        input_log = open('../data/log.txt', 'r')
        data = input_log.readlines()
        if process is not None:
            if data is not None:
                for line in data:
                    if 'progress' in line:
                        progress_list.append(float(line.strip().split(' ')[1]))
                    if 'output' in line:
                        output = json.loads(line.strip()[6:])
                if progress_list[-1] > progress:
                    progress = progress_list[-1]
                if output != {}:
                    finished = True
                    running = False
                    process.kill()
                    log.close()
                    os.remove('../data/log.txt')
        input_log.close()
    except FileNotFoundError:
        return

@app.route('/send_input', methods=['GET', 'POST'])
def send_input():
    # POST request
    if request.method == 'POST':
        data = request.get_json()
        update_input(data)
        return 'OK', 200
    
    # GET request
    else:
        return 'OK', 200

@app.route('/start_optimizer', methods=['GET', 'POST'])    
def start_optimizer():
    global running, finished, process, progress, output, input, log
    log = open('../data/log.txt', 'a')
    output = {}
    progress = 0
    running = True
    finished = False
    # POST request
    if request.method == 'POST':
        running = True
        process = sub.Popen(['python3', '../snp-lamp-design/snp-lamp-design.py', input['WT'], input['SNP'], '-P', str(input['pop_size']),
                   '-T', str(input['params']['temperature']), '-s', str(input['params']['sodium']), '-m', str(input['params']['magnesium'])], 
                  stdout=log)
        #optimizer = GAOptimizer(input['WT'], input['SNP'], input['params'], input['pop_size'])
        #optimizer.run()
        return 'OK', 200
    
    # GET request
    else:
        return 'OK', 200
    
@app.route('/stop_optimizer', methods=['GET', 'POST'])    
def stop_optimizer():
    global running, finished, log, process
    # POST request
    if request.method == 'POST':
        process.kill()
        log.close()
        os.remove('../data/log.txt')
        running = False
        finished = False
        return 'OK', 200
    
    # GET request
    else:
        return 'OK', 200
    
@app.route('/get_progress', methods=['GET', 'POST'])    
def get_progress():
    global running, finished, process, output, progress
    # POST request
    if request.method == 'POST':
        check_progress(process)
        data = min(100.0 * float(progress), 100.0)
        return jsonify({'progress': int(data), 'running': running}), 200
    
    # GET request
    else:
        check_progress(process)
        data = min(100.0 * float(progress), 100.0)
        return jsonify({'progress': int(data), 'running': running}), 200
 
@app.route('/get_output', methods=['GET', 'POST'])    
def get_output():
    global running, finished, process, output, progress
    # POST request
    if request.method == 'POST':
        check_progress(process)
        return jsonify(output), 200
    
    # GET request
    else:
        check_progress(process)
        return jsonify(output), 200
    
@app.route('/quit', methods=['GET', 'POST'])    
def quit():
    sys.exit(0)

'''
if __name__ == '__main__':
    app.run(debug=True)'''