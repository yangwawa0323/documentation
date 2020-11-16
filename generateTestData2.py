# encoding: utf8
# Author: yangwawa0323@163.com
# Website: www.51cloudclass.com
# generateTestData.py
# Generate many fake data to Oracle, for ADDM and AWR monitoring purpose

# Installation:
# $ python -m venv venv
# $ ./venv/bin/activate
# $ pip install cx_oracle sqlalchemy faker
#
# Running:
# $ python ./generateTestData.py

#import cx_Oracle
from sqlalchemy import ( create_engine,Table,text,MetaData,Column, 
     Integer, String, DateTime, Sequence, ForeignKey )
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from random import randint


from faker import Faker


DB_USER = "hr"
DB_PASSWORD = "redhat"
DB_SID = "testing"
LOCALE="zh_CN"  # zh_CN: to chinese faker data
TOTAL=120  # how many faker user that you want to generated.

Base = declarative_base()

br_table = Table("bought_record", Base.metadata, 
            Column('cust_id', Integer, ForeignKey('customer.id')),
            Column('prod_id', Integer, ForeignKey('product.id')), 
            Column('bought_date', DateTime ),
            Column('quantity', Integer ),
	)

class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    product_name = Column("product_name", String(100), nullable=False)
    customers = relationship("Customer",
                    secondary=br_table,
		    backref="bought_products")

class Customer(Base):
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True)
    username = Column("username", String(16), nullable=False)
    address = Column("address", String(100), nullable=True)
    phone = Column("phone", String(11), nullable=True)
    email = Column("email", String(60),nullable=False)


fk = Faker(locale=LOCALE)

def generateCustomer():
    while True:
        c = Customer()
        c.username = fk.name()
        c.address = fk.address()
        c.phone = fk.phone_number()
        c.email = fk.email()
        yield c

engine = create_engine("mysql+pymysql://root:redhat@localhost/demo?charset=utf8mb4")
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)


def generateCustomers(session):
    gc = generateCustomer()
    for i in range(TOTAL):
        cust = next(gc)
        session.add(cust)
    session.commit()


def generateProducts(session):
    for i in range(30):
        prod = Product()
        prod.product_name = fk.uuid4()
        session.add(prod)
    session.commit()

def generateBoughtRecord(session):
    for i in range(3*TOTAL):
        with engine.connect() as connection:
            stmt = br_table.insert().values(
                    cust_id = randint(1,TOTAL), 
                    prod_id = randint(1,30) , 
		    bought_date = fk.date_time_between(
                                         start_date="-30m",
                                         end_date="now"),
                    quantity = fk.random_int()
                    )
            connection.execute(stmt)      

generateCustomers(session)
generateProducts(session)
generateBoughtRecord(session)
session.close()

