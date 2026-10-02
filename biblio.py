"""Biblio : gestion des prets de livres d'une petite bibliotheque associative.

Usage :
    python biblio.py init
    python biblio.py livres
    python biblio.py chercher <texte>
    python biblio.py emprunter <id_livre> <id_membre>
    python biblio.py rendre <id_livre>
    python biblio.py retards
"""

import os
import sqlite3
import sys
from datetime import date, datetime

DB_PATH = os.environ.get("BIBLIO_DB", "biblio.db")
LOAN_DAYS = 14


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.executescript(
        """
        DROP TABLE IF EXISTS loans;
        DROP TABLE IF EXISTS books;
        DROP TABLE IF EXISTS members;

        CREATE TABLE books (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT NOT NULL
        );

        CREATE TABLE members (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        );

        CREATE TABLE loans (
            id INTEGER PRIMARY KEY,
            book_id INTEGER NOT NULL REFERENCES books(id),
            member_id INTEGER NOT NULL REFERENCES members(id),
            loan_date TEXT NOT NULL,
            return_date TEXT
        );
        """
    )
    books = [
        (1, "L'Etranger", "Albert Camus"),
        (2, "Dune", "Frank Herbert"),
        (3, "Le Petit Prince", "Antoine de Saint-Exupery"),
        (4, "Fondation", "Isaac Asimov"),
        (5, "Les Miserables", "Victor Hugo"),
        (6, "Neuromancien", "William Gibson"),
    ]
    members = [(1, "Alice Martin"), (2, "Bilal Haddad"), (3, "Chloe Nguyen")]
    loans = [
        (1, 2, 1, "2026-01-10", None),
        (2, 4, 2, "2026-01-05", "2026-01-12"),
    ]
    cur.executemany("INSERT INTO books VALUES (?, ?, ?)", books)
    cur.executemany("INSERT INTO members VALUES (?, ?)", members)
    cur.executemany("INSERT INTO loans VALUES (?, ?, ?, ?, ?)", loans)
    conn.commit()
    conn.close()
    print("Base initialisee : %d livres, %d membres." % (len(books), len(members)))


def list_books():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, title, author FROM books ORDER BY id")
    books = cur.fetchall()
    for book in books:
        cur.execute(
            "SELECT member_id FROM loans WHERE book_id = ? AND return_date IS NULL",
            (book[0],),
        )
        loan = cur.fetchone()
        status = "disponible" if loan is None else "emprunte"
        print("[%d] %s (%s) : %s" % (book[0], book[1], book[2], status))
    conn.close()


def search_books(text):
    conn = get_connection()
    cur = conn.cursor()
    query = "SELECT id, title, author FROM books WHERE title LIKE '%" + text + "%'"
    cur.execute(query)
    rows = cur.fetchall()
    conn.close()
    if not rows:
        print("Aucun livre trouve.")
    for row in rows:
        print("[%d] %s (%s)" % row)
    return rows


def borrow_book(book_id, member_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM books WHERE id = ?", (book_id,))
    if cur.fetchone() is None:
        conn.close()
        print("Erreur : livre %d introuvable." % book_id)
        return False
    cur.execute(
        "INSERT INTO loans (book_id, member_id, loan_date) VALUES (?, ?, ?)",
        (book_id, member_id, date.today().isoformat()),
    )
    conn.commit()
    conn.close()
    print("Emprunt enregistre : livre %d, membre %d." % (book_id, member_id))
    return True


def return_book(book_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE loans SET return_date = ? WHERE book_id = ? AND return_date IS NULL",
        (date.today().isoformat(), book_id),
    )
    conn.commit()
    conn.close()
    print("Retour enregistre pour le livre %d." % book_id)


def late():
    c = get_connection()
    x = c.cursor()
    x.execute("SELECT * FROM loans")
    r = []
    for l in x.fetchall():
        d = datetime.strptime(l[3], "%Y-%m-%d").date()
        n = (date.today() - d).days
        if n > LOAN_DAYS:
            x2 = c.cursor()
            x2.execute("SELECT title FROM books WHERE id = ?", (l[1],))
            t = x2.fetchone()[0]
            x2.execute("SELECT name FROM members WHERE id = ?", (l[2],))
            m = x2.fetchone()
            if m is None:
                m = "?"
            else:
                m = m[0]
            r.append((t, m, n - LOAN_DAYS))
    c.close()
    if len(r) == 0:
        print("Aucun retard.")
    else:
        for i in r:
            print("%s, emprunte par %s : %d jours de retard" % (i[0], i[1], i[2]))
    return r


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 1
    command = argv[1]
    if command == "init":
        init_db()
    elif command == "livres":
        list_books()
    elif command == "chercher" and len(argv) == 3:
        search_books(argv[2])
    elif command == "emprunter" and len(argv) == 4:
        borrow_book(int(argv[2]), int(argv[3]))
    elif command == "rendre" and len(argv) == 3:
        return_book(int(argv[2]))
    elif command == "retards":
        late()
    else:
        print(__doc__)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
