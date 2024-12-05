from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os.path
import pickle
import base64
from email.mime.text import MIMEText
import html2text
import json

class GmailManager:
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
        self.current_account = self.get_current_account()
    
    def get_current_account(self):
        """Read current account from config"""
        try:
            with open('gmail_config.json', 'r') as f:
                config = json.load(f)
                return config.get('current_account', 'default')
        except FileNotFoundError:
            self.save_config('default')
            return 'default'
    
    def save_config(self, account_name):
        """Save current account to config"""
        with open('gmail_config.json', 'w') as f:
            json.dump({'current_account': account_name}, f)
    
    def get_token_path(self):
        """Get token path for current account"""
        return f'token_{self.current_account}.pickle'
    
    def switch_account(self, account_name=None):
        """Switch to a different account or force new login"""
        if account_name:
            self.current_account = account_name
            self.save_config(account_name)
        
        # Remove existing token to force new login
        token_path = self.get_token_path()
        if os.path.exists(token_path):
            os.remove(token_path)
        
        # Test new connection
        return self.get_latest_emails()
    
    def list_accounts(self):
        """List all accounts that have tokens saved"""
        accounts = []
        for file in os.listdir():
            if file.startswith('token_') and file.endswith('.pickle'):
                account = file.replace('token_', '').replace('.pickle', '')
                accounts.append(account)
        return accounts

    def get_credentials(self):
        """Get credentials for current account"""
        creds = None
        token_path = self.get_token_path()

        # Try to load existing credentials
        if os.path.exists(token_path):
            with open(token_path, 'rb') as token:
                creds = pickle.load(token)

        # If no valid credentials available, let user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                print(f"Please log in for account: {self.current_account}")
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
                
                # Save credentials for future use
                with open(token_path, 'wb') as token:
                    pickle.dump(creds, token)

        return creds

    def get_latest_emails(self):
        """Get latest 5 emails for current account"""
        try:
            creds = self.get_credentials()
            service = build('gmail', 'v1', credentials=creds)
            
            results = service.users().messages().list(
                userId='me',
                labelIds=['INBOX'],
                maxResults=5
            ).execute()
            
            messages = results.get('messages', [])
            email_summaries = []
            
            if messages:
                for message in messages:
                    msg = service.users().messages().get(
                        userId='me', 
                        id=message['id'],
                        format='full'
                    ).execute()
                    
                    headers = msg['payload']['headers']
                    subject = next(h['value'] for h in headers if h['name'].lower() == 'subject')
                    sender = next(h['value'] for h in headers if h['name'].lower() == 'from')
                    
                    try:
                        if 'parts' in msg['payload']:
                            parts = msg['payload']['parts']
                            data = parts[0]['body']['data']
                        else:
                            data = msg['payload']['body']['data']
                        
                        text = base64.urlsafe_b64decode(data).decode()
                        h = html2text.HTML2Text()
                        h.ignore_links = True
                        text = h.handle(text)
                        preview = text[:100] + "..." if len(text) > 100 else text
                        
                    except Exception as e:
                        preview = "Could not extract email content"
                    
                    email_summaries.append({
                        'subject': subject,
                        'from': sender,
                        'preview': preview
                    })
                    
            return {
                'account': self.current_account,
                'emails': email_summaries
            }
            
        except Exception as e:
            print(f"Error accessing Gmail: {str(e)}")
            return None

def check_new_mail(account=None):
    """Check emails, optionally switching accounts first"""
    gmail = GmailManager()
    
    if account:
        result = gmail.switch_account(account)
    else:
        result = gmail.get_latest_emails()
    
    if result:
        summary = f"Emails for account '{result['account']}':\n\n"
        for i, email in enumerate(result['emails'], 1):
            summary += f"{i}. From: {email['from']}\n"
            summary += f"   Subject: {email['subject']}\n"
            summary += f"   Preview: {email['preview']}\n\n"
        return summary
    else:
        return "Could not retrieve emails or no emails found."

def list_mail_accounts():
    """List all saved Gmail accounts"""
    gmail = GmailManager()
    accounts = gmail.list_accounts()
    return f"Available accounts: {', '.join(accounts)}"

# Force new login for current account
def switch_accounts():
    gmail = GmailManager()
    gmail.switch_account()  # Without parameter, forces new login for current account