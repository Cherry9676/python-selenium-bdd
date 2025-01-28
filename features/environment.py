import os
from selenium import webdriver
import json


def before_all(context):
    """Attach custom methods to context."""
    # Add the read_json function to the context object
    context.read_json = read_json
    if not os.path.exists('reports'):
        os.makedirs('reports')
    context.report_file = open('reports/custom_report.txt', 'w')


def before_feature(context, feature):
    """Setup WebDriver before each feature."""
    config = context.read_json('features/Config.json')
    browser = config.get("browser", "chrome").lower()

    if browser == "chrome":
        context.driver = webdriver.Chrome(executable_path="drivers/chromedriver.exe")
    elif browser == "firefox":
        context.driver = webdriver.Firefox(executable_path="drivers/geckodriver.exe")
    else:
        raise ValueError(f"Browser '{browser}' is not supported.")
    context.driver.maximize_window()


def after_step(context, step):
    """Log step result after each step."""
    if step.status == "passed":
        context.report_file.write(f"Step PASSED: {step.name}\n")
    elif step.status == "failed":
        context.report_file.write(f"Step FAILED: {step.name}\n")


def after_feature(context, feature):
    """Quit WebDriver after each feature."""
    context.driver.quit()

def after_all(context):
    """Close the custom report file."""
    context.report_file.close()


def read_json(file_path):
    """Utility to load JSON data from a file."""
    with open(file_path, 'r') as file:
        return json.load(file)
