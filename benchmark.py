#!/usr/bin/env python

import csv
from sys import argv, exit, stdout
from time import time, ctime, sleep
from cStringIO import StringIO
from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

if len(argv) < 2:
    exit("Expected one argument: domainname")

domain = argv[-1]

## https://stackoverflow.com/questions/7157994/do-not-want-images-to-load-and-css-to-render-on-firefox
# get the Firefox profile object
ff_profile = FirefoxProfile()
# Disable CSS
ff_profile.set_preference('permissions.default.stylesheet', 2)
# Disable images
ff_profile.set_preference('permissions.default.image', 2)
# Disable Flash
ff_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
# Set the modified profile while creating the browser object
browser = webdriver.Firefox(ff_profile)


def time_it(function):
    def wrapper(*args, **kwargs):
        # Visit main page
        browser.delete_all_cookies()
        browser.get("http://" + domain)
        sleep(1)
        total = 0.0
        values = [function.__name__]
        stdout.write(function.__name__ + ":\t")
        stdout.flush()
        for i in range(0, 10):
            begin = time()
            function(*args, **kwargs)
            end = time()
            delta = end - begin
            values.append(delta)
            total += delta
            stdout.write("%s\t" % round(delta, 2))
            stdout.flush()
        stdout.write("avg: %s\t" % (total / 10))
        stdout.flush()
        print
        return values
    return wrapper



@time_it
def refresh():
    browser.refresh()


@time_it
def find_product():
    browser.find_element_by_id("search").clear()
    browser.find_element_by_id("search").send_keys("muis")
    browser.find_element_by_class_name("button").click()


@time_it
def find_product_and_put_in_cart():
    browser.find_element_by_partial_link_text("Vlooien Kat").click()
    browser.find_element_by_partial_link_text("knoflook").click()
    browser.find_element_by_class_name("btn-cart-grouped").click()


@time_it
def category_page1():
    browser.find_element_by_partial_link_text("Kat").click()


@time_it
def category_page2():
    browser.find_element_by_partial_link_text("Kattenvoer").click()


@time_it
def category_page3():
    browser.get("http://%s/katten/kattenvoer" % domain)
    browser.find_element_by_partial_link_text("Droogvoer").click()
    browser.find_element_by_partial_link_text("Biologisch").click()

@time_it
def category_page4():
    browser.find_element_by_partial_link_text("Hond").click()

@time_it
def category_page5():
    browser.find_element_by_partial_link_text("Hond").click()
    browser.find_element_by_partial_link_text("Hondenspeelgoed").click()
    browser.find_element_by_partial_link_text("Ballen").click()

@time_it
def category_page6():
    browser.find_element_by_partial_link_text("Nieuw").click()

@time_it
def category_page7():
    browser.find_element_by_partial_link_text("Acties").click()



@time_it
def checkout():
    browser.get("http://%s/ferret-vite-happy-vitam-120gr.html" % domain)
    browser.find_element_by_class_name("btn-cart").click()
    browser.get("http://%s/checkout/cart/" % domain)
    browser.find_element_by_class_name("btn-checkout").click()



csv_file = StringIO()
csv_writer = csv.writer(csv_file)

csv_writer.writerow(["Benchmark performed on domain %s at %s" % (domain, ctime())])
csv_writer.writerow(category_page1())
csv_writer.writerow(category_page2())
csv_writer.writerow(category_page3())
csv_writer.writerow(category_page4())
csv_writer.writerow(category_page5())
csv_writer.writerow(category_page6())
csv_writer.writerow(category_page7())
csv_writer.writerow(refresh())
csv_writer.writerow(find_product())
csv_writer.writerow(find_product_and_put_in_cart())
csv_writer.writerow(checkout())

browser.quit()

csv_file.seek(0)
print
print csv_file.read()

