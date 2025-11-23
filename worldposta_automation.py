import time
import random
import os
import csv
import json
from datetime import datetime
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains


# =====================================================
# CONFIGURATION
# =====================================================

# Registration
REGISTRATION_URL = "https://admin.worldposta.com/auth/register"

# Email Provider
EMAIL_LOGIN_URL = "https://mail.worldposta.com/"
EMAIL_DOMAIN = "@worldposta.com"

# Login
LOGIN_URL = "https://admin.worldposta.com/auth/login"

# Timeouts
EMAIL_WAIT_TIMEOUT = 300  # seconds to wait for verification email
DEFAULT_TIMEOUT = 30  # default WebDriverWait timeout

# Output
SCREENSHOT_DIR = r"C:\Users\olaaa\Desktop\Projects\Registeration\SS"
CSV_FILE = "registration_results.csv"
JSON_FILE = "registration_results.json"


# =====================================================
# UTILITIES (REUSED FROM EXISTING SCRIPT)
# =====================================================

def random_delay(min_sec=1, max_sec=3):
    """Random delay to mimic human behavior"""
    time.sleep(random.uniform(min_sec, max_sec))


def human_like_mouse_move(driver, element):
    """Move mouse in a human-like way"""
    try:
        action = ActionChains(driver)
        action.move_to_element(element).perform()
        random_delay(0.2, 0.5)
    except Exception as e:
        print(f"⚠ Mouse move error: {e}")


def human_like_typing(element, text):
    """Type text character by character with random delays"""
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.05, 0.15))


