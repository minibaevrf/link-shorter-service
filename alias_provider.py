import hashlib


class AliasProvider:
    """Class generates aliases (short links) for source link by their hash

    Attributes:
        alias_len: length of generated aliases
    """

    __alias_len = None

    def __init__(self, alias_len):
        self.__alias_len = alias_len

    def get_alias_by_md5_hash(self, link):
        """Generate alias of source link by MD5 hash of link of given length

        Args:
            link: link to generate alias.

        Returns:
            An alias of given source link based on md5 hash.
        """
        link_hash_obj = hashlib.md5(bytes(link, encoding='utf-8'))
        return link_hash_obj.hexdigest()[:self.__alias_len]
