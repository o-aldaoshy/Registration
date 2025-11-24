"""
WorldPosta Complete Automation Suite
All-in-one script for registration, email verification, and login automation

Usage:
    python worldposta_automation_complete.py                    # Run with your custom test data (default)
    python worldposta_automation_complete.py --random           # Generate random test account
    python worldposta_automation_complete.py --headless         # Run in headless mode
"""

import time
import random
import os
import csv
import json
import argparse
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

# URLs
REGISTRATION_URL = "https://admin.worldposta.com/auth/register"
EMAIL_LOGIN_URL = "https://mail.worldposta.com/"
LOGIN_URL = "https://admin.worldposta.com/auth/login"

# Email Settings
EMAIL_DOMAIN = "@worldposta.com"
EMAIL_SUBJECT_KEYWORD = "Welcome To WorldPosta Business Email"

# Timeouts
EMAIL_WAIT_TIMEOUT = 300  # seconds to wait for verification email (5 minutes)
DEFAULT_TIMEOUT = 30  # default WebDriverWait timeout

# Output Paths
SCREENSHOT_DIR = r"C:\Users\olaaa\Desktop\Projects\Registeration\SS"
CSV_FILE = "registration_results.csv"
JSON_FILE = "registration_results.json"

# =====================================================
# YOUR CUSTOM TEST ACCOUNT DATA
# =====================================================

CUSTOM_TEST_ACCOUNT = {
    'full_name': "AI dexter85",
    'email': "ai.dexter85@worldposta.com",
    'company': "AI Company dexter85",
    'phone': "1095666032",
    'password': "gtzwO@lvr+A82biD5Xdmepf7k/*y1"
}


# =====================================================
# UTILITIES
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
        pass


def human_like_typing(element, text):
    """Type text character by character with random delays"""
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.05, 0.15))