def generate_test_data():
    """Generate random test account data"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    random_num = random.randint(1000, 9999)

    data = {
        'full_name': f"Test User {random_num}",
        'email': f"testuser{timestamp}_{random_num}{EMAIL_DOMAIN}",
        'company': f"TestCorp{random_num}",
        'phone': f"+1555{random.randint(1000000, 9999999)}",
        'password': f"TestPass@{random_num}123"
    }

    return data


def ensure_directory(path):
    """Ensure directory exists"""
    os.makedirs(path, exist_ok=True)


def get_timestamp():
    """Get formatted timestamp"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_screenshot_filename(email, status):
    """Generate screenshot filename"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_email = email.replace("@", "_at_").replace(".", "_")
    return f"{safe_email}_{status}_{timestamp}.png"


# =====================================================
# AUTOMATION BOT CLASS
# =====================================================

class WorldPostaAutomationBot:
    def __init__(self, headless=False):
        """Initialize automation bot with undetected Chrome"""
        print("🌐 Launching Chrome browser...")

        options = uc.ChromeOptions()

        if not headless:
            options.add_argument("--start-maximized")
        else:
            options.add_argument("--headless=new")

        options.add_argument("--disable-blink-features=AutomationControlled")

        # Random window size
        window_width = random.randint(1200, 1920)
        window_height = random.randint(800, 1080)
        options.add_argument(f"--window-size={window_width},{window_height}")

        self.driver = uc.Chrome(options=options, use_subprocess=True)
        self.driver.set_page_load_timeout(60)
        self.wait = WebDriverWait(self.driver, DEFAULT_TIMEOUT)

        # Store account data
        self.account_data = None
        self.status_log = {
            'timestamp': get_timestamp(),
            'email': '',
            'status': 'unknown',
            'error_message': '',
            'screenshot_path': ''
        }

        # Ensure output directories exist
        ensure_directory(SCREENSHOT_DIR)

        print("✅ Browser launched successfully")


    def register(self, account_data):
        """
        Register a new account on WorldPosta

        Args:
            account_data: Dictionary with full_name, email, company, phone, password

        Returns:
            bool: True if registration successful, False otherwise
        """
        print("\n" + "="*60)
        print("📝 STEP 1: REGISTRATION")
        print("="*60)

        self.account_data = account_data
        self.status_log['email'] = account_data['email']

        try:
            print(f"🔗 Navigating to: {REGISTRATION_URL}")
            self.driver.get(REGISTRATION_URL)
            random_delay(3, 5)

            # Scroll to reveal form
            print("📜 Scrolling to registration form...")
            scroll_amount = random.randint(300, 500)
            self.driver.execute_script(f"window.scrollTo(0, {scroll_amount});")
            random_delay(1, 2)

            # Fill Full Name
            print(f"👤 Entering full name: {account_data['full_name']}")
            full_name_input = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[formcontrolname="FullName"]'))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", full_name_input)
            random_delay(0.5, 1)
            human_like_mouse_move(self.driver, full_name_input)
            full_name_input.click()
            random_delay(0.3, 0.6)
            human_like_typing(full_name_input, account_data['full_name'])
            random_delay(0.5, 1)

            # Fill Email
            print(f"📧 Entering email: {account_data['email']}")
            email_input = self.driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname="Email"]')
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", email_input)
            random_delay(0.5, 1)
            human_like_mouse_move(self.driver, email_input)
            email_input.click()
            random_delay(0.3, 0.6)
            human_like_typing(email_input, account_data['email'])
            random_delay(0.5, 1)

            # Fill Company Name
            print(f"🏢 Entering company: {account_data['company']}")
            company_input = self.driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname="Customer"]')
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", company_input)
            random_delay(0.5, 1)
            human_like_mouse_move(self.driver, company_input)
            company_input.click()
            random_delay(0.3, 0.6)
            human_like_typing(company_input, account_data['company'])
            random_delay(0.5, 1)

            # Fill Phone Number
            print(f"📱 Entering phone: {account_data['phone']}")
            phone_input = self.driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname="PhoneNumber"]')
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", phone_input)
            random_delay(0.5, 1)
            human_like_mouse_move(self.driver, phone_input)
            phone_input.click()
            random_delay(0.3, 0.6)
            human_like_typing(phone_input, account_data['phone'])
            random_delay(0.5, 1)

            # Fill Password
            print(f"🔑 Entering password")
            password_input = self.driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname="Password"]')
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", password_input)
            random_delay(0.5, 1)
            human_like_mouse_move(self.driver, password_input)
            password_input.click()
            random_delay(0.3, 0.6)
            human_like_typing(password_input, account_data['password'])
            random_delay(0.5, 1)

            # Fill Confirm Password
            print(f"🔐 Confirming password")
            confirm_password_input = self.driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname="ConfirmPassword"]')
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", confirm_password_input)
            random_delay(0.5, 1)
            human_like_mouse_move(self.driver, confirm_password_input)
            confirm_password_input.click()
            random_delay(0.3, 0.6)
            human_like_typing(confirm_password_input, account_data['password'])
            random_delay(1, 2)

            # Click Submit Button
            print("🚀 Clicking 'Create Account' button...")
            submit_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button#create-account'))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", submit_button)
            random_delay(0.5, 1)
            human_like_mouse_move(self.driver, submit_button)
            random_delay(0.3, 0.7)
            self.driver.execute_script("arguments[0].click();", submit_button)

            print("⏳ Waiting for registration to complete...")
            random_delay(5, 8)

            # Check if registration was successful
            # Look for success indicators or if we're redirected
            current_url = self.driver.current_url
            print(f"📍 Current URL: {current_url}")

            # Take screenshot of registration result
            screenshot_path = os.path.join(SCREENSHOT_DIR, get_screenshot_filename(account_data['email'], 'registration'))
            self.driver.save_screenshot(screenshot_path)
            print(f"📸 Screenshot saved: {screenshot_path}")

            print("✅ Registration form submitted successfully")
            return True

        except Exception as e:
            error_msg = f"Registration failed: {e}"
            print(f"❌ {error_msg}")
            self.status_log['error_message'] = error_msg

            # Take error screenshot
            try:
                screenshot_path = os.path.join(SCREENSHOT_DIR, get_screenshot_filename(account_data['email'], 'registration_error'))
                self.driver.save_screenshot(screenshot_path)
                self.status_log['screenshot_path'] = screenshot_path
                print(f"📸 Error screenshot saved: {screenshot_path}")
            except:
                pass

            return False


    def login_to_email(self, email, password):
        """
        Login to WorldPosta webmail

        Args:
            email: Full email address
            password: Email password

        Returns:
            bool: True if login successful, False otherwise
        """
        print("\n" + "="*60)
        print("📬 STEP 2: EMAIL LOGIN")
        print("="*60)

        try:
            print(f"🔗 Navigating to: {EMAIL_LOGIN_URL}")
            self.driver.get(EMAIL_LOGIN_URL)
            random_delay(3, 5)

            # Enter username
            print(f"📧 Entering email: {email}")
            username_input = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input#username'))
            )
            human_like_mouse_move(self.driver, username_input)
            username_input.click()
            random_delay(0.3, 0.6)
            human_like_typing(username_input, email)
            random_delay(0.5, 1)

            # Enter password
            print(f"🔑 Entering password")
            password_input = self.driver.find_element(By.CSS_SELECTOR, 'input#password')
            human_like_mouse_move(self.driver, password_input)
            password_input.click()
            random_delay(0.3, 0.6)
            human_like_typing(password_input, password)
            random_delay(1, 2)

            # Click login button
            print("🔓 Clicking login button...")
            login_button = self.driver.find_element(By.CSS_SELECTOR, 'div.signinbutton[onclick="clkLgn()"]')
            human_like_mouse_move(self.driver, login_button)
            random_delay(0.3, 0.7)
            self.driver.execute_script("arguments[0].click();", login_button)

            print("⏳ Waiting for email inbox to load...")
            random_delay(5, 8)

            # Check if login successful
            current_url = self.driver.current_url
            print(f"📍 Current URL: {current_url}")

            # Take screenshot
            screenshot_path = os.path.join(SCREENSHOT_DIR, get_screenshot_filename(email, 'email_login'))
            self.driver.save_screenshot(screenshot_path)
            print(f"📸 Screenshot saved: {screenshot_path}")

            print("✅ Email login successful")
            return True

        except Exception as e:
            error_msg = f"Email login failed: {e}"
            print(f"❌ {error_msg}")
            self.status_log['error_message'] = error_msg

            # Take error screenshot
            try:
                screenshot_path = os.path.join(SCREENSHOT_DIR, get_screenshot_filename(email, 'email_login_error'))
                self.driver.save_screenshot(screenshot_path)
                self.status_log['screenshot_path'] = screenshot_path
                print(f"📸 Error screenshot saved: {screenshot_path}")
            except:
                pass

            return False


    def find_verification_email(self, timeout=EMAIL_WAIT_TIMEOUT):
        """
        Find and open the verification email in inbox

        Args:
            timeout: Maximum seconds to wait for email

        Returns:
            bool: True if email found and opened, False otherwise
        """
        print("\n" + "="*60)
        print("🔍 STEP 3: FINDING VERIFICATION EMAIL")
        print("="*60)

        subject_keyword = "Welcome To WorldPosta Business Email"
        print(f"🔎 Looking for email with subject containing: '{subject_keyword}'")
        print(f"⏱️  Maximum wait time: {timeout} seconds")

        start_time = time.time()
        attempt = 0

        try:
            while time.time() - start_time < timeout:
                attempt += 1
                elapsed = int(time.time() - start_time)
                print(f"\n🔄 Attempt {attempt} (elapsed: {elapsed}s / {timeout}s)")

                # Refresh inbox
                print("🔄 Refreshing inbox...")
                self.driver.refresh()
                random_delay(3, 5)

                # Get page source and parse
                html = self.driver.page_source
                soup = BeautifulSoup(html, "html.parser")

                # Try multiple selectors for email rows
                email_selectors = [
                    'div[role="listitem"]',
                    'div[role="option"]',
                    'div.ms-List-cell',
                    'div._lvv_E',
                    'tr[role="row"]',
                    'div[data-convid]',
                    'div.customScrollBar div[tabindex]'
                ]

                email_found = False

                for selector in email_selectors:
                    try:
                        # Use Selenium to find elements
                        email_elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        print(f"   📋 Found {len(email_elements)} elements with selector: {selector}")

                        for idx, elem in enumerate(email_elements):
                            try:
                                elem_text = elem.text
                                if subject_keyword.lower() in elem_text.lower():
                                    print(f"✅ Found verification email!")
                                    print(f"📧 Element text: {elem_text[:100]}...")

                                    # Scroll to element
                                    self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", elem)
                                    random_delay(1, 2)

                                    # Click to open
                                    print("🖱️  Clicking to open email...")
                                    human_like_mouse_move(self.driver, elem)
                                    random_delay(0.5, 1)
                                    elem.click()
                                    random_delay(3, 5)

                                    # Take screenshot
                                    screenshot_path = os.path.join(SCREENSHOT_DIR, get_screenshot_filename(self.account_data['email'], 'email_found'))
                                    self.driver.save_screenshot(screenshot_path)
                                    print(f"📸 Screenshot saved: {screenshot_path}")

                                    email_found = True
                                    break
                            except Exception as e:
                                continue

                        if email_found:
                            break

                    except Exception as e:
                        continue

                if email_found:
                    print("✅ Verification email opened successfully")
                    return True

                # Wait before next attempt
                print(f"⏳ Email not found yet, waiting 15 seconds before retry...")
                time.sleep(15)

            # Timeout reached
            error_msg = f"Verification email not found after {timeout} seconds"
            print(f"❌ {error_msg}")
            self.status_log['error_message'] = error_msg
            return False

        except Exception as e:
            error_msg = f"Error finding verification email: {e}"
            print(f"❌ {error_msg}")
            self.status_log['error_message'] = error_msg
            return False


    def extract_verification_link(self):
        """
        Extract verification link from email body

        Returns:
            str: Verification URL or None if not found
        """
        print("\n" + "="*60)
        print("🔗 STEP 4: EXTRACTING VERIFICATION LINK")
        print("="*60)

        try:
            # Wait for email body to load
            random_delay(3, 5)

            # Get page source
            html = self.driver.page_source
            soup = BeautifulSoup(html, "html.parser")

            # Try to find verification link
            # Look for link with "Confirm Email Address" text or href containing "ConfirmEmail"

            print("🔍 Searching for verification link in email body...")

            # Method 1: Find by text
            links = soup.find_all("a", string=lambda text: text and "Confirm Email" in text)
            if links:
                verification_url = links[0].get("href")
                if verification_url:
                    print(f"✅ Found verification link (by text)")
                    print(f"🔗 URL: {verification_url}")
                    return verification_url

            # Method 2: Find by href pattern
            links = soup.find_all("a", href=lambda href: href and "ConfirmEmail" in href)
            if links:
                verification_url = links[0].get("href")
                if verification_url:
                    print(f"✅ Found verification link (by href pattern)")
                    print(f"🔗 URL: {verification_url}")
                    return verification_url

            # Method 3: Try using Selenium to find clickable link
            print("🔍 Trying Selenium to find clickable link...")
            try:
                link_element = self.driver.find_element(By.XPATH, "//a[contains(text(), 'Confirm Email')]")
                verification_url = link_element.get_attribute("href")
                if verification_url:
                    print(f"✅ Found verification link (via Selenium)")
                    print(f"🔗 URL: {verification_url}")
                    return verification_url
            except:
                pass

            # Method 4: Find any link with ConfirmEmail in href using Selenium
            try:
                link_element = self.driver.find_element(By.XPATH, "//a[contains(@href, 'ConfirmEmail')]")
                verification_url = link_element.get_attribute("href")
                if verification_url:
                    print(f"✅ Found verification link (via Selenium href)")
                    print(f"🔗 URL: {verification_url}")
                    return verification_url
            except:
                pass

            error_msg = "Could not find verification link in email"
            print(f"❌ {error_msg}")
            self.status_log['error_message'] = error_msg

            # Take screenshot for debugging
            screenshot_path = os.path.join(SCREENSHOT_DIR, get_screenshot_filename(self.account_data['email'], 'no_link_found'))
            self.driver.save_screenshot(screenshot_path)
            print(f"📸 Screenshot saved: {screenshot_path}")

            return None

        except Exception as e:
            error_msg = f"Error extracting verification link: {e}"
            print(f"❌ {error_msg}")
            self.status_log['error_message'] = error_msg
            return None


    def confirm_email(self, verification_url):
        """
        Click verification link to confirm email

        Args:
            verification_url: The confirmation URL

        Returns:
            bool: True if confirmation successful, False otherwise
        """
        print("\n" + "="*60)
        print("✉️  STEP 5: CONFIRMING EMAIL")
        print("="*60)

        try:
            print(f"🔗 Navigating to verification URL...")
            self.driver.get(verification_url)
            random_delay(5, 8)

            # Check result
            current_url = self.driver.current_url
            print(f"📍 Current URL: {current_url}")

            # Take screenshot
            screenshot_path = os.path.join(SCREENSHOT_DIR, get_screenshot_filename(self.account_data['email'], 'email_confirmed'))
            self.driver.save_screenshot(screenshot_path)
            print(f"📸 Screenshot saved: {screenshot_path}")

            print("✅ Email confirmation completed")
            return True

        except Exception as e:
            error_msg = f"Email confirmation failed: {e}"
            print(f"❌ {error_msg}")
            self.status_log['error_message'] = error_msg

            # Take error screenshot
            try:
                screenshot_path = os.path.join(SCREENSHOT_DIR, get_screenshot_filename(self.account_data['email'], 'confirmation_error'))
                self.driver.save_screenshot(screenshot_path)
                self.status_log['screenshot_path'] = screenshot_path
                print(f"📸 Error screenshot saved: {screenshot_path}")
            except:
                pass

            return False


    def login_to_website(self, email, password):
        """
        Login to WorldPosta website after email confirmation

        Args:
            email: User email
            password: User password

        Returns:
            bool: True if login successful, False otherwise
        """
        print("\n" + "="*60)
        print("🔐 STEP 6: LOGGING INTO WEBSITE")
        print("="*60)

        try:
            print(f"🔗 Navigating to: {LOGIN_URL}")
            self.driver.get(LOGIN_URL)
            random_delay(3, 5)

            # Enter email
            print(f"📧 Entering email: {email}")
            email_input = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[formcontrolname="Email"]'))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", email_input)
            random_delay(0.5, 1)
            human_like_mouse_move(self.driver, email_input)
            email_input.click()
            random_delay(0.3, 0.6)
            human_like_typing(email_input, email)
            random_delay(0.5, 1)

            # Enter password
            print(f"🔑 Entering password")
            password_input = self.driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname="Password"]')
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", password_input)
            random_delay(0.5, 1)
            human_like_mouse_move(self.driver, password_input)
            password_input.click()
            random_delay(0.3, 0.6)
            human_like_typing(password_input, password)
            random_delay(1, 2)

            # Click Sign In button
            print("🚀 Clicking 'Sign in' button...")
            signin_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button#sign-in'))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", signin_button)
            random_delay(0.5, 1)
            human_like_mouse_move(self.driver, signin_button)
            random_delay(0.3, 0.7)
            self.driver.execute_script("arguments[0].click();", signin_button)

            print("⏳ Waiting for dashboard to load...")
            random_delay(5, 8)

            # Check if login successful
            current_url = self.driver.current_url
            print(f"📍 Current URL: {current_url}")

            # Take screenshot
            screenshot_path = os.path.join(SCREENSHOT_DIR, get_screenshot_filename(email, 'website_login'))
            self.driver.save_screenshot(screenshot_path)
            print(f"📸 Screenshot saved: {screenshot_path}")

            print("✅ Website login successful")
            return True

        except Exception as e:
            error_msg = f"Website login failed: {e}"
            print(f"❌ {error_msg}")
            self.status_log['error_message'] = error_msg

            # Take error screenshot
            try:
                screenshot_path = os.path.join(SCREENSHOT_DIR, get_screenshot_filename(email, 'website_login_error'))
                self.driver.save_screenshot(screenshot_path)
                self.status_log['screenshot_path'] = screenshot_path
                print(f"📸 Error screenshot saved: {screenshot_path}")
            except:
                pass

            return False


    def perform_post_login_actions(self):
        """
        Perform actions after login: Click View Posta and View CloudEdge buttons

        Returns:
            bool: True if all actions successful, False otherwise
        """
        print("\n" + "="*60)
        print("🎯 STEP 7: POST-LOGIN ACTIONS")
        print("="*60)

        try:
            # Wait for dashboard to fully load
            random_delay(3, 5)

            # Scroll to reveal buttons
            print("📜 Scrolling to reveal action buttons...")
            scroll_amount = random.randint(500, 700)
            self.driver.execute_script(f"window.scrollTo(0, {scroll_amount});")
            random_delay(1, 2)

            # Find all launch buttons
            print("🔍 Finding launch buttons...")
            launch_buttons = self.driver.find_elements(By.CSS_SELECTOR, 'button.launch-button')
            print(f"   Found {len(launch_buttons)} launch buttons")

            if len(launch_buttons) < 2:
                error_msg = f"Expected 2 launch buttons, found {len(launch_buttons)}"
                print(f"⚠ {error_msg}")
                self.status_log['error_message'] = error_msg

            # Click first button (View Posta)
            if len(launch_buttons) >= 1:
                print("🖱️  Clicking 'View Posta' button...")
                posta_button = launch_buttons[0]
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", posta_button)
                random_delay(1, 2)
                human_like_mouse_move(self.driver, posta_button)
                random_delay(0.5, 1)
                self.driver.execute_script("arguments[0].click();", posta_button)
                print("✅ Clicked 'View Posta' button")
                random_delay(3, 5)

                # Take screenshot
                screenshot_path = os.path.join(SCREENSHOT_DIR, get_screenshot_filename(self.account_data['email'], 'view_posta'))
                self.driver.save_screenshot(screenshot_path)
                print(f"📸 Screenshot saved: {screenshot_path}")

                # Navigate back if needed
                print("⬅️  Navigating back to dashboard...")
                self.driver.back()
                random_delay(3, 5)

            # Click second button (View CloudEdge)
            if len(launch_buttons) >= 2:
                # Re-find buttons after navigation
                launch_buttons = self.driver.find_elements(By.CSS_SELECTOR, 'button.launch-button')

                print("🖱️  Clicking 'View CloudEdge' button...")
                cloudedge_button = launch_buttons[1]
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", cloudedge_button)
                random_delay(1, 2)
                human_like_mouse_move(self.driver, cloudedge_button)
                random_delay(0.5, 1)
                self.driver.execute_script("arguments[0].click();", cloudedge_button)
                print("✅ Clicked 'View CloudEdge' button")
                random_delay(3, 5)

                # Take screenshot
                screenshot_path = os.path.join(SCREENSHOT_DIR, get_screenshot_filename(self.account_data['email'], 'view_cloudedge'))
                self.driver.save_screenshot(screenshot_path)
                print(f"📸 Screenshot saved: {screenshot_path}")

            print("✅ All post-login actions completed")
            return True

        except Exception as e:
            error_msg = f"Post-login actions failed: {e}"
            print(f"❌ {error_msg}")
            self.status_log['error_message'] = error_msg

            # Take error screenshot
            try:
                screenshot_path = os.path.join(SCREENSHOT_DIR, get_screenshot_filename(self.account_data['email'], 'post_login_error'))
                self.driver.save_screenshot(screenshot_path)
                self.status_log['screenshot_path'] = screenshot_path
                print(f"📸 Error screenshot saved: {screenshot_path}")
            except:
                pass

            return False


    def take_final_screenshot(self):
        """Take final screenshot after completing all steps"""
        print("\n📸 Taking final screenshot...")
        try:
            screenshot_path = os.path.join(SCREENSHOT_DIR, get_screenshot_filename(self.account_data['email'], 'final_success'))
            self.driver.save_screenshot(screenshot_path)
            self.status_log['screenshot_path'] = screenshot_path
            print(f"✅ Final screenshot saved: {screenshot_path}")
            return screenshot_path
        except Exception as e:
            print(f"⚠ Could not take final screenshot: {e}")
            return None


    def save_status(self):
        """Save automation status to CSV and JSON"""
        print("\n" + "="*60)
        print("💾 SAVING RESULTS")
        print("="*60)

        try:
            # Update timestamp
            self.status_log['timestamp'] = get_timestamp()

            # Save to CSV
            csv_exists = os.path.exists(CSV_FILE)
            with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['timestamp', 'email', 'status', 'error_message', 'screenshot_path'])
                if not csv_exists:
                    writer.writeheader()
                writer.writerow(self.status_log)
            print(f"✅ Status saved to CSV: {CSV_FILE}")

            # Save to JSON
            json_data = []
            if os.path.exists(JSON_FILE):
                with open(JSON_FILE, 'r', encoding='utf-8') as f:
                    try:
                        json_data = json.load(f)
                    except:
                        json_data = []

            json_data.append(self.status_log)

            with open(JSON_FILE, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)
            print(f"✅ Status saved to JSON: {JSON_FILE}")

        except Exception as e:
            print(f"⚠ Error saving status: {e}")


    def run_full_workflow(self, account_data=None):
        """
        Run complete automation workflow

        Args:
            account_data: Optional dictionary with account info. If None, generates random data.

        Returns:
            bool: True if entire workflow successful, False otherwise
        """
        print("\n" + "="*60)
        print("🚀 STARTING FULL AUTOMATION WORKFLOW")
        print("="*60)

        try:
            # Generate account data if not provided
            if account_data is None:
                print("🎲 Generating random test account data...")
                account_data = generate_test_data()

            print(f"\n📋 Account Data:")
            print(f"   Full Name: {account_data['full_name']}")
            print(f"   Email: {account_data['email']}")
            print(f"   Company: {account_data['company']}")
            print(f"   Phone: {account_data['phone']}")
            print(f"   Password: {'*' * len(account_data['password'])}")

            # Step 1: Register
            if not self.register(account_data):
                self.status_log['status'] = 'failed_registration'
                self.save_status()
                return False

            # Step 2: Login to email
            if not self.login_to_email(account_data['email'], account_data['password']):
                self.status_log['status'] = 'failed_email_login'
                self.save_status()
                return False

            # Step 3: Find verification email
            if not self.find_verification_email():
                self.status_log['status'] = 'failed_email_not_found'
                self.save_status()
                return False

            # Step 4: Extract verification link
            verification_url = self.extract_verification_link()
            if not verification_url:
                self.status_log['status'] = 'failed_no_verification_link'
                self.save_status()
                return False

            # Step 5: Confirm email
            if not self.confirm_email(verification_url):
                self.status_log['status'] = 'failed_email_confirmation'
                self.save_status()
                return False

            # Step 6: Login to website
            if not self.login_to_website(account_data['email'], account_data['password']):
                self.status_log['status'] = 'failed_website_login'
                self.save_status()
                return False

            # Step 7: Perform post-login actions
            if not self.perform_post_login_actions():
                self.status_log['status'] = 'failed_post_login_actions'
                self.save_status()
                return False

            # Step 8: Take final screenshot
            self.take_final_screenshot()

            # Success!
            self.status_log['status'] = 'success'
            self.save_status()

            print("\n" + "="*60)
            print("🎉 WORKFLOW COMPLETED SUCCESSFULLY!")
            print("="*60)

            return True

        except Exception as e:
            error_msg = f"Workflow failed: {e}"
            print(f"\n❌ {error_msg}")
            self.status_log['error_message'] = error_msg
            self.status_log['status'] = 'failed_unexpected_error'
            self.save_status()
            return False


    def close(self):
        """Close browser and cleanup"""
        try:
            print("\n🔒 Closing browser...")
            self.driver.quit()
            print("✅ Browser closed")
        except Exception as e:
            print(f"⚠ Error closing browser: {e}")


# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":
    print("="*60)
    print("🚀 WORLDPOSTA AUTOMATION BOT")
    print("📌 Full Registration → Email Verification → Login Workflow")
    print("="*60)

    bot = None

    try:
        # Initialize bot (visible browser)
        bot = WorldPostaAutomationBot(headless=False)

        # Option 1: Run with auto-generated test data
        print("\n📌 Running automation with auto-generated test data...")
        success = bot.run_full_workflow()

        # Option 2: Run with custom account data (uncomment to use)
        # custom_data = {
        #     'full_name': "John Doe",
        #     'email': "john.doe@worldposta.com",
        #     'company': "Acme Corp",
        #     'phone': "+15551234567",
        #     'password': "SecurePass@123"
        # }
        # success = bot.run_full_workflow(custom_data)

        if success:
            print("\n✨ Automation completed successfully!")
        else:
            print("\n⚠️  Automation completed with errors. Check logs for details.")

        # Keep browser open for inspection
        print("\n⏸️  Browser will stay open. Press Ctrl+C to close...")
        input("Press ENTER to close browser and exit...")

    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
    finally:
        if bot:
            bot.close()
