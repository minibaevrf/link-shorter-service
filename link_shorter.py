import hashlib


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

    __alias_len = 8

    def save_link(self, source_link):
        """Saving source link inside redis storage with alias which will be used as short link.

        Args:
            source_link: source link which need to save.

        Returns:
            A key of saved source link which can be used as short link.
        """
        link_hash = self.__get_alias_by_md5_hash(source_link)

        # checking that storage already contains links with the same hash
        h_len = self.__r_storage.hlen(link_hash)

        if h_len == 0:
            self.__r_storage.hset(link_hash, format(0, 'x'), source_link)
            return link_hash
        else:
            # set order of stored link in hex format which can be used in alias after hash
            order = format(h_len, 'x')

            self.__r_storage.hset(link_hash, order, source_link)
            return link_hash + order

    def get_source_link(self, short_link):
        """Extracting of source link from redis storage by given short link.

        Args:
            short_link: alias(key) of source link.

        Returns:
            Stored source link, otherwise if storage doesn't contain given short_link(key) - None.
        """
        order = 0
        link_hash = short_link

        if len(short_link) != self.__alias_len:
            order = short_link[self.__alias_len:]
            link_hash = short_link[:self.__alias_len]

        stored_links = self.__r_storage.hget(link_hash, order)

        return None if stored_links is None else stored_links.decode('utf-8')

    def __get_alias_by_md5_hash(self, link):
        """Generate alias of source link by MD5 hash of link of given length

        Args:
            link: link to generate alias.

        Returns:
            An alias of given source link based on md5 hash.
        """
        link_hash_obj = hashlib.md5(bytes(link, encoding='utf-8'))
        return link_hash_obj.hexdigest()[:self.__alias_len]