def generate_random_account():
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
        """Register a new account on WorldPosta"""
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
        """Login to WorldPosta webmail"""
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
        """Find and open the verification email in inbox"""
        print("\n" + "="*60)
        print("🔍 STEP 3: FINDING VERIFICATION EMAIL")
        print("="*60)

        print(f"🔎 Looking for email with subject containing: '{EMAIL_SUBJECT_KEYWORD}'")
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
                        email_elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        print(f"   📋 Found {len(email_elements)} elements with selector: {selector}")

                        for idx, elem in enumerate(email_elements):
                            try:
                                elem_text = elem.text
                                if EMAIL_SUBJECT_KEYWORD.lower() in elem_text.lower():
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
        """Extract verification link from email body"""
        print("\n" + "="*60)
        print("🔗 STEP 4: EXTRACTING VERIFICATION LINK")
        print("="*60)

        try:
            # Wait for email body to load
            random_delay(3, 5)

            # Get page source
            html = self.driver.page_source
            soup = BeautifulSoup(html, "html.parser")

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
        """Click verification link to confirm email"""
        print("\n" + "="*60)
        print("✉️  STEP 5: CONFIRMING EMAIL")
        print("="*60)

        try:
            print(f"🔗 Navigating to verification URL...")
            self.driver.get(verification_url)
            random_delay(5, 8)

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
        """Login to WorldPosta website after email confirmation"""
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


    def get_browser_console_logs(self):
        """Capture browser console errors and warnings"""
        try:
            logs = self.driver.get_log('browser')
            errors = []
            warnings = []

            for entry in logs:
                level = entry.get('level', '')
                message = entry.get('message', '')

                if 'SEVERE' in level or 'ERROR' in level:
                    errors.append(message)
                elif 'WARNING' in level:
                    warnings.append(message)

            return {'errors': errors, 'warnings': warnings}
        except Exception as e:
            return {'errors': [], 'warnings': [], 'capture_error': str(e)}


    def detect_new_tab_or_window(self, original_handles):
        """Check if a new tab or window was opened"""
        try:
            current_handles = self.driver.window_handles
            if len(current_handles) > len(original_handles):
                new_handle = list(set(current_handles) - set(original_handles))[0]
                print(f"  🔄 New tab/window detected!")
                return new_handle
            return None
        except Exception as e:
            print(f"  ⚠️  Error detecting new window: {e}")
            return None


    def save_page_html_on_failure(self, page_name):
        """Save page HTML for debugging"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            html_filename = f"{page_name}_failure_{timestamp}.html"
            html_path = os.path.join(SCREENSHOT_DIR, html_filename)

            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(self.driver.page_source)

            print(f"  💾 HTML saved: {html_filename}")
            return html_path
        except Exception as e:
            print(f"  ⚠️  Could not save HTML: {e}")
            return None


    def detect_url_reload_loop(self, initial_url, max_checks=5, check_interval=2):
        """Detect if page is stuck in a reload loop"""
        print(f"  🔍 Monitoring for reload loops...")
        url_changes = []

        for i in range(max_checks):
            current_url = self.driver.current_url
            url_changes.append(current_url)

            if i > 0:
                # Check if URL changed back to initial URL
                if current_url == initial_url and url_changes[-2] != initial_url:
                    print(f"  ⚠️  Reload loop detected! Returned to: {initial_url}")
                    return True

            time.sleep(check_interval)

        # Check if we saw multiple different URLs (indicates cycling)
        unique_urls = set(url_changes)
        if len(unique_urls) > 2:
            print(f"  ⚠️  URL cycling detected: {len(unique_urls)} different URLs visited")
            return True

        return False


    def save_diagnostic_report(self, page_name, validation_result):
        """Save detailed diagnostic report to JSON"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_filename = f"{page_name}_diagnostic_{timestamp}.json"
            report_path = os.path.join(SCREENSHOT_DIR, report_filename)

            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(validation_result, f, indent=2, ensure_ascii=False)

            print(f"  📋 Diagnostic report saved: {report_filename}")
            return report_path
        except Exception as e:
            print(f"  ⚠️  Could not save diagnostic report: {e}")
            return None


    def validate_page_load(self, page_name, expected_url_fragment, expected_title_keywords,
                          expected_text, expected_element_selector, retry_on_failure=True):
        """
        Comprehensive page validation with detailed diagnostics (Option C)

        Args:
            page_name: Name for logging (e.g., "Posta")
            expected_url_fragment: String that should be in URL
            expected_title_keywords: List of keywords that might be in title
            expected_text: Text that should appear on page
            expected_element_selector: CSS selector for key element
            retry_on_failure: If True, retry validation once after waiting
        """
        print(f"\n🔍 Validating {page_name} page with comprehensive diagnostics...")

        validation_result = {
            'timestamp': get_timestamp(),
            'page_name': page_name,
            'validation_passed': False,
            'checks': [],
            'console_logs': {},
            'recommendations': [],
            'html_saved': None,
            'screenshot_saved': None
        }

        checks_passed = 0
        total_checks = 0

        # Capture initial state
        initial_url = self.driver.current_url
        validation_result['initial_url'] = initial_url

        # Wait for page to settle
        random_delay(3, 5)

        # === CHECK 1: URL Validation ===
        total_checks += 1
        current_url = self.driver.current_url
        validation_result['current_url'] = current_url

        check_result = {
            'name': 'URL Validation',
            'passed': False,
            'expected': f"URL containing '{expected_url_fragment}'",
            'actual': current_url
        }

        if expected_url_fragment.lower() in current_url.lower():
            print(f"  ✅ URL Check: Contains '{expected_url_fragment}'")
            check_result['passed'] = True
            checks_passed += 1
        else:
            print(f"  ❌ URL Check Failed")
            print(f"     Expected: URL containing '{expected_url_fragment}'")
            print(f"     Actual:   {current_url}")
            check_result['error'] = f"URL does not contain expected fragment"
            validation_result['recommendations'].append(f"Check if button opens page in new tab/window")

        validation_result['checks'].append(check_result)

        # === CHECK 2: Title Validation ===
        total_checks += 1
        page_title = self.driver.title
        validation_result['page_title'] = page_title

        check_result = {
            'name': 'Page Title Validation',
            'passed': False,
            'expected': f"Title containing keywords: {expected_title_keywords}",
            'actual': page_title
        }

        if any(keyword.lower() in page_title.lower() for keyword in expected_title_keywords):
            print(f"  ✅ Title Check: '{page_title}'")
            check_result['passed'] = True
            checks_passed += 1
        else:
            print(f"  ❌ Title Check Failed")
            print(f"     Expected: Keywords {expected_title_keywords}")
            print(f"     Actual:   {page_title}")
            check_result['error'] = f"Title doesn't match expected keywords"

        validation_result['checks'].append(check_result)

        # === CHECK 3: Expected Text Validation ===
        total_checks += 1
        page_source = self.driver.page_source

        check_result = {
            'name': 'Expected Text Validation',
            'passed': False,
            'expected': f"Page containing text: '{expected_text}'",
            'actual': None
        }

        if expected_text in page_source:
            print(f"  ✅ Text Check: Found '{expected_text}'")
            check_result['passed'] = True
            check_result['actual'] = f"Text found on page"
            checks_passed += 1
        else:
            print(f"  ❌ Text Check Failed")
            print(f"     Expected text not found: '{expected_text}'")
            check_result['error'] = f"Expected text not present on page"
            validation_result['recommendations'].append(f"Verify page loaded correctly - expected text missing")

        validation_result['checks'].append(check_result)

        # === CHECK 4: Key Element Validation ===
        total_checks += 1
        check_result = {
            'name': 'Key Element Validation',
            'passed': False,
            'expected': f"Element with selector: '{expected_element_selector}'",
            'actual': None
        }

        try:
            element = self.driver.find_element(By.CSS_SELECTOR, expected_element_selector)
            if element.is_displayed():
                print(f"  ✅ Element Check: Found and visible")
                check_result['passed'] = True
                check_result['actual'] = "Element found and displayed"
                checks_passed += 1
            else:
                print(f"  ⚠️  Element Check: Found but not visible")
                check_result['actual'] = "Element found but not displayed"
        except NoSuchElementException:
            print(f"  ❌ Element Check Failed")
            print(f"     Element not found: {expected_element_selector}")
            check_result['error'] = f"Expected element not found on page"
            validation_result['recommendations'].append(f"Element selector may have changed: {expected_element_selector}")

        validation_result['checks'].append(check_result)

        # === CHECK 5: No Error Messages ===
        total_checks += 1
        error_keywords = ["error", "failed", "not found", "404", "403", "500", "denied", "unauthorized"]
        page_source_lower = page_source.lower()

        check_result = {
            'name': 'Error Detection',
            'passed': True,
            'expected': 'No error keywords on page',
            'actual': None
        }

        found_errors = [keyword for keyword in error_keywords if keyword in page_source_lower]

        if not found_errors:
            print(f"  ✅ Error Check: No error keywords detected")
            check_result['actual'] = "No errors found"
            checks_passed += 1
        else:
            print(f"  ⚠️  Error Check: Potential errors detected")
            print(f"     Found keywords: {', '.join(found_errors)}")
            check_result['passed'] = False
            check_result['error'] = f"Error keywords found: {', '.join(found_errors)}"
            check_result['actual'] = f"Errors detected: {', '.join(found_errors)}"
            validation_result['recommendations'].append(f"Check page for error messages - keywords detected: {', '.join(found_errors)}")

        validation_result['checks'].append(check_result)

        # === CHECK 6: Page Not Blank ===
        total_checks += 1
        page_size = len(page_source)

        check_result = {
            'name': 'Page Content Check',
            'passed': False,
            'expected': 'Page size > 500 characters',
            'actual': f'{page_size} characters'
        }

        if page_size > 500:
            print(f"  ✅ Content Check: Page has content ({page_size} chars)")
            check_result['passed'] = True
            checks_passed += 1
        else:
            print(f"  ❌ Content Check: Page appears blank ({page_size} chars)")
            check_result['error'] = "Page appears blank or minimal content"

        validation_result['checks'].append(check_result)

        # === Capture Browser Console Logs ===
        print(f"  📋 Capturing browser console logs...")
        console_logs = self.get_browser_console_logs()
        validation_result['console_logs'] = console_logs

        if console_logs.get('errors'):
            print(f"  ⚠️  Browser Console Errors ({len(console_logs['errors'])}):")
            for error in console_logs['errors'][:3]:  # Show first 3
                print(f"     - {error[:100]}...")
            validation_result['recommendations'].append("Check browser console for JavaScript errors")
        else:
            print(f"  ✅ No browser console errors")

        # === Calculate Success Rate ===
        success_rate = checks_passed / total_checks if total_checks > 0 else 0
        validation_result['checks_passed'] = checks_passed
        validation_result['total_checks'] = total_checks
        validation_result['success_rate'] = success_rate

        # === Determine if Validation Passed ===
        validation_passed = success_rate >= 0.67  # Pass if 67% of checks passed (4 out of 6)

        if validation_passed:
            print(f"\n✅ {page_name} Validation PASSED ({checks_passed}/{total_checks} checks, {success_rate*100:.1f}%)")
            validation_result['validation_passed'] = True

            # Take success screenshot
            screenshot_path = os.path.join(SCREENSHOT_DIR, get_screenshot_filename(self.account_data['email'], f'{page_name.lower()}_success'))
            self.driver.save_screenshot(screenshot_path)
            validation_result['screenshot_saved'] = screenshot_path
            print(f"📸 Success screenshot saved: {os.path.basename(screenshot_path)}")

            return True, validation_result
        else:
            print(f"\n❌ {page_name} Validation FAILED ({checks_passed}/{total_checks} checks, {success_rate*100:.1f}%)")

            # === Save Diagnostic Data on Failure ===
            print(f"\n💾 Saving diagnostic data...")

            # Save screenshot
            screenshot_path = os.path.join(SCREENSHOT_DIR, get_screenshot_filename(self.account_data['email'], f'{page_name.lower()}_validation_error'))
            self.driver.save_screenshot(screenshot_path)
            validation_result['screenshot_saved'] = screenshot_path
            print(f"  📸 Error screenshot saved: {os.path.basename(screenshot_path)}")

            # Save HTML
            html_path = self.save_page_html_on_failure(page_name.lower())
            validation_result['html_saved'] = html_path

            # Save diagnostic report
            report_path = self.save_diagnostic_report(page_name.lower(), validation_result)
            validation_result['diagnostic_report'] = report_path

            # === Show Recommendations ===
            if validation_result['recommendations']:
                print(f"\n💡 Troubleshooting Suggestions:")
                for i, rec in enumerate(validation_result['recommendations'], 1):
                    print(f"  {i}. {rec}")

            # === Retry Logic ===
            if retry_on_failure:
                print(f"\n🔄 Retrying validation after 5 seconds...")
                time.sleep(5)
                print(f"  🔄 Refreshing page...")
                self.driver.refresh()
                random_delay(3, 5)

                print(f"  🔄 Running validation again (no retry this time)...")
                return self.validate_page_load(
                    page_name, expected_url_fragment, expected_title_keywords,
                    expected_text, expected_element_selector, retry_on_failure=False
                )

            return False, validation_result


    def perform_post_login_actions(self):
        """Perform actions after login: Click View Posta and View CloudEdge buttons with comprehensive validation"""
        print("\n" + "="*60)
        print("🎯 STEP 7: POST-LOGIN ACTIONS")
        print("="*60)

        try:
            # Wait for dashboard to fully load
            random_delay(3, 5)

            # Store original window handles
            original_handles = self.driver.window_handles
            original_url = self.driver.current_url

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

            # Find buttons by their text content
            posta_button = None
            cloudedge_button = None

            for button in launch_buttons:
                button_text = button.text.strip()
                if "View Posta" in button_text:
                    posta_button = button
                elif "View CloudEdge" in button_text:
                    cloudedge_button = button

            # ==================== VIEW POSTA ====================
            if posta_button:
                print("\n" + "-"*60)
                print("📧 CLICKING 'VIEW POSTA' BUTTON")
                print("-"*60)
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", posta_button)
                random_delay(1, 2)
                human_like_mouse_move(self.driver, posta_button)
                random_delay(0.5, 1)

                # Click button
                self.driver.execute_script("arguments[0].click();", posta_button)
                print("✅ Clicked 'View Posta' button")

                # Check for new tab/window
                random_delay(2, 3)
                new_handle = self.detect_new_tab_or_window(original_handles)
                if new_handle:
                    print("  🔄 Switching to new tab/window...")
                    self.driver.switch_to.window(new_handle)
                    random_delay(2, 3)

                # Check for reload loop
                if self.detect_url_reload_loop(original_url, max_checks=3, check_interval=2):
                    print("  ⚠️  Page stuck in reload loop!")
                    self.status_log['error_message'] = "Posta page stuck in reload loop"

                # Validate Posta page loaded correctly
                posta_validation, posta_report = self.validate_page_load(
                    page_name="Posta",
                    expected_url_fragment="tools.worldposta.com",
                    expected_title_keywords=["WorldPosta", "Tools", "Posta"],
                    expected_text="Choose a Plan to Start Your Demo",
                    expected_element_selector='a.btn[style*="color: white"]',
                    retry_on_failure=True
                )

                if not posta_validation:
                    error_msg = f"Posta page validation failed ({posta_report['checks_passed']}/{posta_report['total_checks']} checks)"
                    print(f"❌ {error_msg}")
                    self.status_log['error_message'] = error_msg
                    # Continue anyway to try CloudEdge

                # Navigate back to dashboard
                print("\n⬅️  Navigating back to dashboard...")
                if new_handle:
                    self.driver.close()
                    self.driver.switch_to.window(original_handles[0])
                else:
                    self.driver.back()
                random_delay(3, 5)

            # ==================== VIEW CLOUDEDGE ====================
            if cloudedge_button:
                print("\n" + "-"*60)
                print("☁️  CLICKING 'VIEW CLOUDEDGE' BUTTON")
                print("-"*60)

                # Re-find buttons after navigation by text matching
                launch_buttons = self.driver.find_elements(By.CSS_SELECTOR, 'button.launch-button')
                cloudedge_button = None
                for button in launch_buttons:
                    button_text = button.text.strip()
                    if "View CloudEdge" in button_text:
                        cloudedge_button = button
                        break

                if not cloudedge_button:
                    print("❌ CloudEdge button not found after navigation")
                    self.status_log['error_message'] = "CloudEdge button not found"
                    return False

                original_handles = self.driver.window_handles
                original_url = self.driver.current_url
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", cloudedge_button)
                random_delay(1, 2)
                human_like_mouse_move(self.driver, cloudedge_button)
                random_delay(0.5, 1)

                # Click button
                self.driver.execute_script("arguments[0].click();", cloudedge_button)
                print("✅ Clicked 'View CloudEdge' button")

                # Check for new tab/window
                random_delay(2, 3)
                new_handle = self.detect_new_tab_or_window(original_handles)
                if new_handle:
                    print("  🔄 Switching to new tab/window...")
                    self.driver.switch_to.window(new_handle)
                    random_delay(2, 3)

                # Check for reload loop
                if self.detect_url_reload_loop(original_url, max_checks=3, check_interval=2):
                    print("  ⚠️  Page stuck in reload loop!")
                    self.status_log['error_message'] = "CloudEdge page stuck in reload loop"

                # Validate CloudEdge page loaded correctly
                cloudedge_validation, cloudedge_report = self.validate_page_load(
                    page_name="CloudEdge",
                    expected_url_fragment="console.worldposta.com",
                    expected_title_keywords=["CloudEdge", "Console", "WorldPosta"],
                    expected_text="Complete Your Main Info",
                    expected_element_selector='button.green-btn[type="submit"]',
                    retry_on_failure=True
                )

                if not cloudedge_validation:
                    error_msg = f"CloudEdge page validation failed ({cloudedge_report['checks_passed']}/{cloudedge_report['total_checks']} checks)"
                    print(f"❌ {error_msg}")
                    self.status_log['error_message'] = error_msg
                    return False

                # Take final screenshot
                screenshot_path = os.path.join(SCREENSHOT_DIR, get_screenshot_filename(self.account_data['email'], 'cloudedge_final'))
                self.driver.save_screenshot(screenshot_path)
                print(f"📸 Final screenshot saved: {os.path.basename(screenshot_path)}")

            print("\n" + "="*60)
            print("✅ All post-login actions completed successfully")
            print("="*60)
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


    def run_full_workflow(self, account_data):
        """Run complete automation workflow"""
        print("\n" + "="*60)
        print("🚀 STARTING FULL AUTOMATION WORKFLOW")
        print("="*60)

        try:
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
# EXECUTION MODES
# =====================================================

