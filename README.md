![Step1-](https://github.com/user-attachments/assets/1e2bb186-cb9d-4267-92b6-d4e980ec4a34)

![Step3-](https://github.com/user-attachments/assets/37f74637-761a-482d-b065-6a03d35b1959.png =250x250)

![Step](https://github.com/user-attachments/assets/61337ca1-e515-46f2-90d3-773f28b86af8.png =250x250)

![Step67](https://github.com/user-attachments/assets/f166eca5-16f5-42a4-99be-c7b2f2d68463.png =250x250)

# Auto Bill Generator

# Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Installation](#installation)
   - [Clone the Repository](#clone-the-repository)
   - [Set Up the Environment](#set-up-the-environment)
     - [Create a virtual environment](#create-a-virtual-environment)
     - [Activate the virtual environment](#activate-the-virtual-environment)
     - [Install the required packages](#install-the-required-packages)
     - [Install ChromeDriver](#install-chromedriver)
4. [Configuration](#configuration)
   - [Environment Variables](#environment-variables)
   - [Requirements](#requirements)
5. [Usage](#usage)
   - [Start the Application](#start-the-application)
6. [API Reference](#api-reference)
   - [Home](#home)
   - [Run Script](#run-script)
7. [Code Structure](#code-structure)
8. [Troubleshooting](#troubleshooting)
9. [Contributing](#contributing)
10. [License](#license)
11. [Acknowledgements](#acknowledgements)



## Overview

The Auto Bill Generator is a Python Flask application that automates the process of downloading a bill in PDF format from a specified website, extracting key information from the PDF, and sending an SMS with the bill details using Twilio. The application uses Selenium for web scraping, OpenCV and Tesseract for image processing, and Flask for serving the web interface.

## Features

- Downloads a PDF bill from the CESC website.
- Converts the PDF to an image and processes it.
- Extracts the bill amount and date from the image.
- Sends an SMS with the bill details using Twilio.


  

## Installation

### Clone the Repository

```bash
git clone https://github.com/your-username/your-repository.git
cd your-repository
```


### Set Up the Environment


#### Create a virtual environment:

```bash
python -m venv venv
```

#### Activate the virtual environment:

##### On Windows:

```bash
venv\Scripts\activate
```

##### On macOS/Linux:

```bash
source venv/bin/activate
```

#### Install the required packages:

```bash
pip install -r requirements.txt
```


#### Install ChromeDriver:

ChromeDriver is automatically installed using chromedriver-autoinstaller included in the project. Ensure you have Google Chrome installed.

## Configuration

### Environment Variables

Create a .env file in the root directory of the project and add your Twilio credentials:

```dotenv
ACCOUNT_SID=your_twilio_account_sid
AUTH_TOKEN=your_twilio_auth_token
FROM_NUMBER=your_twilio_phone_number
TO_NUMBER=recipient_phone_number
```
### Requirements
- Python 3.x
- Google Chrome
- ChromeDriver (handled by chromedriver-autoinstaller)

## Usage
### Start the Application
Run the Flask application with:
```bash
python app.py
```

The application will be accessible at 'http://localhost:8000'.

## API Reference
### Home
```bash
GET / 
```

### Run Script
```bash
POST /run
```

- Description: Initiates the process to download the PDF, process it, and send an SMS.
- Responses:
  - 200 OK: Indicates successful processing.
  - 400 Bad Request: Indicates an error occurred during processing.
 
## Code Structure
- app.py: Main Flask application file.
- requirements.txt: Contains the required Python packages.
- temp/: Directory for storing temporary files (PDFs, images).
- README.md: Documentation file

## Troubleshooting
- Error in downloading PDF: Ensure the customer ID and website URL are correct. Check network issues.
- Error in processing image: Ensure Tesseract and OpenCV are correctly installed and configured.
- SMS not sent: Verify Twilio credentials and phone numbers.

## Contributing
Feel free to open issues or submit pull requests to improve the project.


## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements
- [Selenium for web scraping](https://awesomeopensource.com/project/elangosundar/awesome-README-templates)
- [OpenCV]
- [Tesseract for image processing](https://github.com/tesseract-ocr/tessdoc?tab=readme-ov-file)
- [Twilio for SMS service](https://www.twilio.com/docs/messaging)

```perl
This template uses the `bash` code block format for all bash commands and the `http` code block format for HTTP methods. Adjust the repository URL and other placeholders as needed.
```
