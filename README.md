# WorldPosta Automation Bot

🤖 Full automation workflow for WorldPosta registration, email verification, and login.

## Features

✅ **Complete Workflow:**
1. Register new user account
2. Login to email inbox
3. Find verification email
4. Extract and click verification link
5. Login to website after activation
6. Click "View Posta" and "View CloudEdge" buttons
7. Take screenshots at each step
8. Log results to CSV and JSON

✅ **Human-Like Behavior:**
- Random delays between actions
- Character-by-character typing with random speed
- Mouse movement simulation
- Realistic scrolling
- Undetected ChromeDriver to avoid bot detection

✅ **Robust Error Handling:**
- Comprehensive try/except blocks
- Screenshot capture on errors
- Detailed error logging
- Multiple selector attempts
- Graceful fallbacks

✅ **Result Tracking:**
- CSV file with all attempts
- JSON file with detailed logs
- Screenshots saved for each major step
- Timestamps for all events

## Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Ensure Chrome Browser is Installed

The script uses Chrome browser. Make sure you have Google Chrome installed on your system.

## Configuration

Edit the configuration section at the top of `worldposta_automation.py`:

```python
# Screenshot directory (Windows path)
SCREENSHOT_DIR = r"C:\Users\olaaa\Desktop\Projects\Registeration\SS"

# Email wait timeout (seconds)
EMAIL_WAIT_TIMEOUT = 300  # 5 minutes

# CSV and JSON output files
CSV_FILE = "registration_results.csv"
JSON_FILE = "registration_results.json"
```

## Usage

### Option 1: Auto-Generated Test Data (Default)

Run the script and it will generate random test accounts:

```bash
python worldposta_automation.py
```

The bot will:
- Generate random full name, company, phone, password
- Create email like: `testuser20250123_145623_1234@worldposta.com`
- Complete the entire workflow automatically

### Option 2: Custom Account Data

Edit the script and uncomment the custom data section in `if __name__ == "__main__"`:

```python
# Option 2: Run with custom account data
custom_data = {
    'full_name': "John Doe",
    'email': "john.doe@worldposta.com",
    'company': "Acme Corp",
    'phone': "+15551234567",
    'password': "SecurePass@123"
}
success = bot.run_full_workflow(custom_data)
```

### Option 3: Loop Through Multiple Accounts

To test multiple accounts in sequence, modify the main section:

```python
if __name__ == "__main__":
    bot = WorldPostaAutomationBot(headless=False)

    # Run 5 test registrations
    for i in range(5):
        print(f"\n{'='*60}")
        print(f"🔄 RUNNING TEST {i+1}/5")
        print(f"{'='*60}")

        success = bot.run_full_workflow()

        if not success:
            print(f"⚠️  Test {i+1} failed")

        # Wait between tests
        time.sleep(30)

    bot.close()
```

## Output Files

### 1. Screenshots (`SS` folder)

All screenshots are saved with descriptive names:

- `email_registration_timestamp.png` - After registration form submission
- `email_email_login_timestamp.png` - After email login
- `email_email_found_timestamp.png` - When verification email is found
- `email_email_confirmed_timestamp.png` - After email confirmation
- `email_website_login_timestamp.png` - After website login
- `email_view_posta_timestamp.png` - After clicking View Posta
- `email_view_cloudedge_timestamp.png` - After clicking View CloudEdge
- `email_final_success_timestamp.png` - Final screenshot
- `email_*_error_timestamp.png` - Error screenshots

### 2. CSV File (`registration_results.csv`)

Columns:
- `timestamp` - When the attempt was made
- `email` - Email address used
- `status` - Result status (success, failed_*, etc.)
- `error_message` - Error details if failed
- `screenshot_path` - Path to final screenshot

### 3. JSON File (`registration_results.json`)

Same data as CSV but in JSON format for easier programmatic access.

## Status Codes

- `success` - Complete workflow succeeded
- `failed_registration` - Registration form submission failed
- `failed_email_login` - Could not login to email
- `failed_email_not_found` - Verification email not found within timeout
- `failed_no_verification_link` - Could not extract verification link
- `failed_email_confirmation` - Could not confirm email
- `failed_website_login` - Could not login to website
- `failed_post_login_actions` - Could not click post-login buttons
- `failed_unexpected_error` - Unexpected error occurred

## Troubleshooting

### Browser Detection / CAPTCHA

If the site detects automation:
1. Script uses `undetected-chromedriver` to avoid detection
2. Random delays mimic human behavior
3. Human-like mouse movements and typing
4. If CAPTCHA appears, solve it manually in the visible browser window

### Email Not Found

If verification email doesn't arrive:
1. Check spam folder (script searches all folders)
2. Increase `EMAIL_WAIT_TIMEOUT` in configuration
3. Verify email was registered correctly
4. Check email inbox selectors are correct

### Selector Issues

If elements not found:
1. Website HTML may have changed
2. Update selectors in the script
3. Use browser DevTools to inspect elements
4. Check console output for specific errors

### Screenshot Path Issues (Windows)

Make sure the path uses raw string `r"C:\path\to\folder"` or forward slashes `"C:/path/to/folder"`

## Advanced Customization

### Change Browser Mode

Headless mode (browser hidden):
```python
bot = WorldPostaAutomationBot(headless=True)
```

Visible mode (default):
```python
bot = WorldPostaAutomationBot(headless=False)
```

### Adjust Wait Times

Edit timeouts in the script:
```python
DEFAULT_TIMEOUT = 30  # WebDriverWait timeout
EMAIL_WAIT_TIMEOUT = 300  # Email arrival timeout
```

### Add More Actions

Add custom actions after login in the `perform_post_login_actions()` method:

```python
def perform_post_login_actions(self):
    # Existing code...

    # Add your custom actions here
    print("🔍 Clicking custom button...")
    custom_button = self.driver.find_element(By.CSS_SELECTOR, 'button.my-custom-button')
    custom_button.click()
    random_delay(2, 4)
```

## Code Structure

### Main Class: `WorldPostaAutomationBot`

**Methods:**
- `register()` - Handle registration form
- `login_to_email()` - Login to webmail
- `find_verification_email()` - Search inbox for verification email
- `extract_verification_link()` - Extract confirmation URL from email
- `confirm_email()` - Navigate to confirmation URL
- `login_to_website()` - Login to website after activation
- `perform_post_login_actions()` - Click buttons after login
- `take_final_screenshot()` - Capture final result
- `save_status()` - Log to CSV/JSON
- `run_full_workflow()` - Orchestrate entire process

### Utility Functions (Reused from Original Script)

- `random_delay()` - Human-like pauses
- `human_like_mouse_move()` - Realistic mouse movement
- `human_like_typing()` - Character-by-character typing
- `generate_test_data()` - Create random account info
- `get_timestamp()` - Formatted timestamps
- `get_screenshot_filename()` - Generate screenshot names

## Best Practices

1. **Test with visible browser first** to see what's happening
2. **Check screenshots** if workflow fails to debug issues
3. **Review CSV/JSON logs** to track success/failure patterns
4. **Use random delays** to avoid detection
5. **Keep Chrome updated** for compatibility with undetected-chromedriver

## Security Notes

⚠️ **Important:**
- This script stores passwords in plain text
- Do not commit credentials to version control
- Use environment variables for production
- Test accounts should use temporary passwords

## Support

If you encounter issues:
1. Check the error message in console output
2. Review the error screenshot
3. Check CSV/JSON logs for detailed status
4. Verify selectors haven't changed on the website
5. Ensure Chrome browser is up to date

## License

This is a custom automation script for internal use.

---

**Happy Automating! 🚀**
