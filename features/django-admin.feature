# Created by p0tt3r at 11/03/22
Feature: django-admin can perform actions
  Tests to check if the django admin can perform basic
  functions of the shopping-cart.

  Scenario: django-admin can add categories in the cart
    Given I am in the Django Admin
    When I click on the "Categories" link
    Then I am on the "Categories" page
    Then I will click on the "ADD CATEGORY" button
    Then I add data for a new Category item and click on "Save" button
