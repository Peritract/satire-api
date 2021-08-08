# Required imports

import json

import web
from web import form

from scripts.prediction import predict

# Use HTML templates

render = web.template.render('templates')

# Mock-up authentication

valid_keys = [
    'test-123-456-789'
]

# Create error classes to raise

class NoAPIKey(web.HTTPError):
    def __init__(self):
        status = '400 Bad request'
        web.header('Content-Type', 'application/json')
        data = json.dumps({'error': 'No API key provided.'})
        web.HTTPError.__init__(self, status=status, data=data)

class InvalidAPIKey(web.HTTPError):
    def __init__(self):
        status = '400 Bad request'
        web.header('Content-Type', 'application/json')
        data = json.dumps({'error': 'Invalid API key provided'})
        web.HTTPError.__init__(self, status=status, data=data)

class NoTextProvided(web.HTTPError):
    def __init__(self):
        status = '400 Bad request'
        web.header('Content-Type', 'application/json')
        data = json.dumps({'error': 'No text data provided'})
        web.HTTPError.__init__(self, status=status, data=data)

# Set up the routes

routes = ('/api/', 'Index',
          '/api/verify', 'Verify',
          '/api/predict', 'Predict',
          '/predict', 'PredictForm')

# Create the endpoints for routes to connect to

class Index:
    def GET(self):
        return 'This API provides satire-detection services in news headlines.'


class Verify:
    def GET(self):

        # Get the params
        params = web.input()

        if 'api_key' in params:
            
            if params['api_key'] in valid_keys:
                web.header('Content-Type', 'application/json')
                return json.dumps({'success': 'API key successfully authenticated.'})

            else:
                raise InvalidAPIKey()
        
        else:
            raise NoAPIKey()


class Predict:
    def GET(self):

        # Get the params
        params = web.input()

        if 'text' not in params:
            raise NoTextProvided()

        elif 'api_key' in params:

            if params['api_key'] not in valid_keys:
                raise InvalidAPIKey()

            else:
                result = predict(params['text'], premium=True)
                web.header('Content-Type', 'application/json')
                return json.dumps({"text": params['text'],
                        "prediction": result[0],
                        "confidence": result[1]})

        else:
            result = predict(params['text'])
            web.header('Content-Type', 'application/json')
            return json.dumps({"text": params['text'],
                               "prediction": result})

# Create the human-facing routes

user_form = form.Form(form.Textbox("text",
                                   form.notnull,
                                   description="Headline",
                                   attrs={'required': True}),
                      form.Button("submit", type="submit",
                                  description="Is it satire?")
                     )

class PredictForm:
    def GET(self):
        f = user_form()
        return render.predict(f)

    def POST(self):
        f = user_form()
        if not f.validates():
            return render.predict(f)
        params = web.input()
        result = predict(params['text'])
        if result == 'satirical':
            return render.satirical()
        else:
            return render.not_satirical()

# Start the app

if __name__ == "__main__":

    # Create an application with the routes set up
    app = web.application(routes, globals())

    # Run the app
    app.run()