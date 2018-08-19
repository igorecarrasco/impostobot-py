import fetcher_tjsp
import sqlite3
import sys

create_table = '''create table if not exists leeches(
                    year integer,
                    month integer,
                    source text,
                    name text,
                    position text,
                    allocation text,
                    gross_pay real,
                    net_pay real,
                    active integer,
                    unique(year, month, source, name, active))'''

def main(argv):
    try:
        year, month = int(argv[1]), int(argv[2])
    except:
        print "Usage: python fetcher.py <year> <month>"
        return 1

    db = sqlite3.connect('impostobot.db')
    cursor = db.cursor()

    cursor.execute(create_table)

    fetcher = fetcher_tjsp.Fetcher()

    result = fetcher.fetch(year, month)
    print "Got %d entries" % len(result)

    values = [(year, month, 'TJSP', e.name, e.position, e.allocation, e.gross_pay, e.net_pay, int(e.active)) for e in result]
    cursor.executemany('insert into leeches values (?,?,?,?,?,?,?,?,?)', values)
    db.commit()

if __name__ == "__main__":
    sys.exit(main(sys.argv))
