from sqlalchemy import Table, Column, Integer, String, Float, MetaData

metadata = MetaData()

expenses = Table(
    "expenses",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(100)),
    Column("amount", Float),
    Column("category", String(50)),
)
