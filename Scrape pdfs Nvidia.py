import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up the WebDriver
service = Service('C:/chromedriver-win64/chromedriver.exe')
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

# Navigate to the page
url = 'https://investor.nvidia.com/financial-info/financial-reports/default.aspx'
driver.get(url)

# Wait for the page to load
wait = WebDriverWait(driver, 20)

def download_pdf(pdf_url, save_path):
    response = requests.get(pdf_url)
    with open(save_path, 'wb') as f:
        f.write(response.content)

def scrape_and_download(section_name, section_xpath):
    print(f"Processing section: {section_name}")
    folder_path = os.path.join('nvidia_pdfs', section_name)
    os.makedirs(folder_path, exist_ok=True)

    try:
        section_div = wait.until(EC.presence_of_element_located((By.XPATH, section_xpath)))
        links = section_div.find_elements(By.XPATH, ".//a[contains(@class, 'module-financial-table_link')]")
        pdf_urls = [link.get_attribute('href') for link in links if link.get_attribute('href').endswith('.pdf')]

        for pdf_url in pdf_urls:
            file_name = os.path.join(folder_path, pdf_url.split('/')[-1])
            download_pdf(pdf_url, file_name)
            print(f'Downloaded {file_name}')
    except Exception as e:
        print(f"Error processing {section_name}: {e}")

# Define sections and their XPaths
sections = {
    "CFO_Commentary": "//*[@id='_ctrl0_ctl75_divModuleContainer']/div/div/div/div[2]/div[3]",
    "NVIDIA_Quarterly_Revenue_Trend": "//*[@id='_ctrl0_ctl75_divModuleContainer']/div/div/div/div[2]/div[4]",
    "Form_10Q_Form_10K": "//*[@id='_ctrl0_ctl75_divModuleContainer']/div/div/div/div[2]/div[5]",
    "Quarterly_Presentation": "//*[@id='_ctrl0_ctl75_divModuleContainer']/div/div/div/div[2]/div[6]",
    "Annual_Review_Proxy_Statement_10K": "//*[@id='_ctrl0_ctl75_divModuleContainer']/div/div/div/div[2]/div[7]"
}

# Process each section
for section_name, section_xpath in sections.items():
    scrape_and_download(section_name, section_xpath)

# Close the WebDriver
driver.quit()

print("All PDFs downloaded successfully.")

