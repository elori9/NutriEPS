Feature: P1 Add food consumption (POST)

  Scenario: An authenticated user can register a record of food consumption
    Given Exists a user "admin" with password "testpass123"
    And I login as user "admin" with password "testpass123"
    When I register a food consumption
      | food_name | calories | quantity |
      | Banana    | 89       | 150      |
    Then I am redirected to the history page
    And I should see "Banana" in the food log

  Scenario: Try to register food consumption but not logged in
    # Aquest Given posat per assegurar-nos que no hi ha sessió
    Given I'm not logged in
    When I register a food consumption
      | food_name | calories | quantity |
      | Banana    | 89       | 150      |
    Then I am redirected to the login page