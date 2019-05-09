from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, Item

engine = create_engine('sqlite:///catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Items for Soccer
category1 = Category(name="Soccer")

session.add(category1)
session.commit()

menuItem1 = Item(name="Shin Gaurd", description="Soccer is definitely a contact sport. Shin guards help reduce the chance of injury to the shin (tibia), the third-most likely area of the body to be injured playing soccer, according to a recent study.",
                     category=category1)

session.add(menuItem1)
session.commit()

print("added menu items!")