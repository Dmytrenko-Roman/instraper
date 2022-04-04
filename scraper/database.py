from typing import NoReturn
from h11 import Data

import pymongo
from pymongo import MongoClient

from config import settings


class MongoDB:
	def __init__(self, connection_string: str, db_name: str, collection_name: str) -> NoReturn:
		self.connection_string = connection_string
		self.cluster = MongoClient(self.connection_string)
		self.db = self.cluster[db_name]
		self.collection = self.db[collection_name]


class PostCollection(MongoDB):
	def create_post(self, post_owner: str, post_description: str):
		post = {
			'owner': post_owner,
			'description': post_description,
		}

		self.collection.insert_one(post)


	


connection_string = f'mongodb+srv://{settings.database_username}:{settings.database_password}@cluster0.slvzn.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'

post_collection = PostCollection(connection_string=connection_string, db_name='instraper', collection_name='post')
