# These lines of code are importing necessary modules and classes for the script to work properly:
import pyautogui #Automates mouse and keyboard actions for UI interaction.
import os #Provides a way of using operating system-dependent functionality.
from pathlib import Path #Offers object-oriented filesystem path handling.
from selenium import webdriver #Selenium WebDriver for automating web browser interaction.
from selenium.common.exceptions import TimeoutException #Exception handling for timeouts in Selenium operations.
from selenium.webdriver.common.by import By #Allows specifying how to locate elements in Selenium (e.g., by ID, class).
from selenium.webdriver.support.ui import WebDriverWait #Enables waiting for certain conditions in Selenium.
from selenium.webdriver.support import expected_conditions as EC #Provides a set of predefined conditions to wait for in Selenium.

# Configures PyAutoGUI to pause for 0.5 seconds after each function call. This helps in making the automation more reliable.
pyautogui.PAUSE = 0.5

class PDFViewerPage:
    """
    A class to represent and interact with a PDF viewer page in a web browser.
    It allows actions like opening a PDF, zooming in, etc.
    """

    def __init__(self, driver, pdf_path):
        """
        Constructor for PDFViewerPage.
        :param driver: Selenium WebDriver for browser automation.
        :param pdf_path: The file path of the PDF to be opened.
        """
        self.driver = driver
        self.pdf_path = pdf_path

    def open_pdf(self, page_number, initial_zoom_level):
        """
        Opens a PDF file in the browser at a specified page and zoom level.
        :param page_number: The page number to navigate to within the PDF.
        :param initial_zoom_level: The initial zoom level for viewing the PDF.
        """
        try:
            # Direct the browser to open the PDF at the specified page and zoom level.
            self.driver.get(f"{self.pdf_path}#page={page_number}&zoom={initial_zoom_level}")
            # Wait until the page's body is loaded to ensure the PDF is visible.
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        except TimeoutException:
            print("Loading the PDF took too much time!")

    def zoom_in(self, increase_zoom_count):
        """
        Zooms into the PDF by simulating keyboard shortcuts.
        :param increase_zoom_count: Number of times to simulate the 'zoom in' keystroke.
        """
        # Simulate holding down the 'ctrl' key ('command' key on Mac).
        pyautogui.keyDown('ctrl')
        # Simulate pressing the '+' key multiple times to zoom in.
        for _ in range(increase_zoom_count):
            pyautogui.press('+')
        # Release the 'ctrl' key after zooming in.
        pyautogui.keyUp('ctrl')

def init_driver(browser_name):
    """
    Initializes a WebDriver instance for a specified browser.
    :param browser_name: Name of the browser to use ('Edge' or 'Chrome').
    :return: A WebDriver instance for the specified browser.
    Note: To use a different browser, add its corresponding condition and return statement here.
    """
    if browser_name == "Edge":
        return webdriver.Edge()
    elif browser_name == "Chrome":
        return webdriver.Chrome()
    elif browser_name == "Firefox":
        return webdriver.Firefox()
    else:
        raise ValueError("Browser not supported")

def pre_zoom_test():
    """
    Performs a simple zoom in and out test.
    This is used to ensure that the PDF viewer responds to keyboard shortcuts.
    """
    pyautogui.keyDown('ctrl')
    pyautogui.press('+')
    pyautogui.press('-')
    pyautogui.keyUp('ctrl')

if __name__ == "__main__":
    # Specify the browser type and PDF file path. Change 'browser_name' to use a different browser.
    browser_name = "Chrome"  # Change this to 'Edge' or other supported browser names.
    pdf_file = Path(os.getcwd()) / "SWTD Mid Term Practice.pdf"
    pdf_path = f"file:///{pdf_file.resolve()}#page=5"
    
    # Initialize the WebDriver and maximize the browser window.
    driver = init_driver(browser_name)
    driver.maximize_window()
    
    # Create a PDFViewerPage instance and open the specified PDF.
    pdf_viewer = PDFViewerPage(driver, pdf_path)
    pdf_viewer.open_pdf(page_number=5, initial_zoom_level=100)

    # Conduct a pre-zoom test to ensure the viewer is ready for zoom commands.
    for _ in range(10):
        try:
            pre_zoom_test()
            break
        except:
            pass

    # Increase the zoom level in the PDF using PyAutoGUI.
    zoom_increase_count = 3
    pdf_viewer.zoom_in(zoom_increase_count)

    # Keep the script running until manually interrupted, checking every 0.5 seconds.
    try:
        while True:
            pyautogui.sleep(0.5)
    except KeyboardInterrupt:
        # Close the browser when the script is interrupted (e.g., by pressing Ctrl+C).
        driver.quit()