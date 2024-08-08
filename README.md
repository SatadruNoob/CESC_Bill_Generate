Table of Contents
Introduction
Prerequisites
Application Workflow
Setup and Installation
Environment Variables
Detailed Code Explanation
Importing Modules
Flask App Setup
Logging Configuration
Temporary Directory Setup
Driver Initialization (init_driver)
Download PDF Bill (download_pdf_bill)
Convert PDF to Image (pdf_to_images)
Preprocess Image (preprocess_image)
Extract Text from Image (extract_text_from_image)
Process Date (process_date)
Send SMS (send_sms)
Flask Routes
Running the Application
Error Handling
Conclusion
Introduction
This application is designed to automate the process of downloading an electricity bill from the CESC website, converting the PDF bill into an image, extracting the bill amount and due date from the image, and sending an SMS with the extracted information to predefined recipients.

Prerequisites
Python 3.x
Flask
Selenium
Google Chrome and ChromeDriver
PDF processing libraries (pdf2image, PIL, cv2, pytesseract)
Twilio account for sending SMS
Basic knowledge of Python, Flask, and web scraping
Application Workflow
Initialize WebDriver: The application starts by initializing the Chrome WebDriver using Selenium.
Download Bill: It navigates to the CESC website, enters the customer ID, and downloads the bill as a PDF.
Convert PDF to Image: The downloaded PDF is converted into an image using the pdf2image library.
Preprocess Image: The image is preprocessed (grayscale, binary threshold, denoising) to make text extraction more accurate.
Extract Text: The application extracts the bill amount and due date from specific coordinates on the image using OCR (pytesseract).
Process Date: The extracted date is processed into a human-readable format.
Send SMS: The bill amount and date are sent via SMS to predefined recipients using the Twilio API.
Flask API: The application provides a simple web interface to trigger the bill generation and SMS sending process.
Setup and Installation    





