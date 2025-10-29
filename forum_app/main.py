from flask import Flask, render_template, request, jsonify, session
from bd import db, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'super_secret_key_123'

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    posts = Post.query.order_by(Post.id.desc()).all()

    added_count = session.get('added_count', 0)
    
    return render_template('index.html', posts=posts, added_count=added_count)

@app.route('/add_ajax', methods=['POST'])
def add_ajax():
    data = request.get_json()
    content = data.get('content', '').strip()
    if not content:
        return jsonify({'status': 'error', 'message': 'The entry cant be empty.'})

    new_post = Post(content=content)
    db.session.add(new_post)
    db.session.commit()

    session['added_count'] = session.get('added_count', 0) + 1

    return jsonify({'status': 'success', 'content': content, 'id': new_post.id, 'added_count': session['added_count']})

@app.route('/delete_ajax/<int:id>', methods=['DELETE'])
def delete_ajax(id):
    post = Post.query.get(id)
    if not post:
        return jsonify({'status': 'error', 'message': 'The entry not findet.'})
    db.session.delete(post)
    db.session.commit()
    return jsonify({'status': 'success', 'id': id})

@app.route('/edit_ajax/<int:id>', methods=['PUT'])
def edit_ajax(id):
    data = request.get_json()
    content = data.get('content', '').strip()
    post = Post.query.get(id)
    if not post:
        return jsonify({'status': 'error', 'message': 'The entry not findet.'})
    if not content:
        return jsonify({'status': 'error', 'message': 'The entry cant be empty.'})
    post.content = content
    db.session.commit()
    return jsonify({'status': 'success', 'id': id, 'content': content})

if __name__ == '__main__':
    app.run(debug=True)
