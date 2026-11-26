import argparse, csv, json, sys
from . import load, lookup, search, to_markdown


def main(argv=None):
    p = argparse.ArgumentParser(prog="gtm-glossary", description="Look up GTM terms from the OneGTMLab glossary (offline).")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("define", help="show one term"); s.add_argument("term", nargs="+")
    s = sub.add_parser("search", help="find terms by word"); s.add_argument("query", nargs="+")
    s = sub.add_parser("list", help="list all term names")
    s = sub.add_parser("export", help="print the whole glossary"); s.add_argument("--format", choices=["json", "csv", "md"], default="json")
    a = p.parse_args(argv)
    if a.cmd == "define":
        t = lookup(" ".join(a.term))
        if not t:
            print("No term %r. Try: gtm-glossary search %s" % (" ".join(a.term), a.term[0]), file=sys.stderr); return 1
        print("%s\n%s\n%s" % (t["term"], t["definition"], t["url"]))
    elif a.cmd == "search":
        hits = search(" ".join(a.query))
        for t in hits: print("%-40s %s" % (t["term"], t["url"]))
        if not hits: return 1
    elif a.cmd == "list":
        for t in load(): print(t["term"])
    elif a.cmd == "export":
        d = load()
        if a.format == "json": json.dump(d, sys.stdout, indent=1, ensure_ascii=False); print()
        elif a.format == "md": sys.stdout.write(to_markdown(d))
        else:
            w = csv.DictWriter(sys.stdout, fieldnames=["id", "term", "definition", "url"]); w.writeheader(); w.writerows(d)
    return 0


if __name__ == "__main__":
    sys.exit(main())
