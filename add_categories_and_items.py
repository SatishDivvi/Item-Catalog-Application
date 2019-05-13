from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, Item, Users

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
User1 = Users(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

category1 = Category(user_id=1, name="Soccer")


session.add(category1)
session.commit()

menuItem1 = Item(name="Shin Gaurd", description="Soccer is definitely a contact sport. Shin guards help reduce the chance of injury to the shin (tibia), the third-most likely area of the body to be injured playing soccer, according to a recent study.",
                     category=category1, user_id=1)

session.add(menuItem1)
session.commit()

category2 = Category(user_id=1, name="Football")


session.add(category1)
session.commit()

menuItem1 = Item(name="Helmet", description="As you would probably suspect, the helmet is the most important piece of equipment in football.  Face masks are mandatory, a visor is optional. Jaw pads can also be worn attached to the bottom of the helmet and provide some protection against  concussions.",
                     category=category2, user_id=1)

session.add(menuItem1)
session.commit()

menuItem2 = Item(name="Neck collars", description="Neck collars are often worn by linebackers and defensive lineman for whiplash protection.",
                     category=category2, user_id=1)

session.add(menuItem2)
session.commit()

menuItem3 = Item(name="Jockstrap and Cup", description="Athletic supporters and protective cups are mandatory.",
                     category=category2, user_id=1)

session.add(menuItem3)
session.commit()

menuItem4 = Item(name="Mouth Guard", description="Mouth guards not only protect the wearer's teeth and jaw, but may provide some protection against head injuries such as concussions. The mouth piece must be worn at all times during play. The mouthpiece must be a highly visible color and is mandatory.",
                     category=category2, user_id=1)

session.add(menuItem4)
session.commit()

menuItem5 = Item(name="Gloves", description="Receiver gloves aid in catching the football, particularly during cold weather. Lineman gloves have more padding and help protect of all parts of the hand.",
                     category=category2, user_id=1)

session.add(menuItem5)
session.commit()

print("added menu items!")
