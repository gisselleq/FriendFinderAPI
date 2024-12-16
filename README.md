# FriendFinderAPI: AI-Driven Matchmaking

## Overview
The FriendFinderAPI is a project that was designed to help users find friends based on their shared interests.

---

## Features
- **AI-Powered Matchmaking**: Uses the Sentences Transformer model to analyze user bios and generate embeddings. 
- **Cosine Similarity**: Matches users by calculating the closeness of their embeddings, making sure that the connections are similar.
- **Simple API Workflow**: Includes two primary endpoints for user registration and friend suggestions.

---

## Technology Used
- **Programming Language**: Python
- **Framework**: Flask
- **Libraries**: Sentence Transformers
**Embedding Model**: all-MiniLM-L6-v2

---

**How it Works**
1. **User Registration**:
   User submits their profile (name, bio, and interests).
   The bio is then processed into a 384-dimensional embedding vector using Sentence Transformers.
   User data and embeddings are stored in a 'users.json' file.

2. **Friend Suggestions**:
   A user's embedding is compared to others in the databased using cosine similiarity.
   Similarity scores are calculated, ranked, and returned as a list of potential matches.

---

## Installation and Setup
### Prerequisites
- Python 3.7+
- Flask
- Sentence Transformers Library

---

## API Endpoints
### **1. Register a User**
**Endpoint**: `/register`

**Method**: POST

**Input**:
```json
{
  "user_id": "11",
  "name": "Bob Smith",
  "bio": "I love programming and gaming.",
  "interests": ["tech", "games"]
}
```

**Output**:
```json
{
  "message": "User Bob Smith registered successfully!"
}
```


### **2. Get Friend Suggestions**
**Endpoint**: `/suggestions/<user_id>`

**Method**: GET

**Output**:
```json
[
  {
    "user_id": "12",
    "name": "Alice Johnson",
    "similarity_score": 0.89
  },
  {
    "user_id": "13",
    "name": "Charlie Brown",
    "similarity_score": 0.75
  }
]
```
---

## References
- [Sentence Transformers Documentation](https://www.sbert.net/)
- [Flask Documentation](https://flask.palletsprojects.com/en/stable/)

---

## Author
**Gisselle Quiroz**
- Contact: gquiroz@lamar.edu



