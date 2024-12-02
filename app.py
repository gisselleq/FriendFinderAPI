from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer, util
import json

app = Flask(__name__)

# pre trained embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# in mem database
users = {}

@app.route('/')
def home():
    return "Welcome to A-FriendFinder API! Available routes: /register, /suggestions/<user_id>"



# register a new user
@app.route('/register', methods=['POST'])
def register():
    try:
       
        print(f"Request JSON: {request.json}")

        
        if not request.is_json:
            return jsonify({"error": "Request must be JSON. Ensure Content-Type is application/json."}), 400

        data = request.json

       # make sure input data has everything 
        required_keys = ['user_id', 'name', 'bio', 'interests']
        missing_keys = [key for key in required_keys if key not in data]

        if missing_keys:
            return jsonify({"error": f"Missing keys in request: {missing_keys}"}), 400

        user_id = data['user_id']
        try:
                with open('data/users.json', 'r') as f:
                    users = json.load(f)
        except FileNotFoundError:
            users = {}
        except json.JSONDecodeError:
            return jsonify({"error": "Invalid JSON format in request."}), 500
            
  

      

        # see if user_id already exists
        if user_id in users:
            return jsonify({"error": f"User with id {user_id} already exists."}), 409

        # Add user to database (in-memory for now)
        users[user_id] = {
            "name": data['name'],
            "bio": data['bio'],
            "interests": data['interests'],
        }


        with open('data/users.json', 'w') as f:
            json.dump(users, f, indent=4)

        return jsonify({"message": f"User {name} registered successfully!"}), 201

    except Exception as e:
        # Catch unexpected errors
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

    # suggestions
@app.route('/suggestions', methods=['GET'])
def get_suggestions(user_id):
    if user_id not in users:
        return jsonify({'message': 'User does not exist'}), 400

    user_data = users[user_id]
    user_embeddings = user_data['embeddings']

    # compute similarity scores
    suggestions = []
      
    for other_user_id, other_user_data in users.items():
        if other_user_id == user_id:
            continue

        similarity = util.cos_sim(user_embeddings, other_user_data['embeddings']).item()
        suggestions.append({
            'id': other_user_id,
            'name': other_user_data['name'],
            'score': similarity
        })
    
    # sort the suggestions by score
    suggestions = sorted(suggestions, key=lambda x: x['score'], reverse=True)

    return jsonify(suggestions), 200

   
   

if __name__ == '__main__':
    app.run(debug=True)