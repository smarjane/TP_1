import os
import tempfile
import unittest

_tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
_tmp.close()
os.environ["BIBLIO_DB"] = _tmp.name

import biblio  # noqa: E402


class BiblioTest(unittest.TestCase):
    def setUp(self):
        biblio.init_db()

    def test_search_finds_title(self):
        rows = biblio.search_books("Dune")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][1], "Dune")

    def test_borrow_available_book(self):
        self.assertTrue(biblio.borrow_book(3, 1))

    def test_borrow_unknown_book_fails(self):
        self.assertFalse(biblio.borrow_book(42, 1))

    def test_late_contains_dune(self):
        titles = [row[0] for row in biblio.late()]
        self.assertIn("Dune", titles)


if __name__ == "__main__":
    unittest.main()
