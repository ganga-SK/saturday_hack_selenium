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
