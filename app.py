from flask import Flask, render_template, request, redirect
import pymysql
import pymysql.cursors

app = Flask(__name__)

DB_CONFIG = {
    'host': 'db',
    'user': 'root',
    'password': 'password',
    'database': 'tododb',
    'cursorclass': pymysql.cursors.DictCursor
}

def get_db():
    return pymysql.connect(**DB_CONFIG)

@app.route('/')
def index():
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM tasks ORDER by jadwal ASC")
        tasks = cur.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    task = request.form['task']
    jadwal = request.form['jadwal']

    
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute("INSERT INTO tasks (title,jadwal) VALUES (%s, %s)", (task, jadwal))
        conn.commit()
    conn.close()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute("DELETE FROM tasks WHERE id = %s", (id,))
        conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)