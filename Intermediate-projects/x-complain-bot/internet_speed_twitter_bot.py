from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from dotenv import load_dotenv
import tweepy

load_dotenv()


class SpeedTester:
    """Handles internet speed testing via Selenium."""
    
    def __init__(self, url="https://www.speedtest.net/"):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option('detach', True)
        chrome_options.add_argument("--disable-popup-blocking")
        # Anti-detection settings
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        
        self.driver = webdriver.Chrome(options=chrome_options)
        # Remove webdriver flag
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.driver.get(url)
        
        # Store promised speeds as floats
        self.promised_up = float(os.environ.get("PROMISED_UP", 0))
        self.promised_down = float(os.environ.get("PROMISED_DOWN", 0))
        self.download_speed = 0.0
        self.upload_speed = 0.0
    
    def _accept_cookies(self):
        """Accept cookie consent popup."""
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        )
        self.driver.find_element(By.ID, value="onetrust-accept-btn-handler").click()

    def _run_speed_test(self):
        """Execute the speed test and capture results."""
        self.driver.find_element(By.CLASS_NAME, value="start-text").click()

        WebDriverWait(self.driver, 60).until(
            EC.text_to_be_present_in_element((By.CLASS_NAME, "download-speed"), ".")
        )
        WebDriverWait(self.driver, 60).until(
            EC.text_to_be_present_in_element((By.CLASS_NAME, "upload-speed"), ".")
        )

        self.download_speed = float(self.driver.find_element(By.CLASS_NAME, value="download-speed").text)
        self.upload_speed = float(self.driver.find_element(By.CLASS_NAME, value="upload-speed").text)
        print(f"Download: {self.download_speed} Mbps, Upload: {self.upload_speed} Mbps")

    def run_test(self):
        """Run the complete speed test workflow."""
        self._accept_cookies()
        self._run_speed_test()
        self.driver.quit()


class TwitterBot:
    """Handles posting to X/Twitter via Tweepy API."""
    
    def __init__(self):
        self.client = tweepy.Client(
            consumer_key=os.environ.get("X_API_KEY"),
            consumer_secret=os.environ.get("X_API_SECRET"),
            access_token=os.environ.get("X_ACCESS_TOKEN"),
            access_token_secret=os.environ.get("X_ACCESS_TOKEN_SECRET")
        )

    def post(self, message, reply_to_id=None):
        """
        Post a tweet or reply to an existing tweet.
        
        Args:
            message: The tweet content
            reply_to_id: Optional tweet ID to reply to
            
        Returns:
            The ID of the created tweet
        """
        if reply_to_id:
            response = self.client.create_tweet(text=message, in_reply_to_tweet_id=reply_to_id)
        else:
            response = self.client.create_tweet(text=message)
        
        tweet_id = response.data['id']
        print(f"Tweet posted! ID: {tweet_id}")
        return tweet_id

 