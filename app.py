import os
import json
import subprocess
import threading
from datetime import datetime
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# Determine the appropriate directory based on the environment
REPORTS_DIR = os.path.join(os.environ.get('HOME', '/home'), 'site', 'wwwroot', 'test_reports')
os.makedirs(REPORTS_DIR, exist_ok=True)

is_running = False
running_tests_process = None
CURRENT_MODE = 'demo'  # Default mode
run_type = ""
progress = {
    "running": False,
    "progress": 0,
    "log": ""
}

tests = [
    {"name": "test_ActionByUserRole", "path": r"C:\Users\Administrator\Automation\Tests\test_ActionByUserRole.py"},
    # Add other test definitions here...
    {"name": "run_full_regression", "path": r"C:\Users\Administrator\Automation\Tests"}
]

@app.route('/tests.html')
def tests_page():
    return render_template('tests.html')

@app.route('/progress.html')
def progress_page():
    return render_template('progress.html')

@app.route('/')
def index():
    return render_template('tests.html')

@app.route('/data')
def get_data():
    data_files = [f for f in os.listdir(REPORTS_DIR) if f.endswith('.json')]
    datasets = []
    for file in data_files:
        with open(os.path.join(REPORTS_DIR, file), 'r') as f:
            data = json.load(f)
            datasets.append(data)
    return jsonify(datasets)

@app.route('/kill_tests', methods=['POST'])
def kill_tests():
    global is_running, running_tests_process
    if not is_running:
        return jsonify({"error": "No tests are currently running"}), 400

    if running_tests_process:
        running_tests_process.terminate()
        running_tests_process = None

    is_running = False
    progress["log"] += f"\nProcess killed in {CURRENT_MODE} mode."
    return jsonify({"message": "Running tests were successfully killed"}), 200

@app.route('/progress')
def get_progress():
    return jsonify(progress)

@app.route('/set_mode/<mode>', methods=['POST'])
def set_mode(mode):
    global CURRENT_MODE
    CURRENT_MODE = mode
    print(f'Setting mode to {mode}')
    return jsonify(success=True, mode=mode)

@app.route('/run_test/<test_name>', methods=['POST'])
def run_test(test_name):
    try:
        global run_type
        global CURRENT_MODE
        mode = CURRENT_MODE  # Use the current mode

        test = next((t for t in tests if t['name'] == test_name), None)
        if not test:
            return jsonify(success=False, error="Test not found"), 404

        test_path = test['path']
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        report_file = os.path.join(REPORTS_DIR, f'{test_name}_report_{timestamp}.json')

        # Run pytest with JSON report generation
        result = subprocess.run(['pytest', test_path, '--json-report', f'--json-report-file={report_file}', f'--base-url={mode}'],
                                capture_output=True, text=True)
        success = result.returncode == 0

        # Read the generated report
        with open(report_file, 'r') as f:
            report_content = json.load(f)
        return jsonify(success=success, output=result.stdout, report=report_content)

    except Exception as e:
        return jsonify(success=False, error=str(e))

@app.route('/run_full_api', methods=['POST'])
def run_full_api():
    try:
        global progress
        progress["running"] = True
        progress["progress"] = 0
        progress["log"] = ""

        # Collecting all test paths for full API test
        test_paths = [test['path'] for test in tests if test['name'] == "api"]

        threading.Thread(target=run_api_tests, args=(test_paths, 'regression', "Ofakimdb_Copy")).start()
        return jsonify(success=True)

    except Exception as e:
        return jsonify(success=False, error=str(e))

@app.route('/run_max_api', methods=['POST'])
def run_max_api():
    try:
        global progress
        progress["running"] = True
        progress["progress"] = 0
        progress["log"] = ""

        # Collecting all test paths for max API test
        test_paths = [test['path'] for test in tests if test['name'] == "max"]

        threading.Thread(target=run_api_tests, args=(test_paths, 'max', 'Ofakimdb_Copy')).start()
        return jsonify(success=True)

    except Exception as e:
        return jsonify(success=False, error=str(e))

@app.route('/run_full_regression', methods=['POST'])
def run_full_regression():
    try:
        global progress
        global is_running, running_tests_process
        if is_running:
            return jsonify({"error": "Tests are already running"}), 400

        is_running = True
        progress["running"] = True
        progress["progress"] = 0
        progress["log"] = ""
        global run_type
        global CURRENT_MODE
        mode = CURRENT_MODE  # Use the current mode

        if mode == "qa":
            run_type = "qa"
            db_conection = "Ofakimdb"
        else:
            run_type = "regression"
            db_conection = "Ofakimdb_Copy"

        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        report_file = os.path.join(REPORTS_DIR, f"run_full_regression_report_{timestamp}.json")

        # Collecting all test paths for full regression
        test_paths = [test['path'] for test in tests if test['name'] == "run_full_regression"]

        # Run pytest with JSON report generation
        threading.Thread(target=run_tests, args=(test_paths, mode, db_conection, report_file, run_type)).start()
        return jsonify(success=True)

    except Exception as e:
        return jsonify(success=False, error=str(e))

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=TRUE)
