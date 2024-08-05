import argparse
import re
from flask import Flask, jsonify, request, send_from_directory, render_template
import subprocess
import os
import json
from datetime import datetime
import threading

app = Flask(__name__)

# Directory to store test reports
REPORTS_DIR = r'C:\Users\Administrator\Automation\Tests\test_reports'
is_running = False
running_tests_process = None
os.makedirs(REPORTS_DIR, exist_ok=True)

tests = [
    {"name": "test_ActionByUserRole", "path": r"C:\Users\Administrator\Automation\Tests\test_ActionByUserRole.py"},
    {"name": "test_AddBeneficiaries", "path": r"C:\Users\Administrator\Automation\Tests\test_AddBeneficiaries.py"},
    {"name": "test_AddMoney", "path": r"C:\Users\Administrator\Automation\Tests\test_AddMoney.py"},
    {"name": "test_AddPayment", "path": r"C:\Users\Administrator\Automation\Tests\test_AddPayment.py"},
    {"name": "test_AddPaymentFromDeshboard", "path": r"C:\Users\Administrator\Automation\Tests\test_AddPaymentFromDeshboard.py"},
    {"name": "test_ConvertFromDashboard", "path": r"C:\Users\Administrator\Automation\Tests\test_ConvertFromDashboard.py"},
    {"name": "test_hit", "path": r"C:\Users\Administrator\Automation\Tests\test_hit.py"},
    {"name": "test_mass_our_type_cost", "path": r"C:\Users\Administrator\Automation\Tests\test_mass_our_type_cost.py"},
    {"name": "test_mass_payment", "path": r"C:\Users\Administrator\Automation\Tests\test_mass_payment.py"},
    {"name": "max", "path": r"C:\Users\Administrator\Automation\Tests"},
    {"name": "test_payment_our_fee", "path": r"C:\Users\Administrator\Automation\Tests\test_payment_our_fee.py"},
    {"name": "test_TravelCash", "path": r"C:\Users\Administrator\Automation\Tests\test_TravelCash.py"},
    {"name": "test_Edit_beneficiary", "path": r"C:\Users\Administrator\Automation\Tests\test_Edit_beneficiary.py"},
    {"name": "test_LockUpFromDashboard", "path": r"C:\Users\Administrator\Automation\Tests\test_LockUpFromDashboard.py"},
    {"name": "api", "path": r"C:\Users\Administrator\Automation\Okoora_Api"},
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
    global is_running, running_tests_process, progress, CURRENT_MODE
    if not is_running:
        return jsonify({"error": "No tests are currently running"}), 400

    if running_tests_process:
        running_tests_process.terminate()
        running_tests_process = None

    is_running = False
    progress["log"] += f"\nProcess killed in {CURRENT_MODE} mode."
    return jsonify({"message": "Running tests were successfully killed"}), 200

CURRENT_MODE = 'demo'  # Default mode
run_type = ""
progress = {
    "running": False,
    "progress": 0,
    "log": ""
}

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

        if test_name == "api":
            test_path = next(test['path'] for test in tests if test['name'] == test_name)
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

        if test_name == "test_ActionByUserRole":
            test_path = next(test['path'] for test in tests if test['name'] == test_name)
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            report_file = os.path.join(REPORTS_DIR, f'{test_name}_report_{timestamp}.json')

            # Run pytest with JSON report generation
            result = subprocess.run(['pytest', test_path, '--json-report', f'--base-url=demo', f'--json-report-file={report_file}'],
                                    capture_output=True, text=True)
            success = result.returncode == 0

            # Read the generated report
            with open(report_file, 'r') as f:
                report_content = json.load(f)
            return jsonify(success=success, output=result.stdout, report=report_content)

        else:
            if mode == "qa":
                db_conection = "Ofakimdb"
            else:
                db_conection = "Ofakimdb_Copy"
            test_path = next(test['path'] for test in tests if test['name'] == test_name)
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            report_file = os.path.join(REPORTS_DIR, f'{test_name}_report_{timestamp}.json')

            # Run pytest with JSON report generation
            result = subprocess.run(['pytest', test_path, '--json-report', f'--base-url={mode}', f'--db-name={db_conection}', f'--json-report-file={report_file}'],
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

        # Collecting all test paths for full API test
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

def run_tests(test_paths, mode, db_connection, report_file, run_type):
    global progress, is_running, running_tests_process
    progress["running"] = True
    progress["progress"] = 0
    progress["log"] = ""

    # Get the total number of tests
    test_count_result = subprocess.run(
        ['pytest', '--collect-only'] + test_paths,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    total_tests = len(re.findall(r'<Function ', test_count_result.stdout))
    if total_tests == 0:
        progress["running"] = False
        progress["progress"] = 100
        progress["log"] = "No tests found."
        is_running = False
        return

    running_tests_process = subprocess.Popen(
        ['pytest'] + test_paths + [f'-m {run_type}', '-v', f'--base-url={mode}', f'--db-name={db_connection}', f'--json-report-file={report_file}'],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )

    completed_tests = 0
    for line in iter(running_tests_process.stdout.readline, ''):
        progress["log"] += line
        match = re.search(r'\[\s*(\d+)%\]', line)
        if match:
            percentage = int(match.group(1))
            completed_tests = (percentage * total_tests) // 100
            progress["progress"] = percentage
        print(line, end='')

    running_tests_process.wait()
    progress["running"] = False
    progress["progress"] = 100
    is_running = False

    with open(report_file, 'r') as f:
        report_content = json.load(f)

def run_api_tests(test_paths, mark, db_env=None):
    global progress, is_running, running_tests_process
    progress["running"] = True
    progress["progress"] = 0
    progress["log"] = ""

    # Get the total number of tests
    test_count_result = subprocess.run(
        ['pytest', '--collect-only'] + test_paths,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    total_tests = len(re.findall(r'<Function ', test_count_result.stdout))
    if total_tests == 0:
        progress["running"] = False
        progress["progress"] = 100
        progress["log"] = "No tests found."
        is_running = False
        return

    running_tests_process = subprocess.Popen(
        ['pytest'] + test_paths + ['-v', f'-m {mark}', f'--db-name={db_env}'],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )

    completed_tests = 0
    for line in iter(running_tests_process.stdout.readline, ''):
        progress["log"] += line
        match = re.search(r'\[\s*(\d+)%\]', line)
        if match:
            percentage = int(match.group(1))
            completed_tests = (percentage * total_tests) // 100
            progress["progress"] = percentage
        print(line, end='')

    running_tests_process.wait()
    progress["running"] = False
    progress["progress"] = 100
    is_running = False

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

def parse_arguments():
    parser = argparse.ArgumentParser(description="Run pytest with a specified mode.")
    parser.add_argument('mode', type=str, help="Mode to run the tests (e.g., 'qa' or 'default')")
    parser.add_argument('test_name', type=str, help="Name of the test to run")
    return parser.parse_args()

if __name__ == '__main__':
    app.run(debug=True)
