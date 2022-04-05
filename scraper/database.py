from pymongo import MongoClient

from config import settings


class MongoDB:
    def __init__(self, connection_string: str, db_name: str, collection_name: str) -> None:
        self.connection_string = connection_string
        self.cluster = MongoClient(self.connection_string)
        self.db = self.cluster[db_name]
        self.collection = self.db[collection_name]


class PostCollection(MongoDB):
    def get_post(self, post_dict: dict) -> dict:
        return self.collection.find_one(post_dict)


    def create_post(
        self,
        post_owner: str,
        post_owner_location: str,
        post_owner_url: str,
        post_description: str,
        post_image_url: str,
    ) -> None:
        post_to_verify = self.get_post({"description": post_description})


        if not post_to_verify:
            post = {
                "owner": post_owner,
                "owner_location": post_owner_location,
                "owner_url": post_owner_url,
                "description": post_description,
                "image_url": post_image_url,
            }

            self.collection.insert_one(post)


CONNECTION_STRING = f"mongodb+srv://{settings.database_username}:{settings.database_password}@cluster0.slvzn.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
post_collection = PostCollection(
    connection_string=CONNECTION_STRING, db_name="instraper", collection_name="post"
)
