from behave import *

use_step_matcher("parse")

@when('I click the edit button for "{food_name}"')
def step_impl(context, food_name):
    # Busquem un enllaç que vagi cap a la ruta d'editar.
    # (Si fas servir un class específic com .btn-edit, pots canviar el find_by_css)
    edit_links = context.browser.find_by_css('a[title="Edit"]')
    assert len(edit_links) > 0, "No edit buttons found on the page"
    edit_links.first.click()

@then('I see the edit page for "{food_name}"')
def step_impl(context, food_name):
    assert context.browser.is_text_present(food_name), \
        f"Food name '{food_name}' not found on edit page"
    assert context.browser.is_element_present_by_name('quantity'), \
        "Quantity input field not found on the form"

@when('I change the quantity to {quantity}')
def step_impl(context, quantity):
    # Omplim el camp del formulari que es diu 'quantity'
    context.browser.fill('quantity', quantity)

@when('I submit the edit form')
def step_impl(context):
    button = context.browser.find_by_css('button[type="submit"]')
    assert len(button) > 0, "Submit button not found"
    button.first.click()


@then('I should see "{food_name}" with quantity {quantity} in the food log')
def step_impl(context, food_name, quantity):
    assert context.browser.is_text_present(food_name), \
        f"Food '{food_name}' should be visible"
    assert context.browser.is_text_present(str(quantity)), \
        f"Quantity '{quantity}' should be visible"

@when('I try to access the edit page for the consumption log')
def step_impl(context):
    from nutrieps.models import ConsumptionLog
    log = ConsumptionLog.objects.first()
    context.browser.visit(context.get_url(f'/history/edit/{log.id}/'))

@when("I try to access the edit page for user1's consumption log")
def step_impl(context):
    from nutrieps.models import ConsumptionLog
    # Busquem un log que sapiguem segur que és del user1
    log = ConsumptionLog.objects.filter(user__username='user1').first()
    context.browser.visit(context.get_url(f'/history/edit/{log.id}/'))

@then('I receive a 403 Forbidden error')
def step_impl(context):
    # Quan Django bloqueja per permisos, sol mostrar una pàgina amb el codi 403
    assert context.browser.is_text_present('403') or context.browser.is_text_present('Forbidden'), \
        "Expected 403 Forbidden error page"