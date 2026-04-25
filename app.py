from flask import Flask, render_template, request, redirect
import pymysql
import pymysql.cursors
import re

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
    return render_template('index.html', tasks=get_tasks(), error = None)

@app.route('/add', methods=['POST'])
def add():
    task = request.form.get('task', '').strip()
    jadwal = request.form.get('jadwal', '').strip()

    # validasi task tidak boleh kosong
    if not task:
        return render_template('index.html', 
            error="Nama kegiatan tidak boleh kosong!",
            tasks=get_tasks())

    # validasi format jadwal HH:MM
    pola = r'^\d{2}:\d{2}$'
    if not re.match(pola, jadwal):
        return render_template('index.html',
            error="Format jadwal tidak valid! Gunakan format HH:MM (contoh: 09:00)",
            tasks=get_tasks())

    # validasi jam dan menit masuk akal
    jam, menit = jadwal.split(':')
    if not (0 <= int(jam) <= 23 and 0 <= int(menit) <= 59):
        return render_template('index.html',
            error="Jam harus 00-23 dan menit harus 00-59!",
            tasks=get_tasks())

    conn = get_db()
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO tasks (title, jadwal) VALUES (%s, %s)",
            (task, jadwal)
        )
        conn.commit()
    conn.close()
    return redirect('/')

def get_tasks():
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM tasks ORDER BY jadwal ASC")
        tasks = cur.fetchall()
    conn.close()
    return tasks

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