import os
import time
import requests
import re
import logging
from pdf2image import convert_from_path
from PIL import Image
import cv2
import pytesseract
from flask import Flask, jsonify, render_template_string, request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Use the current working directory for temporary files
DOWNLOAD_DIR = os.path.join(os.getcwd(), 'temp')

# Create download directory if it doesn't exist
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

LOCK_FILE = os.path.join(DOWNLOAD_DIR, 'run.lock')

# Install ChromeDriver
chromedriver_autoinstaller.install()

def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--remote-debugging-port=9222")  # Optional for debugging

    prefs = {
        "download.default_directory": DOWNLOAD_DIR,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True,
    }
    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=options)
    return driver


def download_pdf_bill(driver):
    try:
        logging.info("WebDriver initialized.")
        driver.get("https://www.cesc.co.in/viewPrintBill")
        logging.info("Page loaded.")
        wait = WebDriverWait(driver, 60)
        customer_id_field = wait.until(
            EC.presence_of_element_located((By.ID, "customer_id"))
        )
        customer_id_field.send_keys("XX")
        logging.info("Customer ID entered.")
        generate_bill_button = wait.until(
            EC.presence_of_element_located((By.ID, "btn_bill"))
        )
        driver.execute_script("arguments[0].click();", generate_bill_button)
        logging.info("Generate Duplicate Bill button clicked using JavaScript.")
        time.sleep(20)
        pdf_element = wait.until(
            EC.presence_of_element_located((By.ID, "showPDFhere"))
        )
        pdf_url = pdf_element.get_attribute("data")
        logging.info(f"PDF URL found: {pdf_url}")
        pdf_path = os.path.join(DOWNLOAD_DIR, 'downloaded_bill.pdf')
        response = requests.get(pdf_url)
        if response.status_code == 200:
            with open(pdf_path, 'wb') as f:
                f.write(response.content)
            logging.info(f"PDF downloaded at: {pdf_path}")
        else:
            logging.error(f"Failed to download PDF. Status code: {response.status_code}")
    except Exception as e:
        logging.error(f"Error in download_pdf_bill: {e}")
        raise
    finally:
        driver.quit()
        logging.info("Browser closed.")
    return pdf_path

def pdf_to_images(pdf_path, dpi=300, width=2481, height=3508):
    images = convert_from_path(pdf_path, dpi=dpi)
    image = images[0]
    image = image.resize((width, height), Image.LANCZOS)
    image_path = os.path.join(DOWNLOAD_DIR, 'first_page_image.jpg')
    image.save(image_path, 'JPEG')
    return image_path

def preprocess_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found at {image_path}")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    denoised = cv2.fastNlMeansDenoising(binary, h=30)
    processed_image_path = os.path.join(DOWNLOAD_DIR, 'processed_image.jpg')
    cv2.imwrite(processed_image_path, denoised)
    return denoised

def extract_text_from_image(processed_image, x, y, w, h):
    roi = processed_image[y:y+h, x:x+w]
    pil_image = Image.fromarray(roi)
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(pil_image, config=custom_config)
    return text

def process_date(date_text):
    month_map = {
        "01": "January", "02": "February", "03": "March", "04": "April",
        "05": "May", "06": "June", "07": "July", "08": "August",
        "09": "September", "10": "October", "11": "November", "12": "December"
    }
    match = re.search(r'(\d{2})/(\d{2})/(\d{2,4})', date_text)
    if match:
        day, month, year = match.groups()
        month_name = month_map.get(month, "Invalid month")
        if year and len(year) == 2:
            year = "20" + year
        processed_date = f"{month_name}"
        return processed_date
    else:
        return "Invalid date format"

account_sid = 'XX'
auth_token = 'XX'
from_number = 'XX'

def send_sms(bill, month):
    from twilio.rest import Client
    people = {
        "M.k Biswas": 0.34,
        "Sanjay Gupta": 0.32,
        "Sanchita Adhikary": 0.17,
        "Sukhtara Mondal": 0.17
    }
    divided_amounts = {name: f"Rs {bill * proportion:.2f}" for name, proportion in people.items()}
    formatted_response = []

    for name in people.keys():
        if name in divided_amounts:
            formatted_response.append(f"{name}: {divided_amounts[name]}")

    formatted_response.append(f"For Month: {month}")
    formatted_response.append(f"Full Bill Amount: {bill}")
    response_string = "\n".join(formatted_response)

    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=response_string,
        from_=from_number,
        to='XX'
    )

    if message.sid:
        logging.info("SMS sent successfully!")
    else:
        logging.error("Failed to send SMS.")

@app.route('/')
def home():
    return render_template_string('''
        <!doctype html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Auto Bill Generator</title>
        </head>
        <body>
            <h1>Welcome to the Auto Bill Generator API</h1>
            <form action="/run" method="post">
                <button type="submit">Start</button>
            </form>
        </body>
        </html>
    ''')

@app.route('/run', methods=['POST'])
def run_script():
    if os.path.exists(LOCK_FILE):
        return jsonify({"status": "error", "message": "Process is already running."})

    open(LOCK_FILE, 'w').close()

    try:
        driver = init_driver()
        logging.info("WebDriver initialized.")
        
        pdf_path = download_pdf_bill(driver)
        logging.info("Processing PDF:", pdf_path)

        image_path = pdf_to_images(pdf_path)
        logging.info("Converted PDF to image:", image_path)

        processed_image = preprocess_image(image_path)

        bill_amount_coords = (725, 750, 200, 125)
        bill_amount_text = extract_text_from_image(processed_image, *bill_amount_coords)
        bill_amount = float(bill_amount_text)
        logging.info("Bill Amount:", bill_amount)

        date_coords = (242, 881, 150, 50)
        date_text = extract_text_from_image(processed_image, *date_coords)
        logging.info("Extracted Date:", date_text)
        processed_date = process_date(date_text)
        logging.info("Processed Date:", processed_date)

        send_sms(bill_amount, processed_date)
    except Exception as e:
        logging.error(f"Error in run_script: {e}")
        return jsonify({"status": "error", "message": str(e)})
    finally:
        if os.path.exists(LOCK_FILE):
            os.remove(LOCK_FILE)
        if 'driver' in locals():
            driver.quit()

    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
