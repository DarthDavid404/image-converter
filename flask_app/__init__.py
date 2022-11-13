from flask import Flask
from dotenv import load_dotenv
load_dotenv()
import os
app = Flask(__name__)
app.secret_key = os.getenv("superSecretKey")