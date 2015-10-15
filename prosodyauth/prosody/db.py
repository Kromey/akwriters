from django.db import connection


class ProsodyDatastore:
    @staticmethod
    def get_data_store(username, domain, store):
        data = {}
        with connection.cursor() as cursor:
            cursor.execute(
                    'SELECT key, value FROM prosody.prosody WHERE UPPER("user")=UPPER(%s) AND UPPER(host)=UPPER(%s) AND store=%s',
                    [username, domain, store]
                    )

            data = dict(cursor.fetchall())

        return data

    @staticmethod
    def get_value(username, domain, store, key):
        try:
            data = ProsodyDatastore.get_data_store(username, domain, store)[key]
        except KeyError:
            data = None

        return data

    @staticmethod
    def set_value(username, domain, store, key, value):
        with connection.cursor() as cursor:
            cursor.execute(
                    'UPDATE prosody.prosody SET value=%s WHERE UPPER("user")=UPPER(%s) AND UPPER(host)=UPPER(%s) AND store=%s AND key=%s',
                    [value, username, domain, store, key]
                    )

    @staticmethod
    def insert_value(username, domain, store, key, value):
        with connection.cursor() as cursor:
            cursor.execute(
                    'INSERT INTO prosody.prosody SET value=%s, UPPER("user")=UPPER(%s), UPPER(host)=UPPER(%s), store=%s, key=%s',
                    [value, username, domain, store, key]
                    )

