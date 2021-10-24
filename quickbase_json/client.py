import requests
import json




class QuickbaseJSONClient:
    def __init__(self, realm, auth, **kwargs):
        self.realm = realm
        self.auth = auth
        self.headers = {
            'QB-Realm-Hostname': f'{self.realm}.quickbase.com',
            'User-Agent': '{User-Agent}',
            'Authorization': f'QB-USER-TOKEN {auth}'
        }
        self.debug = True if kwargs.get('debug') else False

    """
    Records API
    """

    def query_records(self, table: str, select: list, where: str, **kwargs):
        """
        Queries for record data.
        https://developer.quickbase.com/operation/runQuery
        :param table: quickbase table
        :param select: list, list of fids to query
        :param where: Quickbase query language string. i.e. {3.EX.100}
        :param kwargs: optional request parameters.
        :return: json data of records {data: ..., fields: ...}
        """

        body = {'from': table, 'select': select, 'where': where}

        # add optional args
        body.update(kwargs)

        return requests.post('https://api.quickbase.com/v1/records/query', headers=self.headers, json=body).json()

    def insert_update_records(self, table: str, data: list):
        """
        Inerts or updates records in a given table.
        https://developer.quickbase.com/operation/upsert
        :param table: table to add records to
        :param data: list of dict of data, [{"6": {"value": 'example'}}] (do not include 3, record id to insert)
        :return: record id of created/updated records
        """

        body = {'to': table, 'data': data}
        return requests.post('https://api.quickbase.com/v1/records', headers=self.headers, json=body).json()

    def delete_records(self, table: str, where: str):
        """
        Deletes records in a table based on a query.
        https://developer.quickbase.com/operation/deleteRecords
        :param table: The unique identifier of the table.
        :param where: The filter to delete records. To delete all records specify a filter that will include all records.
        :return: dict, numberDeleted is number of records deleted.
        """

        headers = self.headers
        body = {'to': table, 'where': where}
        return requests.delete('https://api.quickbase.com/v1/records', headers=headers, json=body).json()

    """
    Table API
    """

    def create_table(self, app_id: str, name: str, **kwargs):
        """
        Creates a table in an application.
        https://developer.quickbase.com/operation/createTable
        :param app_id: The unique identifier of an app
        :param name: name of table
        :param kwargs: optional args
        :return:
        """

        headers = self.headers
        params = {'appId': f'{app_id}'}
        body = {'name': name}.update(kwargs)
        return requests.post('https://api.quickbase.com/v1/tables', params=params, headers=headers, json=body).json()

    def get_tables(self, app_id: str):
        """
        Gets all tables in an application
        https://developer.quickbase.com/operation/getAppTables
        :param app_id: The unique identifier of an app.
        :return: dict of all tables in application.
        """

        headers = self.headers
        params = {'appId': f'{app_id}'}
        return requests.post('https://api.quickbase.com/v1/tables', params=params, headers=headers, json=body).json()
