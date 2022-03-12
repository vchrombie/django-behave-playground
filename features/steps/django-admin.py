from behave import Given, When, Then

from selenium.webdriver.common.by import By

from pattern.text.en import singularize


@given("I am in the Django Admin")
def step_impl(context):

    # Login to the django-admin panel
    context.selenium.get(f'{context.test.live_server_url}/admin/')

    username = context.selenium.find_element(value='id_username')
    password = context.selenium.find_element(value='id_password')

    username.send_keys('admin')
    password.send_keys('admin')

    context.selenium.find_element(by=By.XPATH, value="//input[@value='Log in']").click()

    context.test.assertEquals(context.selenium.title, 'Site administration | Django site admin')


@when('I click on the "{name}" link')
def step_impl(context, name):
    context.selenium.find_element(by=By.LINK_TEXT, value=name).click()


@then('I am on the "{name}" page')
def step_impl(context, name):
    name = singularize(str(name)).lower()
    context.test.assertEquals('Select {} to change | Django site admin'.format(name), context.selenium.title)


@then('I will click on the "ADD {name}" button')
def step_impl(context, name):
    name = str(name).lower()

    context.selenium.refresh()
    context.selenium.find_element(by=By.XPATH, value="//a[@href='/admin/products/{}/add/']".format(name)).click()

    context.test.assertEquals("Add {} | Django site admin".format(name), context.selenium.title)


@then('I add data for a new Category item and click on "Save" button')
def step_impl(context):
    title = context.selenium.find_element(value='id_title')
    title.send_keys('Books')
    context.selenium.find_element(by=By.XPATH, value="//input[@value='Save']").click()

    context.test.assertEquals("Select category to change | Django site admin", context.selenium.title)
