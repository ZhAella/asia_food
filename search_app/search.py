from django.contrib.postgres.search import (SearchQuery,
                                            SearchVector,
                                            SearchRank)


class SearchEngine:
    @staticmethod
    def search(vector, *queries):
        for query in queries:
            search_query = SearchQuery(query)
            search_vector = SearchVector(vector)
            search_rank = SearchRank(search_vector, search_query)
            return search_rank

