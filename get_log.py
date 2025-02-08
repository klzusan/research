# python 3.12.2

import os, time
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, TimeoutException

# 各種設定
browsers = ['chrome', 'firefox', 'edge']
url_file = 'urls.txt'
log_dir = 'logs'
waiting_time = 10

# メイン
def main():
    urls = read_urls(url_file)

    for browser in browsers:
        print(f"{browser}")
        try:
            for url in urls:
                driver = setup_driver(browser, url)
                save_console_logs(browser, driver, url)
                driver.quit()
        finally:
            driver.quit()
        
# urlを一つずつ読み込む
def read_urls(file_path):
    with open(file_path, 'r') as f:
        urls = f.read().splitlines()
    return urls

# 各ブラウザのドライバ設定
def setup_driver(browser, url):
    try:
        if browser == 'chrome':
            options = webdriver.ChromeOptions()
            options.add_argument("--incognito")
            options.add_argument("--disable-extensions")
            os.makedirs(f"{log_dir}/{browser}/raw", exist_ok=True)
            output = os.path.join(log_dir, browser, "raw", f"{url}.txt")
            service = webdriver.ChromeService(log_output=output, service_args=['--log-level=ALL'])
            driver = webdriver.Chrome(service=service, options=options)
        elif browser == 'firefox':
            options = webdriver.FirefoxOptions()
            options.add_argument("--private")
            options.add_argument("--disable-extensions")
            os.makedirs(f"{log_dir}/{browser}/raw", exist_ok=True)
            output = os.path.join(log_dir, browser, "raw", f"{url}.txt")
            service = webdriver.FirefoxService(log_output=output, service_args=['--log', 'trace'])
            driver = webdriver.Firefox(service=service, options=options)
        elif browser == 'edge':
            options = webdriver.EdgeOptions()
            options.add_argument("--disable-extensions")
            options.add_argument("--inprivate")
            os.makedirs(f"{log_dir}/{browser}/raw", exist_ok=True)
            output = os.path.join(log_dir, browser, "raw", f"{url}.txt")
            service = webdriver.EdgeService(log_output=output, service_args=['--log-level=ALL'])
            driver = webdriver.Edge(service=service, options=options)
        else:
            raise ValueError('Unsupported borwser')
    except WebDriverException:
        print("WebDriverException")
        return None
    return driver

# urlのフォーマット
def format_url(url):
    print("Processing \"" + url + '\"')
    if not url.startswith("http://") and not url.startswith("https://"):
        return "https://" + url
    return url

# 指定URLにアクセスしてコンソールメッセージをログファイルに保存
def save_console_logs(browser, driver, url):
    formatted_url = format_url(url)
    try:
        driver.get(formatted_url)
        time.sleep(waiting_time)
    except TimeoutException:
        print(f"Failed to load page: {url} (Timeout)")
        return
    except WebDriverException as e:
        print(f"Failed to load page: {url} (Error: {e})")
        return

if __name__ == '__main__':
    main()
    print("Done")