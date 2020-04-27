class RedisMock:
    """Mock of Redis storage to use in unit tests without Redis instance"""
    __storage = None

    def __init__(self):
        self.__storage = {}

    def hget(self, link_hash, order):
        """Get saved source link by hash and order of it

        Args:
            link_hash: hash of link.
            order: order of stored link in cases of collisions.

        Returns:
            An alias of given source link generated from alias_generator_method
        """
        if link_hash not in self.__storage or str(order) not in self.__storage[link_hash]:
            return None

        return self.__storage[link_hash][str(order)]

    def hlen(self, link_hash):
        """Get count of stored links with the same hash.

        Args:
            link_hash: hash of link.

        Returns:
            Count of stored links with the same hash
        """
        return 0 if link_hash not in self.__storage else len(self.__storage[link_hash])

    def hset(self, link_hash, order, source_link):
        """Set source link by hash and order

        Args:
            link_hash: hash of link.
            order: order of stored link in cases of collisions.
            source_link:link needed to save.
        """
        if link_hash not in self.__storage:
            self.__storage[link_hash] = {}

        # encode value because Redis stores it like that
        self.__storage[link_hash][order] = source_link.encode('utf-8')

    def set(self, key, value):
        self.__storage[key] = value.encode('utf-8')

    def get(self, key):
        if key in self.__storage:
            return self.__storage[key]
        return None
