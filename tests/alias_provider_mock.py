from alias_provider import AliasProvider


class AliasProviderMock:

    __original_alias_provider = None

    __overrode_get_alias_by_md5_hash = None

    __alias_len = 8

    def __init__(self):
        self.__original_alias_provider = AliasProvider(self.__alias_len)

    def get_alias_by_md5_hash(self, link):
        if self.__overrode_get_alias_by_md5_hash is not None:
            return self.__overrode_get_alias_by_md5_hash(link)

        return self.__original_alias_provider.get_alias_by_md5_hash(link)

    def override_get_alias_by_md5_hash(self, new_method):
        self.__overrode_get_alias_by_md5_hash = new_method
