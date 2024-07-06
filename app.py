from flask import Flask, render_template, request, send_file
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

app = Flask(__name__)


# if driver downloaded to default downloads folder
downloads_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
driver_path = os.path.join(downloads_dir, 'chromedriver.exe')
# Replace with the path to your WebDriver if necessary

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    wiki_url = request.form['wiki_url']
    
    # Init
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    prefs = {'download.default_directory': os.path.abspath('./downloads')}
    options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(executable_path=driver_path, options=options)
    try:
        driver.get(wiki_url)

        time.sleep(2)

        print_link = driver.find_element(By.LINK_TEXT, "Download as PDF")
        print_link.click()

        time.sleep(5)

        download_link = driver.find_element(By.LINK_TEXT, "Download the file")
        download_link.click()

        time.sleep(10)

        download_dir = os.path.abspath('./downloads') #getting directory with files

        downladed_files = os.listdir(download_dir)

        pdf_file = [file for file in downladed_files if file.endswith('.pdf')][0] #getting first pdf file within all the downloaded files

        pdf_path = os.path.join(download_dir, pdf_file) #creating a full path for the pdf within the download_dir

    finally: 
        driver.quit()

    return send_file(pdf_path, as_attachment=True)

if __name__ == '__main__':
    if not os.path.exists('./downloads'):
        os.makedirs('./downloads')
    app.run(debug=True)





