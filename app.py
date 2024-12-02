from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer, util

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
    data = request.get_json()
    user_id = data['user_id']
    name = data['name']
    bio = data['bio']
    interests = data['interests']  


    if user_id in users:
        return jsonify({'message': 'User already exists'}), 400

    users[user_id] = {
        'name': name,
        'bio': bio,
        'embeddings': model.encode(bio),
        'interests': interests,

    }


    return jsonify({'message': 'User registered successfully'}), 201

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