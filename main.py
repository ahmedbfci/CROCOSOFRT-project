import os
from dotenv import load_dotenv
import mysql.connector
from flask import Flask, request, jsonify

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)


def get_db():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )

@app.route('/posts', methods=['POST'])
def add_post():
    db = get_db()
    cursor = db.cursor()
    user_id = request.json['user_id']
    content = request.json['content']
    cursor.execute("INSERT INTO Post (user_id, content) VALUES (%s, %s)", (user_id, content))
    db.commit()
    cursor.close()
    db.close()
    return jsonify({'message': 'Post added successfully'}), 201

@app.route('/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    db = get_db()
    cursor = db.cursor()
    content = request.json['content']
    cursor.execute("UPDATE Post SET content = %s WHERE id = %s", (content, post_id))
    db.commit()
    cursor.close()
    db.close()
    return jsonify({'message': 'Post updated successfully'}), 200

@app.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM Post WHERE id = %s", (post_id,))
    db.commit()
    cursor.close()
    db.close()
    return jsonify({'message': 'Post deleted successfully'}), 200

@app.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Post WHERE id = %s", (post_id,))
    post = cursor.fetchone()
    cursor.close()
    db.close()
    if post:
        return jsonify({
            'id': post[0],
            'user_id': post[1],
            'content': post[2],
            'timestamp': post[3]
        }), 200
    else:
        return jsonify({'message': 'Post not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)