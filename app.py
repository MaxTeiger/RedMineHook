import redmine_api
import config
from flask import Flask, request
from flask_restful import Resource, Api
from gevent.pywsgi import WSGIServer
from flask_api import status
import hmac
import hashlib

app = Flask(__name__)
api = Api(app)

print("app.py found !")

#Compare the HMAC hash signature
def verify_hmac_hash(data, signature):

    GitHub_secret = bytes(config.SECRET_TOKEN.encode('UTF-8'))
    mac = hmac.new(GitHub_secret, msg=data, digestmod=hashlib.sha1)
    mysignature = "sha1=" +str(mac.hexdigest())
    print("My signature :" +mysignature)
    return hmac.compare_digest(mysignature, str(signature))
    

# For dev, the complete URL was http://574173cf.ngrok.io/payload (use ngrok to make our 
# localhost port 5000 (default) public)
@app.route('/payload', methods=['GET', 'POST'])
def testFlask():
    # The Github Webhook use a POST method to send informations about the repo and the action which enable the webhook
    if request.method == 'POST': 

        # We ensure the request is send in JSON format
        print (request.is_json)        
        
        # We retrieve the JSON object received and store it in a dictionnary (default)
        content = request.get_json()

        #we retrieve the signature of the request
        signature = request.headers.get('X-Hub-Signature')
        print("Signature received : " + str(signature))
        
        
        data = request.data


        if verify_hmac_hash(data, signature):
            
            # We retrieve the html url of the pull request  
            pullURL = content['pull_request']['html_url']
        
            # Retrieve the body of the pull request (in order to know the fix id)
            if content['pull_request']['body'] != "":
                pullBody = content['pull_request']['body']
            else:
                pullBody = "Nothing specified #123456789"

            print("Pull URL : " +str(pullURL))
            print("Pull Body (must contain #fixnumber):" +str(pullBody))

            # We call the webscrapping function which retrieve the fix number of the pull request 
            return redmine_api.updateIssueOnRedMineFromGit(pullBody, pullURL)
        
        else: 
            print("Well yes, but no")
            return "Well yes, but no", status.HTTP_403_FORBIDDEN

    # If going on this route directly through the browser 
    elif request.method == 'GET':
        return 'Hello World! (sorry you are probably on a wrong route)'

# # If you want to change default port number enable this line 
# app.run(host='0.0.0.0', port= 5000)

if __name__ == '__main__':
    # Debug/Development
    # app.run(debug=True, host="0.0.0.0", port="5000")

    # Production
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()