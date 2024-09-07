from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# إنشاء قاعدة البيانات وجداول المقالات
def init_db():
    conn = sqlite3.connect('articles.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS articles
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, content TEXT)''')
    conn.commit()
    conn.close()

init_db()

# الصفحة الرئيسية لعرض المقالات
@app.route('/')
def index():
    conn = sqlite3.connect('articles.db')
    c = conn.cursor()
    c.execute("SELECT * FROM articles")
    articles = c.fetchall()
    conn.close()
    return render_template('index.html', articles=articles)

# صفحة لإضافة مقالة جديدة
@app.route('/new', methods=['GET', 'POST'])
def new_article():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        conn = sqlite3.connect('articles.db')
        c = conn.cursor()
        c.execute("INSERT INTO articles (title, content) VALUES (?, ?)", (title, content))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('new_article.html')

if __name__ == '__main__':
    app.run(debug=True , port=5000)
