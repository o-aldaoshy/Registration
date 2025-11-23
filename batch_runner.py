"""
Batch runner for multiple account registrations
Reads account data from CSV and processes each one
"""

import csv
import time
from worldposta_automation import WorldPostaAutomationBot, random_delay

# Configuration
INPUT_CSV = "accounts_to_register.csv"  # CSV with account data
DELAY_BETWEEN_ACCOUNTS = (60, 120)  # Seconds to wait between accounts (min, max)
HEADLESS_MODE = False  # Set to True to hide browser


def read_accounts_from_csv(filename):
    """
    Read account data from CSV file

    Expected CSV format:
    full_name,email,company,phone,password
    John Doe,john@worldposta.com,Acme Corp,+15551234567,SecurePass123
    """
    accounts = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                accounts.append({
                    'full_name': row['full_name'],
                    'email': row['email'],
                    'company': row['company'],
                    'phone': row['phone'],
                    'password': row['password']
                })
        print(f"✅ Loaded {len(accounts)} accounts from {filename}")
        return accounts
    except FileNotFoundError:
        print(f"❌ File not found: {filename}")
        print(f"📝 Creating sample CSV file...")
        create_sample_csv(filename)
        return []
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        return []


def create_sample_csv(filename):
    """Create a sample CSV file with the correct format"""
    sample_data = [
        {
            'full_name': 'John Doe',
            'email': 'john.doe@worldposta.com',
            'company': 'Acme Corp',
            'phone': '+15551234567',
            'password': 'SecurePass@123'
        },
        {
            'full_name': 'Jane Smith',
            'email': 'jane.smith@worldposta.com',
            'company': 'TechCorp',
            'phone': '+15559876543',
            'password': 'SecurePass@456'
        }
    ]

    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['full_name', 'email', 'company', 'phone', 'password'])
        writer.writeheader()
        for row in sample_data:
            writer.writerow(row)

    print(f"✅ Sample CSV created: {filename}")
    print(f"📝 Edit this file with your account data and run again")


def run_batch_automation():
    """Run automation for multiple accounts"""
    print("="*60)
    print("🚀 WORLDPOSTA BATCH AUTOMATION")
    print("="*60)

    # Read accounts from CSV
    accounts = read_accounts_from_csv(INPUT_CSV)

    if not accounts:
        print("\n⚠️  No accounts to process. Exiting.")
        return

    total_accounts = len(accounts)
    successful = 0
    failed = 0

    print(f"\n📊 Total accounts to process: {total_accounts}")
    print(f"⏱️  Delay between accounts: {DELAY_BETWEEN_ACCOUNTS[0]}-{DELAY_BETWEEN_ACCOUNTS[1]} seconds")
    print(f"🖥️  Headless mode: {'Enabled' if HEADLESS_MODE else 'Disabled'}")

    bot = None

    try:
        # Initialize bot once for all accounts
        bot = WorldPostaAutomationBot(headless=HEADLESS_MODE)

        for idx, account_data in enumerate(accounts, 1):
            print("\n" + "#"*60)
            print(f"🔄 PROCESSING ACCOUNT {idx}/{total_accounts}")
            print("#"*60)
            print(f"📧 Email: {account_data['email']}")
            print(f"👤 Name: {account_data['full_name']}")
            print(f"🏢 Company: {account_data['company']}")

            # Run workflow for this account
            try:
                success = bot.run_full_workflow(account_data)

                if success:
                    successful += 1
                    print(f"✅ Account {idx}/{total_accounts} completed successfully")
                else:
                    failed += 1
                    print(f"❌ Account {idx}/{total_accounts} failed")

            except Exception as e:
                failed += 1
                print(f"❌ Account {idx}/{total_accounts} failed with error: {e}")

            # Wait before next account (if not last)
            if idx < total_accounts:
                wait_time = random_delay(DELAY_BETWEEN_ACCOUNTS[0], DELAY_BETWEEN_ACCOUNTS[1])
                print(f"\n⏳ Waiting before next account...")
                time.sleep(wait_time)

        # Final summary
        print("\n" + "="*60)
        print("📊 BATCH AUTOMATION COMPLETE")
        print("="*60)
        print(f"✅ Successful: {successful}/{total_accounts}")
        print(f"❌ Failed: {failed}/{total_accounts}")
        print(f"📁 Results saved to: registration_results.csv and registration_results.json")
        print("="*60)

        # Keep browser open for inspection
        if not HEADLESS_MODE:
            print("\n⏸️  Browser will stay open. Press ENTER to close...")
            input("Press ENTER to close browser and exit...")

    except KeyboardInterrupt:
        print("\n⚠️  Batch processing interrupted by user")
        print(f"📊 Processed: {successful + failed}/{total_accounts}")
        print(f"✅ Successful: {successful}")
        print(f"❌ Failed: {failed}")
    except Exception as e:
        print(f"\n❌ Fatal error in batch runner: {e}")
    finally:
        if bot:
            bot.close()


if __name__ == "__main__":
    run_batch_automation()
