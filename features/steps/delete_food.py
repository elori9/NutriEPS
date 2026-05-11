from behave import *
from django.contrib.auth.models import User
from nutrieps.models import FoodItem, ConsumptionLog

use_step_matcher("parse")


@given('I have a consumption log entry for "{food_name}" with {quantity:d} grams')
def step_impl(context, food_name, quantity):
    user = User.objects.get(username="testuser")
    food, _ = FoodItem.objects.get_or_create(
        name=food_name,
        defaults={'calories': 52, 'protein': 0.3, 'carbs': 14, 'fat': 0.2}
    )
    context.consumption_log = ConsumptionLog.objects.create(
        user=user, food=food, quantity=quantity
    )


@given('I have a consumption log entry for "{food_name}" with {quantity:d} grams as user "{username}"')
def step_impl(context, food_name, quantity, username):
    user = User.objects.get(username=username)
    food, _ = FoodItem.objects.get_or_create(
        name=food_name,
        defaults={'calories': 52, 'protein': 0.3, 'carbs': 14, 'fat': 0.2}
    )
    context.consumption_log = ConsumptionLog.objects.create(
        user=user, food=food, quantity=quantity
    )


@given('"{username}" has a consumption log entry for "{food_name}" with {quantity:d} grams')
def step_impl(context, username, food_name, quantity):
    user = User.objects.get(username=username)
    food, _ = FoodItem.objects.get_or_create(
        name=food_name,
        defaults={'calories': 100, 'protein': 5, 'carbs': 10, 'fat': 3}
    )
    context.other_consumption_log = ConsumptionLog.objects.create(
        user=user, food=food, quantity=quantity
    )


@when('I visit the history page')
def step_impl(context):
    context.browser.visit(context.get_url('/history/'))


@when('I click the delete icon for "{food_name}"')
def step_impl(context, food_name):
    # Find the delete link (🗑️) next to the food name
    import time
    time.sleep(0.5)
    # Look for the link that contains the delete URL for this food's consumption log
    links = context.browser.links.find_by_partial_text('🗑️')
    # Click the first matching delete icon
    for link in links:
        link.click()
        break


@then('I should see the delete confirmation page')
def step_impl(context):
    assert context.browser.is_text_present('Are you sure you want to delete this entry?')


@then('I should see "{text}"')
def step_impl(context, text):
    assert context.browser.is_text_present(text), f"Text '{text}' not found on page"


@when('I confirm the deletion')
def step_impl(context):
    button = context.browser.find_by_id('confirm-delete-btn')
    button.click()


@when('I cancel the deletion')
def step_impl(context):
    link = context.browser.find_by_id('cancel-delete-btn')
    link.click()


@then('I should be redirected to the history page')
def step_impl(context):
    assert '/history/' in context.browser.url


@then('I should not see "{text}" in the food log')
def step_impl(context, text):
    assert not context.browser.is_text_present(text), f"Text '{text}' should not be present on page"


@then('I should see "{text}" in the food log')
def step_impl(context, text):
    assert context.browser.is_text_present(text), f"Text '{text}' should be present on page"


@when('I try to delete the consumption log entry for "{food_name}" by "{username}"')
def step_impl(context, food_name, username):
    log = context.other_consumption_log
    context.browser.visit(context.get_url(f'/delete-consumption/{log.pk}/'))


@then('I should get a forbidden response')
def step_impl(context):
    assert '403' in context.browser.html or 'Forbidden' in context.browser.html


@when('I try to delete the consumption log without being logged in')
def step_impl(context):
    log = context.consumption_log
    context.browser.visit(context.get_url(f'/delete-consumption/{log.pk}/'))


@then('I should be redirected to the login page')
def step_impl(context):
    assert '/accounts/login/' in context.browser.url
