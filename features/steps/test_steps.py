from behave import *
import time

@given("I open the login page")
def step_open_login_page(context):
    config = context.read_json("features/config.json")
    context.driver.get(config["base_url"])

@when('I enter "{username}" and "{password}"')
def step_enter_credentials(context, username, password):
    locators = context.read_json("features/locators/locators.json")
    # context.driver.find_element_by_id(locators["loginPage"]["usernameField"].split(":")[1]).send_keys(username)
    # context.driver.find_element_by_id(locators["loginPage"]["passwordField"].split(":")[1]).send_keys(password)

@when("I click on login button")
def step_click_login(context):
    locators = context.read_json("features/locators/locators.json")
    # context.driver.find_element_by_xpath(locators["loginPage"]["loginButton"].split(":")[1]).click()

@then("I should see the dashboard")
def step_verify_dashboard(context):
    time.sleep(2)
    # assert "Dashboard" in context.driver.page_source, "Dashboard not loaded"
