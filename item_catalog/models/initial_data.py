from item_catalog.db import DBSession
from item_catalog.models import User, Category, Item

users = [
		('Junior', 'juniorbaez01@gmail.com', 'holamundo'),
		('Roberto', 'Robertobaez01@gmail.com', 'holamundo2')
	]

categories = [
		('frontend',),
		('backend',)
	]

items = [
		(1, 1, "1111111111sdf", "11111 gwoeijg;lksdnbgdoifgjsddf"),
		(1, 1, "1111111111grght", "11111 gwoeijg;lksdnbgdsdgoifgjsddf"),
		(1, 1, "1111111111", "11111 gwoeijg;lksdnbgdoifsdggjsddf"),
		(2, 2, "asdfsdasdfsdgsd", "gwoeijg;lkssdnbgdoifgjsddf"),
		(2, 2, "2222sdfs22dgsd", "2222222gwoeisdfgsdjg;lksdnbgdoifgjsddf"),
		(2, 2, "2222sdg22dgsd", "2222222sdfgssgwoeijg;lksdnbgdoifgjsddf"),
	]

for user in users:
	DBSession.add( User(name=user[0], email=user[1], password=user[2]) )

for cat in categories:
	DBSession.add( Category(name=cat[0]) )

for i in items:
	DBSession.add( Item(user_id=i[0], category_id=i[1], name=i[2], desc=i[3]) )

DBSession.commit()
