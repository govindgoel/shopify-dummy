from flask import Flask, request
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask_cors import CORS

uri =  "<MONGO_URI>"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


app = Flask(__name__)

CORS(app)


  
@app.route("/")
def hello():
    return "Hello There"

@app.route('/subscribe', methods=['POST'])
def post_to_database():
    email = request.headers["Email"]
    print(email)

    if not email:
        return "No email provided"
    
    client.db.emails.insert_one({'email': email})

    return "Success"
    
    
@app.route('/getemails', methods=['GET'])
def get_emails():
    if request.headers['token'] == '<token>':
        emails = client.db.emails.find()
        email_list = []
        for email in emails:
            email_list.append(email['email'])
        return {'emails': email_list}
    else:
        return "Invalid Request"


  
if __name__ == "__main__":
  app.run(host='0.0.0.0')  
