from app.gmail_client import GmailClient


if __name__ == '__main__':
    client = GmailClient()
    client.get_labels()
