from __future__ import annotations
from selenium import webdriver
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
import typing
import time


def setup_browser() -> WebDriver:
    return webdriver.Firefox()


def element_finder(
    driver: WebDriver,
    type: str,
    find_str: typing.Union[str, typing.List[str]],
) -> "WebElement":
    content = None
    if type == "class":
        content = driver.find_element_by_class_name(find_str)
    elif type == "xpath":
        content = driver.find_element_by_xpath(find_str)
    elif type == "css":
        content = driver.find_element_by_css_selector(find_str)
    return content


def elements_finder(
    driver: WebDriver,
    type: str,
    find_str: str,
) -> typing.List["WebElement"]:
    content = []
    if type == "class":
        content = driver.find_elements_by_class_name(find_str)
    elif type == "css":
        content = driver.find_elements_by_css_selector(find_str)
    return content


def check_race_started(
    element: "WebElement"
) -> bool:
    return element.is_enabled()


if __name__ == "__main__":
    browser = setup_browser()
    browser.get("https://play.typeracer.com")
    start_game_button = (
        WebDriverWait(browser, 10)
        .until(lambda d: element_finder(
                driver=d,
                type="class",
                find_str="""gwt-Anchor.prompt-button.bkgnd-green""",
            )
        )
    )
    if start_game_button:
        start_game_button.click()
    key = "unselectable"
    paragraphs = (
        WebDriverWait(browser, 10)
        .until(lambda d: elements_finder(
                driver=d,
                type="css",
                find_str="span[unselectable=on]",
            )
        )
    )
    last = paragraphs.pop()
    text = ""
    for p in paragraphs:
        text += p.text
    text += " "
    text += last.text
    print("___________________")
    print(text)
    print("___________________")
    input_field = (
        WebDriverWait(browser, 15)
        .until(lambda d: element_finder(
            driver=d,
            type="css",
            find_str="input[class='txtInput']",
        ))
    )
    print("RACE STARTED")
    # input_field.click()
    for word in text.split(" "):
        input_field.send_keys(word)
        time.sleep(0.05)
        input_field.send_keys(" ")
        time.sleep(0.05)
    time.sleep(5)
    browser.close()
