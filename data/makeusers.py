import json
from faker import Faker
import random
from sentence_transformers import SentenceTransformer

fake = Faker()
model = SentenceTransformer('all-MiniLM-L6-v2')

interest_pool= [
    "gaming","music","sports","movies","reading","cooking","traveling","photography","fashion","art","technology","programming","design","writing","dancing","singing","yoga","meditation","hiking","cycling","swimming","running","weightlifting"
    ,"knitting", "woodworking", "pottery", "origami", "cosplay",
]


bio_templates = [
    "I love {interest1} and {interest2} during my free time.",
    "Exploring {interest1} and learning about {interest2} are my passions.",
    "I enjoy {interest1}, and I am always eager to try new things like {interest2}.",
    "My favorite activities are {interest1} and {interest2}.",
    "When I am not working, I am usually enjoying {interest1} or {interest2}.",
    "I am passionate about {interest1} and have recently started exploring {interest2}.",
    "I am deeply curious about {interest1} and have been enjoying {interest2} as a new hobby.",
    "You can catch me enjoying {interest1} or discovering more about {interest2}.",
    "Balancing {interest1} with a touch of {interest2} is how I unwind.",
    "For me, {interest1} is a way of life, and {interest2} adds a spark of adventure."
]

def generate_users(num_users):
    users = {}
    for user_id in range(1, num_users+1):
        selected_interests = random.sample(interest_pool, 2)
        bio = random.choice(bio_templates).format(interest1=selected_interests[0], interest2=selected_interests[1])

        embeddings = model.encode(bio).tolist()

        user = {
            "id": str(user_id),
            "name": fake.name(),
            "bio": bio,
            "interests": selected_interests,
            'embeddings': embeddings

        }
        users[user_id] = user
    return users

# number of users that are gunna be generated
num_users = 10

# put users in json file
users = generate_users(num_users)
with open('data/users.json', 'w') as f:
    json.dump(users, f, indent=4)

print(f"{num_users} users generated and saved to data/users.json")