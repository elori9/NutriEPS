Feature: Delete Food Consumption
  In order to manage my food consumption log
  As a registered user
  I want to delete food entries that I have logged

  Background: There is a registered user with a food log entry
    Given Exists a user "user1" with password "testpass123"
    And Exists a food
      | name   | calories |
      | Banana | 89       |
    And Exists a consumption log for user "user1"
      | food_name | quantity |
      | Banana    | 150      |

  Scenario: Delete own food consumption with confirmation
    Given I login as user "user1" with password "testpass123"
    When I go to the history page
    And I click the delete button for "Banana"
    Then I see the delete confirmation page with "Banana"
    When I confirm the deletion
    Then I am redirected to the history page
    And I should not see "Banana" in the food log

  Scenario: Cancel delete returns to history
    Given I login as user "user1" with password "testpass123"
    When I go to the history page
    And I click the delete button for "Banana"
    Then I see the delete confirmation page with "Banana"
    When I click the cancel button
    Then I am redirected to the history page
    And I should see "Banana" in the food log

  Scenario: Cannot delete food consumption without login
    Given I'm not logged in
    When I try to access the delete page for the consumption log
    Then I am redirected to the login page