from behave import *

use_step_matcher("parse")

@given("I'm not logged in")
def step_impl(context):
    context.browser.visit(context.get_url('/accounts/logout/'))

@when('I register a food consumption')
def step_impl(context):
    context.browser.visit(context.get_url('/add-consumption/'))
    
    from urllib.parse import urlparse
    current_path = urlparse(context.browser.url).path
    
    if current_path == '/add-consumption/':
        for row in context.table:
            context.browser.fill('food_name', row['food_name'])
            context.browser.fill('calories', row['calories'])
            context.browser.fill('quantity', row['quantity'])
        
        button = context.browser.find_by_css('button[type="submit"]')
        if button:
            button.first.click()
    else:
        pass
