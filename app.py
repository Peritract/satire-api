# Required imports

import json

import web
from web import form

from scripts.prediction import predict

# App routes

# Start the app

if __name__ == "__main__":

    # Test prediction functionality
    print(predict("Mom Who Spent 25 Years Trying to Change You Doesn’t Understand Why You’re Not More Confident"))