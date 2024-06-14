from elasticsearch import Elasticsearch

class Indexer:
    def __init__(self):
        self.es = Elasticsearch()

    def create_index(self, index_name):
        """
        Creates an Elasticsearch index with the specified name.
        """
        self.es.indices.create(index=index_name, ignore=400)

    def index_document(self, index_name, doc_id, doc_content):
        """
        Indexes a document into the specified Elasticsearch index.
        
        Parameters:
        - index_name: Name of the Elasticsearch index.
        - doc_id: ID of the document to be indexed.
        - doc_content: Content of the document to be indexed.
        """
        self.es.index(index=index_name, id=doc_id, body={"content": doc_content})

    def search(self, index_name, query):
        """
        Performs a search query on the specified Elasticsearch index.

        Parameters:
        - index_name: Name of the Elasticsearch index to search within.
        - query: Query string to search for within the 'content' field.

        Returns:
        - Hits matching the query.
        """
        res = self.es.search(index=index_name, body={"query": {"match": {"content": query}}})
        return res['hits']['hits']