def run_automation(headless=False, use_random=False):
    """Run automation with custom or random account"""
    bot = None
    try:
        bot = WorldPostaAutomationBot(headless=headless)

        # Use random or custom account
        if use_random:
            account_data = generate_random_account()
            print(f"\n🎲 Generated random account: {account_data['email']}")
        else:
            account_data = CUSTOM_TEST_ACCOUNT
            print(f"\n✅ Using custom test account: {account_data['email']}")

        success = bot.run_full_workflow(account_data)

        if success:
            print("\n✨ Automation completed successfully!")
        else:
            print("\n⚠️  Automation completed with errors. Check logs for details.")

        return success

    finally:
        if bot and not headless:
            print("\n⏸️  Browser will stay open. Press ENTER to close...")
            input("Press ENTER to close browser and exit...")
            bot.close()
        elif bot:
            bot.close()


# =====================================================
# MAIN
# =====================================================

def main():
    parser = argparse.ArgumentParser(
        description='WorldPosta Complete Automation Suite',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python worldposta_automation_complete.py                    # Run with your custom test data (default)
  python worldposta_automation_complete.py --random           # Generate random test account
  python worldposta_automation_complete.py --headless         # Run in headless mode
  python worldposta_automation_complete.py --random --headless # Random account in headless mode
        """
    )

    parser.add_argument('--random', action='store_true',
                       help='Generate random test account instead of using custom data')
    parser.add_argument('--headless', action='store_true',
                       help='Run browser in headless mode (hidden)')

    args = parser.parse_args()

    print("="*60)
    print("🚀 WORLDPOSTA AUTOMATION SUITE")
    print("📌 Full Registration → Email Verification → Login Workflow")
    print("="*60)

    try:
        run_automation(headless=args.headless, use_random=args.random)

    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")


if __name__ == "__main__":
    main()
