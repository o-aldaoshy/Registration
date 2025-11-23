"""
Test runner with your specific account data
"""

from worldposta_automation import WorldPostaAutomationBot

# Your specific test account data
ACCOUNT_DATA = {
    'full_name': "AI dexter85",
    'email': "ai.dexter85@worldposta.com",
    'company': "AI Company dexter85",
    'phone': "1095666032",
    'password': "gtzwO@lvr+A82biD5Xdme pf7k/*y1"
}

if __name__ == "__main__":
    print("="*60)
    print("🚀 WORLDPOSTA AUTOMATION - CUSTOM TEST DATA")
    print("="*60)
    print(f"\n📋 Using account:")
    print(f"   Email: {ACCOUNT_DATA['email']}")
    print(f"   Name: {ACCOUNT_DATA['full_name']}")
    print(f"   Company: {ACCOUNT_DATA['company']}")
    print(f"   Phone: {ACCOUNT_DATA['phone']}")
    print("="*60)

    bot = None

    try:
        # Initialize bot (visible browser for debugging)
        bot = WorldPostaAutomationBot(headless=False)

        # Run workflow with your specific data
        success = bot.run_full_workflow(ACCOUNT_DATA)

        if success:
            print("\n✨ Automation completed successfully!")
        else:
            print("\n⚠️  Automation completed with errors. Check logs for details.")

        # Keep browser open for inspection
        print("\n⏸️  Browser will stay open. Press ENTER to close...")
        input("Press ENTER to close browser and exit...")

    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
    finally:
        if bot:
            bot.close()
