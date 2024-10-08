from flask import Flask

app = Flask(__name__)

# Import routes
from customer_api import routes
