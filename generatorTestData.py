# encoding: utf8
# generateTestData.py

import cx_Oracle
from sqlalchemy import ( create_engine,Table,text,MetaData,Column,
     Integer, String, Sequence )
from sqlalchemy.exc import DatabaseError
from faker import Faker

DB_USER = "hr"
DB_PASSWORD = "redhat"
DB_SID = "testing"
LOCALE="zh_CN"  # zh_CN: to chinese faker data
TOTAL=100000  # how many faker user that you want to generated.


def createTables(metadata):
    # create `my_user` table, cache table structure to metadata
    my_user = Table("my_user", metadata, 
                   Column("user_id", Integer, Sequence("user_id_seq"), primary_key=True),
                   Column("username", String(16), nullable=False),
                   Column("address", String(100), nullable=True),
                   Column("phone", String(11), nullable=True),
                   Column("email", String(60),nullable=False),
    )
    return {"my_user": my_user}


def generateFakeUserData(connection, tables):
    fk = Faker(locale=LOCALE)
    # Oracle is different from MySQL, it has no auto_increment attribute for
    # an INTEGER field. you have create a sequence first, and call sequence.nextval
    #
    try:
        connection.execute(text("""
CREATE SEQUENCE user_id_seq INCREMENT BY 1 NOCYCLE 
"""))
    except DatabaseError:
        # When run this program again , Oracle already has the `user_id_seq`
        # sequence, so it throw the ORA-xxxxx error.
        print("[WARNING]: `user_id_seq` sequence has been created.")
    while True:
        username = fk.name()
        address = fk.address()
        phone = fk.phone_number()
        email = fk.email()
        print("=" * 50)
        print("Generate username:%s\n address:%s\n phone:%s\n email:%s\n\n" % ( 
          username,
          address,
          phone,
          email,))
        stmt = tables["my_user"].insert().values(username=username,address=address,phone=phone,email=email)
        connection.execute(stmt) 
        print(stmt)

        yield (username,address,phone,email,)
    

engine = create_engine("oracle+cx_oracle://%s:%s@%s/?encoding=UTF-8&nencoding=UTF-8"
     % (DB_USER,DB_PASSWORD,DB_SID,)
)
metadata = MetaData()
tables = createTables(metadata)
metadata.create_all(engine)


with engine.connect() as connection:
    gn = generateFakeUserData(connection,tables)
    connection = connection.execution_options(
           isolation_level="AUTOCOMMIT"
    )
    for i in range(TOTAL):
        print(next(gn))

print("You has been generate %d users" % TOTAL)



