import os
from flask import Flask, render_template, request, send_file
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

app = Flask(__name__)

downloads_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
if not os.path.exists(downloads_dir):
    os.makedirs(downloads_dir)

@app.route('/')
def index():
    return render_template('index.html')  

@app.route('/download', methods=['POST'])
def download():
    wiki_url = request.form['wiki_url']

    edge_options = EdgeOptions()
    edge_options.use_chromium = True  
    edge_options.add_argument('--headless')  
    edge_options.add_argument(f"--download.default_directory={os.path.abspath(downloads_dir)}")


    edge_driver_path = r'C:\Users\nimmi\Downloads\edgedriver_win64\msedgedriver.exe'
    edge_service = EdgeService(edge_driver_path)

    capabilities = DesiredCapabilities.EDGE.copy()
    capabilities['download.default_directory'] = os.path.abspath(downloads_dir)

    class DownloadCompleteListener(AbstractEventListener):
        def __init__(self):
            pass

        def after_navigate_to(self, url, driver):
            print(f"Navigated to {url}")

        def after_click(self, element, driver):
            print(f"Clicked element with tag name '{element.tag_name}'")

    try:
        driver = EventFiringWebDriver(webdriver.Edge(service=edge_service, options=edge_options), DownloadCompleteListener())
        driver.get(wiki_url)

        wait = WebDriverWait(driver, 10)
        print_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Download as PDF")))
        print_link.click()

    except Exception as e:
        return render_template('error.html', error=str(e))

    finally:
        if 'driver' in locals():
            driver.quit()  

    downloaded_files = [(f, os.path.getmtime(os.path.join(downloads_dir, f))) for f in os.listdir(downloads_dir)]
    if downloaded_files:
        newest_file = max(downloaded_files, key=lambda x: x[1])[0]
        pdf_path = os.path.join(downloads_dir, newest_file)
        return send_file(pdf_path, as_attachment=True)
    else:
        return render_template('error.html', error="Download failed or no file found")

if __name__ == '__main__':
    app.run(debug=True)
