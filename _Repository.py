import atexit
import sqlite3
from DAO import _Clinics, _Logistics, _Suppliers, _Vaccines
from DTO import Vaccine, Supplier, Logistic, Clinic

class _Repository:
    def __init__(self):
        self._conn = sqlite3.connect('database.db')
        self.vaccine = _Vaccines(self._conn)
        self.supplier = _Suppliers(self._conn)
        self.clinic = _Clinics(self._conn)
        self.logistics = _Logistics(self._conn)

    def create_tables(self):
        self._conn.executescript("""
        CREATE TABLE vaccines (
            id         INT         PRIMARY KEY,
            date       DATE        NOT NULL,
            supplier   INT,         
            quantity   INT         NOT NULL,
            
            FOREIGN KEY(supplier)   REFERENCES suppliers(id)
        );
 
        CREATE TABLE suppliers (
            id         INT         PRIMARY KEY,
            name       STRING      NOT NULL,
            logistic   INT,         
            
            FOREIGN KEY(logistic)   REFERENCES logistics(id)
        );
        
        CREATE TABLE clinics (
            id         INT         PRIMARY KEY,
            location   STRING      NOT NULL,
            demand     INT         NOT NULL,
            logistic   INT,         
            
            FOREIGN KEY(logistic)   REFERENCES logistics(id)
        );
 
        CREATE TABLE logistics (
            id              INT         PRIMARY KEY,
            name            STRING      NOT NULL,
            count_sent      INT         NOT NULL,
            count_received  INT         NOT NULL
     
        );
    """)

    def insert(self, vaccine, supplier, clinic, logistics):
        self.insert_vaccine(vaccine)
        self.insert_supplier(supplier)
        self.insert_clinic(clinic)
        self.insert_logistic(logistics)

    def summary(self):
        return str(self.vaccine.total_inventory())+', '+str(self.clinic.total_demand())+', '+str(self.logistics.total_received())+', '+str(self.logistics.total_sent())+'\n'

    def receive_shipment(self, name, amount, date):
        supplier = self.supplier.find(name)
        self.vaccine.insert(Vaccine(self.vaccine.fetch_next_id(), date, supplier.id, amount))
        logistic = self.logistics.find(supplier.logistic)
        self.logistics.add_received(logistic.id, amount)

    def send_shipment(self, location, amount):
        self.clinic.decrease_demand(location, amount)
        clinic = self.clinic.find(location)
        self.logistics.add_sent(clinic.logistic, amount)
        while amount != 0:
            amount = self.vaccine.fetch_decrease(amount)

    def insert_vaccine(self, data):
        for d in data:
            arr = d.split(',')
            self.vaccine.insert(Vaccine(int(arr[0]), arr[1], int(arr[2]), int(arr[3])))

    def insert_supplier(self, data):
        for d in data:
            arr = d.split(',')
            self.supplier.insert(Supplier(int(arr[0]), arr[1], int(arr[2])))

    def insert_clinic(self, data):
        for d in data:
            arr = d.split(',')
            self.clinic.insert(Clinic(int(arr[0]), arr[1], int(arr[2]), int(arr[3])))

    def insert_logistic(self, data):
        for d in data:
            arr = d.split(',')
            self.logistics.insert(Logistic(int(arr[0]),arr[1],int(arr[2]), int(arr[3])))

    def _close(self):
        self._conn.commit()
        self._conn.close()

# the repository singleton
repo = _Repository()
atexit.register(repo._close)


