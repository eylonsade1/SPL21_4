from DTO import Clinic, Logistic, Supplier, Vaccine


class _Vaccines:
    def __init__(self, conn):
        self.conn = conn

    def insert(self, vaccine):
        self.conn.execute("""
               INSERT INTO vaccines (id, date, supplier, quantity) VALUES (?, ?, ?, ?)
           """, [vaccine.id, vaccine.date, vaccine.supplier, vaccine.quantity])

    def fetch_decrease(self, amount):
        c = self.conn.cursor()
        c.execute("""
                SELECT id, date, supplier, quantity  FROM vaccines WHERE id=(SELECT MIN(id) FROM vaccines)
            """)
        vac = c.fetchone()
        if amount == int(vac[3]):
            self.delete(vac.id)
            return 0
        elif amount < int(vac[3]):
            self.update_quantity((int(vac[3])-amount), vac[0])
            return 0
        else:
            self.delete(int(vac[0]))
            return amount - int(vac[3])

    def fetch_next_id(self):
        c = self.conn.cursor()
        c.execute("""
                SELECT COUNT(*) FROM vaccines
            """)
        last = c.fetchone()
        if last == 0:
            return 1
        else:
            c.execute("""
                SELECT id, date, supplier, quantity  FROM vaccines WHERE id=(SELECT MAX(id) FROM vaccines)
            """)
            v = c.fetchone()
            return v[0]+1

    def update_quantity(self, amount, id):
        self.conn.execute("""
                UPDATE vaccines SET quantity=(?) WHERE id=(?)
            """, [amount, id])

    def delete(self, id):
        self.conn.execute("""
                DELETE FROM vaccines WHERE id=(?)
            """, [id])

    def total_inventory(self):
        c = self.conn.cursor()
        c.execute("""
                SELECT SUM(quantity) FROM vaccines
            """)
        return c.fetchone()[0]


class _Suppliers:
    def __init__(self, conn):
        self.conn = conn

    def insert(self, supplier):
        self.conn.execute("""
               INSERT INTO suppliers (id, name, logistic) VALUES (?, ?, ?)
           """, [supplier.id, supplier.name, supplier.logistic])

    def find(self, name):
        c = self.conn.cursor()
        c.execute("""
                SELECT id,name,logistic FROM suppliers WHERE name = ?
            """, [name])
        return Supplier(*c.fetchone())


class _Clinics:
    def __init__(self, conn):
        self.conn = conn

    def insert(self, clinic):
        self.conn.execute("""
                INSERT INTO clinics (id, location, demand, logistic) VALUES (?, ?, ?, ?)
            """, [clinic.id, clinic.location, clinic.demand, clinic.logistic])

    def find(self, location):
        c = self.conn.cursor()
        c.execute("""
                SELECT id, location, demand, logistic FROM clinics WHERE location = ?
            """, [location])

        r = c.fetchone()
        return Clinic(r[0], r[1], r[2], r[3])

    def decrease_demand(self, location, amount):
         self.conn.execute("""
                UPDATE clinics SET demand=demand-(?) WHERE location=(?)
                 """, [amount, location])

    def total_demand(self):
        c = self.conn.cursor()
        c.execute("""
                SELECT SUM(demand) FROM clinics
            """)
        return c.fetchone()[0]


class _Logistics:
    def __init__(self, conn):
        self.conn = conn

    def insert(self, logistic):
        self.conn.execute("""
                INSERT INTO logistics (id, name, count_sent, count_received) VALUES (?, ?, ?, ?)
            """, [logistic.id, logistic.name, logistic.count_sent, logistic.count_received])

    def find(self, id):
        c = self.conn.cursor()
        c.execute("""
                SELECT id, name, count_sent, count_received FROM logistics WHERE id=(?)
            """, [id])
        return Logistic(*c.fetchone())

    def add_received(self, logisticID, value):
        self.conn.execute("""
                UPDATE logistics SET count_received=count_received+(?) WHERE id=(?)
                 """, [value, logisticID])

    def add_sent(self, logisticID, value):
        self.conn.execute("""
                UPDATE logistics SET count_sent=count_sent+(?) WHERE id=(?)
                 """, [value, logisticID])

    def total_received(self):
        c = self.conn.cursor()
        c.execute("""
                SELECT SUM(count_received) FROM logistics
                """)
        return c.fetchone()[0]

    def total_sent(self):
        c = self.conn.cursor()
        c.execute("""
                SELECT SUM(count_sent) FROM logistics
                """)
        return c.fetchone()[0]
