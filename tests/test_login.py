import pytest
from playwright.sync_api import Page, expect

@pytest.fixture
def login_page(page: Page):
    page.goto("https://www.saucedemo.com")
    return page

def test_successful_login(login_page: Page):
    page = login_page

    page.get_by_placeholder("username").fill("standard_user")
    page.get_by_placeholder("password").fill("secret_sauce")

    page.get_by_role("button", name="Login").click()

    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")

    expect(page.locator(".inventory_list")).to_be_visible()


def test_invalid_login(login_page: Page):

    page = login_page

    page.get_by_placeholder("username").fill("standard_user")
    page.get_by_placeholder("password").fill("wrong_password")

    page.get_by_role("button", name="Login").click()

    error_message = ("Epic sadface: Username and password do not match "
        "any user in this service")

    expect(page.get_by_text(error_message)).to_be_visible()
    expect(page.locator('[data-test="error"]')).to_be_visible()
    expect(page.locator('[data-test="error"]')).to_contain_text(
    "Username and password do not match")


def test_invalid_username(login_page: Page):

    page = login_page

    page.get_by_placeholder("username").fill("wrong-user")
    page.get_by_placeholder("password").fill("secret_sauce")

    page.get_by_role("button", name="Login").click()

    error_message = ("Epic sadface: Username and password do not match "
        "any user in this service")

    expect(page.get_by_text(error_message)).to_be_visible()

def test_empty_login(login_page: Page):
    page = login_page

    page.get_by_role("button", name="Login").click()

    error_message = ("Epic sadface: Username is required")

    expect(page.get_by_text(error_message)).to_be_visible()

def test_empty_username(login_page: Page):
    page = login_page

    page.get_by_placeholder("password").fill("secret_sauce")

    page.get_by_role("button", name="Login").click()

    error_message = ("Epic sadface: Username is required")

    expect(page.get_by_text(error_message)).to_be_visible()

def test_empty_password(login_page: Page):
    page = login_page

    page.get_by_placeholder("username").fill("standard_user")

    page.get_by_role("button", name="Login").click()

    expect(page.locator('[data-test="error"]')).to_be_visible()

    expect(page.locator('[data-test="error"]')).to_contain_text("Epic sadface: Password is required")

def test_product_displayed(login_page: Page):
    page = login_page

    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")

    page.get_by_role("button", name="Login").click()

    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")

    expect(page.locator(".inventory_list")).to_be_visible()

    expect(page.locator(".inventory_item")).to_have_count(6)

def test_add_product_to_cart(login_page: Page):
    page = login_page

    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")

    page.get_by_role("button", name="Login").click()

    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")

    product = page.locator(".inventory_item").filter(has_text="Sauce Labs Backpack")

    product.get_by_role("button", name="Add to cart").click()

    expect(page.locator(".shopping_cart_badge")).to_have_text("1")

    expect(product.get_by_role("button", name="Remove")).to_be_visible()

def test_product_appears_in_cart(login_page: Page):
    page = login_page

    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    
    page.get_by_role("button", name="Login").click()

    product = page.locator(".inventory_item").filter(has_text="Sauce Labs Backpack")

    product.get_by_role("button", name="Add to cart").click()

    page.locator(".shopping_cart_link").click()

    expect(page).to_have_url("https://www.saucedemo.com/cart.html")

    expect(page.locator(".cart_item").filter(has_text= "Sauce Labs Backpack"))

    expect(page.locator(".cart_item")).to_have_count(1)

def test_remove_product_from_cart(login_page: Page):
    page = login_page

    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")

    page.get_by_role("button", name="Login").click()

    product = page.locator(".inventory_item").filter(has_text="Sauce Labs Backpack")

    product.get_by_role("button", name="Add to cart").click()

    page.locator(".shopping_cart_link").click()

    expect(page.locator(".cart_item")).to_have_count(1)

    page.get_by_role("button", name="Remove").click()

    expect(page.locator(".cart_item")).to_have_count(0)

    expect(page.locator(".shopping_cart_badge")).to_have_count(0)

def test_complete_checkout(login_page: Page):
    page = login_page

    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.get_by_role("button", name="Login").click()

    product = page.locator(".inventory_item").filter(has_text="Sauce Labs Backpack")

    product.get_by_role("button", name="Add to cart").click()

    expect(page.locator(".shopping_cart_badge")).to_have_text("1")

    page.locator(".shopping_cart_link").click()

    expect(page.locator(".cart_item")).to_have_count(1)

    page.get_by_role("button", name="Checkout").click()

    expect(page).to_have_url("https://www.saucedemo.com/checkout-step-one.html")

    page.locator('[data-test="firstName"]').fill("Claiden")
    page.locator('[data-test="lastName"]').fill("K B")
    page.locator('[data-test="postalCode"]').fill("673579")

    page.get_by_role("button", name="Continue").click()

    expect(page).to_have_url("https://www.saucedemo.com/checkout-step-two.html")

    expect(page.locator(".inventory_item_name")).to_have_text("Sauce Labs Backpack")

    expect(page.locator(".inventory_item_price")).to_have_text("$29.99")

    expect(page.locator(".summary_subtotal_label")).to_have_text("Item total: $29.99")

    expect(page.locator(".summary_tax_label")).to_have_text("Tax: $2.40")

    expect(page.locator(".summary_total_label")).to_have_text("Total: $32.39")

    page.get_by_role("button", name="Finish").click()

    expect(page).to_have_url("https://www.saucedemo.com/checkout-complete.html")

    expect(page.get_by_role("heading", name="Thank you for your order!")).to_be_visible()


















