from flask import Flask, redirect, render_template, request, url_for
import sqlite3

app = Flask(__name__)
DATABASE = "notes.db"


def init_db():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    """)
    connection.commit()
    connection.close()


def get_notes():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM notes ORDER BY id DESC")
    notes = cursor.fetchall()
    connection.close()
    return notes


def add_note(title, content):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO notes (title, content) VALUES (?, ?)",
        (title, content),
    )
    connection.commit()
    connection.close()


def delete_note(note_id):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    connection.commit()
    connection.close()


init_db()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/notes", methods=["GET", "POST"])
def notes():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()

        if title and content:
            add_note(title, content)

        return redirect(url_for("notes"))

    return render_template("notes.html", notes=get_notes())


@app.route("/delete/<int:note_id>", methods=["POST"])
def delete(note_id):
    delete_note(note_id)
    return redirect(url_for("notes"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
