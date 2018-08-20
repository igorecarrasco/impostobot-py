import fetcher_tjsp
import fetcher_cnj
import sqlite3
import sys

create_table = '''create table if not exists paychecks(
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

    # fetcher = fetcher_tjsp.Fetcher()

    #  Create crude list of instantiated Fetcher objects
    fetchers = [
        fetcher_tjsp.Fetcher(),
        fetcher_cnj.Fetcher()]

    for fetcher in fetchers:
        dynamic_fetcher = getattr(fetcher, 'fetch')
        result = dynamic_fetcher(year, month)
        print "Got %d entries" % len(result)

        values = [(year, month, e.source , e.name, e.position, e.allocation, e.gross_pay, e.net_pay, int(e.active)) for e in result]
        cursor.executemany('insert into paychecks values (?,?,?,?,?,?,?,?,?)', values)
        db.commit()

if __name__ == "__main__":
    sys.exit(main(sys.argv))
