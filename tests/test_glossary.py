import io, json, os, sys, unittest, contextlib
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import gtm_glossary
from gtm_glossary.__main__ import main


class T(unittest.TestCase):
    def test_count(self):
        self.assertEqual(len(gtm_glossary.load()), 110)

    def test_every_entry_links_to_glossary_page(self):
        for t in gtm_glossary.load():
            self.assertTrue(t["url"].startswith("https://www.onegtmlab.dev/glossary/"), t)
            self.assertTrue(t["definition"])

    def test_lookup_by_name_and_id(self):
        self.assertEqual(gtm_glossary.lookup("DMARC")["id"], "dmarc")
        self.assertEqual(gtm_glossary.lookup("lead scoring")["id"], "lead-scoring")
        self.assertIsNone(gtm_glossary.lookup("not a term"))

    def test_search_ranks_term_matches_first(self):
        r = gtm_glossary.search("email")
        self.assertTrue(r and "email" in r[0]["term"].lower())

    def test_cli_define(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(main(["define", "spf", "record"]), 0)
        self.assertIn("https://www.onegtmlab.dev/glossary/spf-record", out.getvalue())

    def test_cli_export_csv_and_md(self):
        for fmt, needle in (("csv", "id,term,definition,url"), ("md", "# GTM glossary")):
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                main(["export", "--format", fmt])
            self.assertIn(needle, out.getvalue())

    def test_csv_matches_json(self):
        import csv
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        rows = list(csv.DictReader(open(os.path.join(root, "glossary.csv"), encoding="utf-8")))
        self.assertEqual([r["id"] for r in rows], [t["id"] for t in gtm_glossary.load()])


if __name__ == "__main__":
    unittest.main()
