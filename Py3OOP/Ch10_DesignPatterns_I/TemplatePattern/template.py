'''
The template pattern is used when several different task have some steps in common
The common steps are implemented in a base class and the distinct steps are
overriden in sublasses, to provide custom behavior.
'''
import sqlite3
import datetime


class QueryTemplate:

    def connect(self):
        self.conn = sqlite3.connect("sales.db")

    def construct_query(self):
        raise NotImplementedError()

    def do_query(self):
        results = self.conn.execute(self.query)
        self.results = results.fetchall()

    def format_results(self):
        output = []
        for row in self.results:
            row = [str(i) for i in row]
            output.append(", ".join(row))
        self.formatted_results = "\n".join(output)

    def output_results(self):
        raise NotImplementedError()

    def process_format(self):
        '''This method is to be called by an outside client. It calls the steps
        in the correct order, but doesn't care about the implementation.
        Each step could be overriden by a subclass'''
        self.connect()
        self.construct_query()
        self.do_query()
        self.format_results()
        self.output_results()


class NewVehiclesQuery(QueryTemplate):

    def construct_query(self):
        self.query = "select * from Sales where new='true'"

    def output_results(self):
        print(self.formatted_results)


class UserGrossQuery(QueryTemplate):

    def construct_query(self):
        self.query = ("select salesperson, sum(amt) " +
            " from Sales group by salesperson")

    def output_results(self):
        filename = "gross_sales_{0}".format(
            datetime.date.today().strftime("%Y%m%d"))
        with open(filename, 'w') as outfile:
            outfile.write(self.formatted_results)


if __name__ == "__main__":

    conn = sqlite3.connect("sales.db")
    conn.execute("CREATE TABLE Sales (salesperson text, "
        "amt currency, year integer, model text, new boolean)")
    conn.execute("INSERT INTO Sales values"
    " ('Tim', 16000, 2010, 'Honda Fit', 'true')")
    conn.execute("INSERT INTO Sales values"
    " ('Tim', 9000, 2006, 'Ford Focus', 'false')")
    conn.execute("INSERT INTO Sales values"
    " ('Gayle', 8000, 2004, 'Dodge Neon', 'false')")
    conn.execute("INSERT INTO Sales values"
    " ('Gayle', 28000, 2009, 'Ford Mustang', 'true')")
    conn.execute("INSERT INTO Sales values"
    " ('Gayle', 50000, 2010, 'Lincoln Navigator', 'true')")
    conn.execute("INSERT INTO Sales values"
    " ('Don', 20000, 2008, 'Toyota Prius', 'false')")
    conn.commit()
    conn.close()
