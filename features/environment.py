import os
import json
from datetime import datetime
from selenium import webdriver


def before_all(context):
    """Setup necessary directories and files for reporting."""
    context.read_json = read_json
    if not os.path.exists('reports'):
        os.makedirs('reports')
    if not os.path.exists('reports/screenshots'):
        os.makedirs('reports/screenshots')

    # Create the styled HTML report file (but do not add the feature name yet)
    context.report_path = 'reports/test_report.html'
    with open(context.report_path, 'w') as report_file:
        report_file.write("""<html><head><title>Test Report</title><style>
            body { font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px; }
            h1 { text-align: center; color: #333; }
            h2 { text-align: center; color: #333; font-size: 24px; }
            table { width: 100%; border-collapse: collapse; background: white; box-shadow: 0px 0px 10px #ccc; }
            th, td { padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }
            th { background-color: #333; color: white; }
            tr:hover { background-color: #f1f1f1; }
            .passed { color: green; font-weight: bold; }
            .failed { color: red; font-weight: bold; }
            .expandable { cursor: pointer; background: #e0e0e0; padding: 8px; font-weight: bold; }
            .scenario-steps { display: none; }
        </style><script>
            function toggleScenario(id) {
                var rows = document.querySelectorAll(`#${id}`);
                rows.forEach(function(row) {
                    row.style.display = row.style.display === 'table-row' ? 'none' : 'table-row';
                });
            }
        </script></head><body><h1>Automation Test Report</h1><table>
            <tr><th onclick="toggleScenario('steps-all')">Scenario</th><th>Status</th><th>Screenshot</th></tr>
        """)


def before_feature(context, feature):
    """Setup before each feature."""
    if 'feature_written' not in context:  # Check if feature has already been written
        context.feature_written = True  # Set the flag indicating that the feature is written
        feature_name = context.feature.name  # Extract the feature name
        with open(context.report_path, 'a') as report_file:
            report_file.write(f"<h2>Feature: {feature_name}</h2>")  # Write feature once


def before_scenario(context, scenario):
    """Setup WebDriver before every scenario and write feature name once."""

    # Proceed with the driver initialization and rest of the code
    config = context.read_json('features/config.json')
    browser = config.get("browser", "chrome").lower()

    if browser == "chrome":
        context.driver = webdriver.Chrome(executable_path="drivers/chromedriver.exe")
    elif browser == "firefox":
        context.driver = webdriver.Firefox(executable_path="drivers/geckodriver.exe")
    else:
        raise ValueError(f"Browser '{browser}' is not supported.")

    context.driver.maximize_window()

    # Continue with scenario-specific setup
    print(f"🚀 Browser opened for scenario: {scenario.name}")
    # Add scenario row to the report
    with open(context.report_path, 'a') as report_file:
        report_file.write(f"""
        <tr class="expandable" onclick="toggleScenario('steps-{scenario.name.replace(' ', '_')}')">
            <td colspan="3">{scenario.name}</td>
        </tr>
        <tbody id="steps-{scenario.name.replace(' ', '_')}" class="scenario-steps">
        """)


def after_step(context, step):
    """Log step result, take a screenshot, and write to the HTML report."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_name = f"{step.name.replace(' ', '_')}_{timestamp}.png"
    screenshot_path = f"reports/screenshots/{screenshot_name}"
    context.driver.save_screenshot(screenshot_path)

    step_status = "PASSED" if step.status == "passed" else "FAILED"
    step_class = "passed" if step.status == "passed" else "failed"

    with open(context.report_path, 'a') as report_file:
        report_file.write(f"""
        <tr>
            <td>{step.name}</td>
            <td class="{step_class}">{step_status}</td>
            <td><a href='screenshots/{screenshot_name}' target='_blank'><img src='screenshots/{screenshot_name}' width='100'></a></td>
        </tr>
        """)


def after_scenario(context, scenario):
    """Quit WebDriver after every scenario."""
    context.driver.quit()
    print(f"❌ Browser closed for scenario: {scenario.name}")

    # Close scenario steps in the report
    with open(context.report_path, 'a') as report_file:
        report_file.write("</tbody>")


def after_all(context):
    """Finalize the HTML report."""
    with open(context.report_path, 'a') as report_file:
        report_file.write("""</table></body></html>""")


def read_json(file_path):
    """Utility to load JSON data from a file."""
    with open(file_path, 'r') as file:
        return json.load(file)
