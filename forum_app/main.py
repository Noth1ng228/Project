from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from bd import db, Post, Reply

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'super_secret_key_123'

db.init_app(app)

with app.app_context():
    db.create_all()


ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "Password_123"


@app.route('/')
def index():
    posts = Post.query.order_by(Post.id.desc()).all()
    added_count = session.get('added_count', 0)
    logged_in = session.get('logged_in', False)
    return render_template('index.html', posts=posts, added_count=added_count, logged_in=logged_in)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Invalid username or password.")
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))


# post 
@app.route('/add_ajax', methods=['POST'])
def add_ajax():
    data = request.get_json()
    content = data.get('content', '').strip()
    if not content:
        return jsonify({'status': 'error', 'message': 'The entry can’t be empty.'})

    new_post = Post(content=content)
    db.session.add(new_post)
    db.session.commit()

    session['added_count'] = session.get('added_count', 0) + 1
    return jsonify({'status': 'success', 'content': content, 'id': new_post.id, 'added_count': session['added_count']})


@app.route('/delete_ajax/<int:id>', methods=['DELETE'])
def delete_ajax(id):
    if not session.get('logged_in'):
        return jsonify({'status': 'error', 'message': 'Unauthorized access.'})

    post = Post.query.get(id)
    if not post:
        return jsonify({'status': 'error', 'message': 'The entry not found.'})
    db.session.delete(post)
    db.session.commit()
    return jsonify({'status': 'success', 'id': id})


@app.route('/edit_ajax/<int:id>', methods=['PUT'])
def edit_ajax(id):
    if not session.get('logged_in'):
        return jsonify({'status': 'error', 'message': 'Unauthorized access.'})

    data = request.get_json()
    content = data.get('content', '').strip()
    post = Post.query.get(id)
    if not post:
        return jsonify({'status': 'error', 'message': 'The entry not found.'})
    if not content:
        return jsonify({'status': 'error', 'message': 'The entry can’t be empty.'})
    post.content = content
    db.session.commit()
    return jsonify({'status': 'success', 'id': id, 'content': content})



@app.route('/add_reply/<int:post_id>', methods=['POST'])
def add_reply(post_id):
    data = request.get_json()
    content = data.get('content', '').strip()
    if not content:
        return jsonify({'status': 'error', 'message': 'The reply can’t be empty.'})

    reply = Reply(content=content, post_id=post_id)
    db.session.add(reply)
    db.session.commit()

    return jsonify({'status': 'success', 'content': reply.content, 'id': reply.id, 'post_id': post_id})


@app.route('/delete_reply/<int:id>', methods=['DELETE'])
def delete_reply(id):
    if not session.get('logged_in'):
        return jsonify({'status': 'error', 'message': 'Unauthorized access'})

    reply = Reply.query.get(id)
    if not reply:
        return jsonify({'status': 'error', 'message': 'Reply not found'})

    db.session.delete(reply)
    db.session.commit()
    return jsonify({'status': 'success', 'id': id})


@app.route('/edit_reply/<int:id>', methods=['PUT'])
def edit_reply(id):
    if not session.get('logged_in'):
        return jsonify({'status': 'error', 'message': 'Unauthorized access'})

    data = request.get_json()
    content = data.get('content', '').strip()
    reply = Reply.query.get(id)
    if not reply:
        return jsonify({'status': 'error', 'message': 'Reply not found'})
    if not content:
        return jsonify({'status': 'error', 'message': 'The reply can’t be empty'})
    reply.content = content
    db.session.commit()
    return jsonify({'status': 'success', 'id': id, 'content': content})


if __name__ == '__main__':
    app.run(debug=True)
