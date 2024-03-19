import requests
from time import sleep
from settings import TEST_MODE

def wait_until_present(url, xpath, timeout=5):
    response = requests.get(url)
    if response.status_code == 200:
        json_response = response.json()
        if json_response.get('xpath') == xpath:
            return True
    return False

def click_element(url, xpath):
    response = requests.post(url, json={'xpath': xpath})
    return response.status_code == 200

def next_month(url):
    return click_element(url, "/html/body/div[5]/div[2]/div/a")

def current_month_available(url):
    return wait_until_present(url, "/html/body/div[5]/div[1]/table/tbody")

def nearest_available(url):
    avalible_in = 0
    while not current_month_available(url):
        next_month(url)
        avalible_in += 1
    return avalible_in

def select_date(url):
    response = requests.get(url)
    if response.status_code == 200:
        json_response = response.json()
        if json_response.get('class') == "undefined":
            return json_response.get('date')
    return None

def reschedule(url):
    reschedule_url = "/html/body/div[4]/main/div[4]/div/div/form/div[2]/fieldset/ol/li/input"
    response = requests.post(url, json={'xpath': reschedule_url})
    if response.status_code == 200:
        if not TEST_MODE:
            confirm_url = "/html/body/div[6]/div/div/a[2]"
            requests.post(url, json={'xpath': confirm_url})

def legacy_reschedule(url):
    driver_url = "http://yourdriverurl.com"
    date_selection_box = "/html/body/div[4]/main/div[4]/div/div/form/fieldset/ol/fieldset/div/div[2]/div[3]/label[1]"
    date_selection_url = driver_url + "/element"
    if click_element(date_selection_url, date_selection_box):
        avalible_in_months = nearest_available(driver_url)
        print("Trying to pick time and reschedule...")
        selected_date = select_date(driver_url)
        if selected_date:
            appointment_time_url = driver_url + "/element"
            appointment_time_options_url = driver_url + "/elements"
            click_element(appointment_time_url, selected_date)
            sleep(2)
            appointment_time_options = requests.get(appointment_time_options_url)
            if appointment_time_options.status_code == 200:
                last_option = appointment_time_options.json()[-1]
                click_element(appointment_time_url, last_option)
                reschedule(driver_url)

# Call the legacy_reschedule function with your driver URL
legacy_reschedule("http://yourdriverurl.com")