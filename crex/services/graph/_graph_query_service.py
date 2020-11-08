from abc import ABC
from rdflib.query import Result
from frex.stores import SparqlQueryable, RequestResultCache


class _GraphQueryService(ABC):
    """
    _GraphQueryService is the base class for all query services based on queryable graphs.
    """

    def __init__(self, *, queryable: SparqlQueryable):
        self.queryable = queryable
        self.cache_graph = None

    def get_cache_graph(self, *, sparql: str):
        """
        Apply a sparql query to query the queryable object, then create a new RequestResultCache based on the
        result.

        :param sparql: a SPARQL query to query the graph
        """
        self.cache_graph = RequestResultCache(
            result=self.queryable.query(sparql=sparql)
        ).get_graph()

    def get_query_result(self, *, sparql: str) -> Result:
        """
        Query a graph and return the result.

        :param sparql: a SPARQL query string to query the graph
        :return: the Result object returned by the query call
        """
        query_result = self.queryable.query(sparql=sparql)

        return query_result
