Feature: Edit Food Consumption
  In order to keep my food consumption log accurate
  As a registered user
  I want to edit the quantity of food entries I have logged

  Background: There are registered users and a food log entry
    Given Exists a user "user1" with password "testpass123"
    And Exists a user "user2" with password "testpass123"
    And Exists a food
      | name   | calories |
      | Banana | 89       |
    And Exists a consumption log for user "user1"
      | food_name | quantity |
      | Banana    | 150      |

  Scenario: Edit own food consumption successfully
    Given I login as user "user1" with password "testpass123"
    When I go to the history page
    And I click the edit button for "Banana"
    Then I see the edit page for "Banana"
    When I change the quantity to 250
    And I submit the edit form
    Then I am redirected to the history page
    And I should see "Banana" with quantity 250 in the food log

  Scenario: Cancel edit returns to history
    Given I login as user "user1" with password "testpass123"
    When I go to the history page
    And I click the edit button for "Banana"
    Then I see the edit page for "Banana"
    When I click the cancel button
    Then I am redirected to the history page
    And I should see "Banana" with quantity 150 in the food log

  Scenario: Cannot edit food consumption without login
    Given I'm not logged in
    When I try to access the edit page for the consumption log
    Then I am redirected to the login page

  Scenario: Cannot edit another user's food consumption
    Given I login as user "user2" with password "testpass123"
    When I try to access the edit page for user1's consumption log
    Then I receive a 403 Forbidden error