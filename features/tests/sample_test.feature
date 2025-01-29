Feature: User Login

  Scenario: Successful Login with Valid Credentials
    Given I open the login page
    When I enter "testuser" and "password"
    And I click on login button
    Then I should see the dashboard

  Scenario: Successful Login with inValid Credentials
    Given I open the login page
    When I enter "testuser" and "password"
    And I click on login button
    Then I should see the dashboard