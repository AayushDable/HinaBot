try:
    from youtube_surfer import search_youtube
    from access_gmail import check_new_mail,list_mail_accounts,switch_accounts
    from feedback_mechanisms import get_clarification
    from home_automation import ac_control
    ac_control("off")
    print("Task completed")

except ImportError as e:
    print(f"ImportError: {str(e)}")
except Exception as e:
    print(f"Error: {str(e)}")