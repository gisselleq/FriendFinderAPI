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
@app.route('/register', methods=['GET','POST'])
def register():
    global users
    if request.method == 'GET':
        return jsonify({"message": "Please use POST method to register a new user."}), 405
    if request.method == 'POST':
        try:
            if not request.is_json:
                return jsonify({"error": "Request must be JSON. Ensure Content-Type is application/json."}), 400

            data = request.json
            required_keys = ['user_id', 'name', 'bio', 'interests']
            missing_keys = [key for key in required_keys if key not in data]

            if missing_keys:
                return jsonify({"error": f"Missing keys in request: {missing_keys}"}), 400

            user_id = data['user_id']

            # Read current users from the file
            try:
                with open('data/users.json', "r") as file:
                    users = json.load(file)
                print("Successfully loaded users from file.")
            except FileNotFoundError:
                print("Error users.json not found")
                users = {}
            except json.JSONDecodeError:
                return jsonify({"error": "Failed to decode users.json"}), 500

            if user_id in users:
                return jsonify({"error": f"User with id {user_id} already exists."}), 409

            # Add the new user
            users[user_id] = {
                "name": data['name'],
                "bio": data['bio'],
                "interests": data['interests']
            }

            # Save updated users to the file
            with open('data/users.json', "w") as file:
                json.dump(users, file, indent=4)

            return jsonify({"message": f"User {data['name']} registered successfully!"}), 201

        except Exception as e:
            return jsonify({"error": f"Internal server error: {str(e)}"}), 500





    # suggestions
@app.route('/suggestions/<user_id>', methods=['GET'])
def get_suggestions(user_id):
    global users
    
    # get useres from file to ensure consistency
    try: 
        with open('data/users.json', 'r') as file:
            users = json.load(file)
        print("Successfully loaded users from file.")
    except FileNotFoundError:
        print("Error users.json not found")
        users = {}
    except json.JSONDecodeError:
        return jsonify({"error": "Failed to decode users.json"}), 500
    

    # removes any leading or trailing whitespaces
    user_id = user_id.strip()
    print(f"Available user IDs in dictionary: {list(users.keys())}")
    print(f"Received request for suggestions for user_id: {user_id}")


    if user_id not in users:
        print("User not found in users dictionary")
        return jsonify({'message': 'User does not exist'}), 400
    
    user_data = users[user_id]
    print("user found: ", user_data)


    if 'embeddings' not in user_data:
        print("embeddings not found for user", user_id)
        return jsonify({'message': 'User embeddings not found'}), 400

    user_embeddings = user_data['embeddings']
    suggestions = []


    # compute similarity scores
    suggestions = []
      
    for other_user_id, other_user_data in users.items():
        if other_user_id == user_id:
            continue
        if 'embeddings' not in other_user_data:
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