from logging import info

from pymongo import MongoClient
from pymongo.database import Database, Collection

from settings_loader import SettingsFile

DB_NAME: str = 'black_lists'
BL_DOMAINS_COLLECTION_NAME: str = 'domains'
BL_IPS_COLLECTION_NAME: str = 'ips'


class MongoCollection:
    def __init__(self, db_string: str, db_name: str, collection_name: str):
        self.db_string: str = db_string
        self.db_name: str = db_name
        self.collection_name = collection_name
        self.client: MongoClient()
        self.db: Database
        self.collection: Collection

    def __enter__(self):
        info(f"[{self.__class__}]Creating connection to {self.db_name}")
        self.client = MongoClient(self.db_string)
        self.db = self.client[self.db_name]
        self.collection = self.db[self.collection_name]
        return self.collection

    def __exit__(self, exc_type, exc_value, trace):
        info(f"[{self.__class__}]Closing connection to {self.db_name}")
        self.client.close()


def update_field_from_list(token_filename: str, db_name: str, collection_name: str, field_name: str,
                           values: list[str]) -> None:
    db_string = SettingsFile(token_filename).settings

    # getting exising values list from db
    with MongoCollection(db_string=db_string,
                         db_name=db_name,
                         collection_name=collection_name) as collection:
        existing_records = collection.find({field_name: {'$in': values}})
        existing_values = list(map(lambda x: x[field_name], list(existing_records)))

    # getting new values
    cache_values_set = set(values)
    existing_values_set = set(existing_values)
    new_values_set = cache_values_set - existing_values_set
    new_values = list(new_values_set)

    # updating existing values and adding new values
    with MongoCollection(db_string=db_string,
                         db_name=db_name,
                         collection_name=collection_name) as collection:
        if len(existing_values) != 0:
            collection.update_many({field_name: {'$in': existing_values}}, {"$currentDate": {"last_update": True}})
        if len(new_values) != 0:
            collection.insert_many([{field_name: ip} for ip in new_values])
            collection.update_many({field_name: {'$in': new_values}}, {"$currentDate": {"last_update": True}})

    return


def upload_blocked_ips(blocked_ips_list: list[str]) -> None:
    update_field_from_list(token_filename='tokens/mongo.token',
                           db_name=DB_NAME,
                           collection_name=BL_IPS_COLLECTION_NAME,
                           field_name='ip',
                           values=blocked_ips_list)


def upload_blocked_domains(blocked_domains_list: list[str]) -> None:
    update_field_from_list(token_filename='tokens/mongo.token', db_name=DB_NAME,
                           collection_name=BL_DOMAINS_COLLECTION_NAME,
                           field_name='domain',
                           values=blocked_domains_list)
