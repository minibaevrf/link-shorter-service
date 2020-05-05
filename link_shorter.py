from alias_provider import AliasProvider


class LinkShorter:
    """Class which generate short links(aliases) by given source link, store it inside redis storage
    and extract source link by short link(alias).

    Attributes:
        redis_storage: Redis storage which is used to store short(as key) and source(as value) links.
    """
    __r_storage = None

    __alias_provider = None

    __alias_len = 8

    def __init__(self, redis_storage, alias_provider=None):
        """Inits LinkShorter with passed redis storage."""
        self.__r_storage = redis_storage

        self.__alias_provider = AliasProvider(self.__alias_len) if alias_provider is None else alias_provider

    def save_link(self, source_link):
        """Saving source link inside redis storage with alias which will be used as short link.

        Args:
            source_link: source link which need to save.

        Returns:
            A key of saved source link which can be used as short link.
        """

        # make lower() for source link to ignore case and avoid saving one link multiple times
        lower_source_link = source_link.lower()

        short_link = self.__get_already_saved_alias(lower_source_link)

        if short_link is not None:
            return short_link.decode('utf-8')

        link_hash = self.__alias_provider.get_alias_by_md5_hash(lower_source_link)

        # checking that storage already contains links with the same hash
        h_len = self.__r_storage.hlen(link_hash)

        order = None

        if h_len == 0:
            order = format(0, 'x')
            short_link = link_hash
        else:
            # set order of stored link in hex format which can be used in alias after hash
            order = format(h_len, 'x')
            short_link = link_hash + order

        self.__r_storage.hset(link_hash, order, lower_source_link)
        self.__save_short_for_reuse(short_link, lower_source_link)

        return short_link

    def get_source_link(self, short_link):
        """Extracting of source link from redis storage by given short link.

        Args:
            short_link: alias(key) of source link.

        Returns:
            Stored source link, otherwise if storage doesn't contain given short_link(key) - None.
        """
        # make lower() for short link to ignore case
        lower_short_link = short_link.lower()

        order = 0
        link_hash = lower_short_link

        if len(lower_short_link) != self.__alias_len:
            order = lower_short_link[self.__alias_len:]
            link_hash = lower_short_link[:self.__alias_len]

        stored_links = self.__r_storage.hget(link_hash, order)

        return None if stored_links is None else stored_links.decode('utf-8')

    def __get_already_saved_alias(self, source_link):
        """Checking that passed source link already exists and contains alias (short link) for it

        Attributes:
            source_link: source link which need to check.

        Returns:
            Stored alias, otherwise if storage doesn't contain given short_link(key) - None.
        """
        return self.__r_storage.get(source_link)

    def __save_short_for_reuse(self, short_link, source_link):
        """Save alias for source link to reuse them for better performance"""
        self.__r_storage.set(source_link, short_link)
