import os
from dotenv import load_dotenv

load_dotenv()

print("Key:", os.getenv("TRELLO_API_KEY"))
print("Token:", os.getenv("TRELLO_TOKEN"))
