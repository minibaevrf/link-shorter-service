import random
import string


class LinkShorter:
    """Class which generate short links(aliases) by given source link, store it inside redis storage
    and extract source link by short link(alias).

    Attributes:
        redis_storage: Redis storage which is used to store short(as key) and source(as value) links.
    """
    __r_storage = None

    def __init__(self, redis_storage):
        """Inits LinkShorter with passed redis storage."""
        self.__r_storage = redis_storage

    __short_link_len = 8

    def save_link(self, source_link):
        """Saving source link inside redis storage with alias which will be used as short link.

        Args:
            source_link: source link which need to save.

        Returns:
            A key of saved source link which can be used as short link.
        """
        short_link = self.__get_random_str()
        self.__save_link_in_db(short_link, source_link)
        return short_link

    def get_source_link(self, short_link):
        """Extracting of source link from redis storage by given short link.

        Args:
            short_link: alias(key) of source link.

        Returns:
            Stored source link, otherwise if storage doesn't contain given short_link(key) - None.
        """
        if self.__r_storage.exists(short_link):
            return self.__r_storage.get(short_link)
        return None

    def __save_link_in_db(self, short_link, source_link):
        """Utility private method which saves source link(value) into redis storage by short link (key).

        Args:
            short_link: alias(key) of source link.
            source_link: source link which need to save(value).
        """
        self.__r_storage.set(short_link, source_link)

    def __get_random_str(self):
        """Utility private method which generate unique string to be able to use it as alias(key) for short links.

        Returns:
            Unique string which doesn't use in redis storage as key.
        """
        pattern = string.ascii_letters + string.digits
        result = ''.join(random.choice(pattern) for i in range(self.__short_link_len))
        while True:
            if not self.__r_storage.exists(result):
                break
            else:
                result = ''.join(random.choice(pattern) for i in range(self.__short_link_len))

        return result
