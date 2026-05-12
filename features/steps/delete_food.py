from behave import *

use_step_matcher("parse")


@given('Exists a food')
def step_impl(context):
    from nutrieps.models import FoodItem
    for row in context.table:
        FoodItem.objects.create(
            name=row['name'], 
            calories=float(row['calories']), 
            protein=0, carbs=0, fat=0
        )

@given('Exists a consumption log for user "{username}"')
def step_impl(context, username):
    from django.contrib.auth.models import User
    from nutrieps.models import FoodItem, ConsumptionLog
    
    user = User.objects.get(username=username)
    
    for row in context.table:
        food = FoodItem.objects.get(name=row['food_name'])
        context.consumption_log = ConsumptionLog.objects.create(
            user=user, 
            food=food, 
            quantity=float(row['quantity'])
        )


@when('I go to the history page')
def step_impl(context):
    context.browser.visit(context.get_url('/history/'))


@when('I click the delete button for "{food_name}"')
def step_impl(context, food_name):
    delete_links = context.browser.find_by_css('a[title="Delete"]')
    assert len(delete_links) > 0, "No delete buttons found on the page"
    delete_links.first.click()


@then('I see the delete confirmation page with "{food_name}"')
def step_impl(context, food_name):
    assert context.browser.is_text_present('Delete Food Log'), \
        "Delete confirmation page title not found"
    assert context.browser.is_text_present(food_name), \
        f"Food name '{food_name}' not found on confirmation page"
    assert context.browser.is_text_present('Are you sure'), \
        "Confirmation question not found"


@when('I confirm the deletion')
def step_impl(context):
    button = context.browser.find_by_css('.btn-delete')
    assert len(button) > 0, "Delete confirmation button not found"
    button.first.click()


@when('I click the cancel button')
def step_impl(context):
    cancel = context.browser.find_by_css('.btn-cancel')
    assert len(cancel) > 0, "Cancel button not found"
    cancel.first.click()


@then('I am redirected to the history page')
def step_impl(context):
    assert '/history' in context.browser.url, \
        f"Expected to be on history page, but URL is {context.browser.url}"


@then('I should not see "{food_name}" in the food log')
def step_impl(context, food_name):
    assert not context.browser.is_text_present(food_name), \
        f"Food '{food_name}' should not be visible after deletion"


@then('I should see "{food_name}" in the food log')
def step_impl(context, food_name):
    assert context.browser.is_text_present(food_name), \
        f"Food '{food_name}' should still be visible after cancelling"


@when('I try to access the delete page for the consumption log')
def step_impl(context):
    from nutrieps.models import ConsumptionLog
    log = ConsumptionLog.objects.first()
    context.browser.visit(context.get_url(f'/history/delete/{log.id}/'))


@then('I am redirected to the login page')
def step_impl(context):
    assert '/accounts/login' in context.browser.url, \
        f"Expected redirect to login, but URL is {context.browser.url}"
