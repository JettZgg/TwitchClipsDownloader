from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

def get_clip_download_url(driver, clip_url):
    """
    Get the download link for a Twitch clip.
    
    :param driver: Selenium WebDriver instance
    :param clip_url: URL of the Twitch clip page.
    :return: Download URL of the clip, or None if failed.
    """
    print(f"Fetching clip page: {clip_url}")
    
    try:
        driver.get(clip_url)
        
        # Wait for the video element to be present
        video_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "video"))
        )
        
        # Get the src attribute of the video element
        video_url = video_element.get_attribute('src')
        
        if video_url:
            print(f"Found video URL: {video_url}")
            return video_url
        else:
            print("Could not find video URL")
            return None
    except Exception as e:
        print(f"Error parsing Twitch page: {str(e)}")
        return None
