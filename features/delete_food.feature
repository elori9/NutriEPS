Feature: Delete food consumption log
  As a registered user
  I want to delete my food log entries
  So that I can correct mistakes in my consumption history

  Background: There is a registered user with a food log
    Given Exists a user "testuser" with password "testpass123"

  Scenario: Successfully delete own consumption log entry
    Given I login as user "testuser" with password "testpass123"
    And I have a consumption log entry for "Apple" with 150 grams
    When I visit the history page
    And I click the delete icon for "Apple"
    Then I should see the delete confirmation page
    And I should see "Apple"
    And I should see "150"
    When I confirm the deletion
    Then I should be redirected to the history page
    And I should not see "Apple" in the food log

  Scenario: Cancel deletion keeps the entry
    Given I login as user "testuser" with password "testpass123"
    And I have a consumption log entry for "Banana" with 200 grams
    When I visit the history page
    And I click the delete icon for "Banana"
    Then I should see the delete confirmation page
    When I cancel the deletion
    Then I should be redirected to the history page
    And I should see "Banana" in the food log

  Scenario: Cannot delete another user's consumption log
    Given Exists a user "otheruser" with password "otherpass123"
    And "otheruser" has a consumption log entry for "Pizza" with 300 grams
    And I login as user "testuser" with password "testpass123"
    When I try to delete the consumption log entry for "Pizza" by "otheruser"
    Then I should get a forbidden response

  Scenario: Unauthenticated user cannot delete entries
    Given I have a consumption log entry for "Rice" with 250 grams as user "testuser"
    When I try to delete the consumption log without being logged in
    Then I should be redirected to the login page
