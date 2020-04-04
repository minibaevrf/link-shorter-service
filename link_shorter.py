import random
import string


class LinkShorter:
    __r_storage = None

    def __init__(self, redis_storage):
        self.__r_storage = redis_storage

    __short_link_len = 8

    def save_link(self, source_link):
        short_link = self.__get_random_str()
        self.__save_link_in_db(short_link, source_link)
        return short_link

    def get_source_link(self, short_link):
        if self.__r_storage.exists(short_link):
            return self.__r_storage.get(short_link)
        return None

    def __save_link_in_db(self, short_link, source_link):
        self.__r_storage.set(short_link, source_link)

    """
    Get a random string to use as short address for link
    """
    def __get_random_str(self):
        pattern = string.ascii_letters + string.digits
        result = ''.join(random.choice(pattern) for i in range(self.__short_link_len))
        while True:
            if not self.__r_storage.exists(result):
                break
            else:
                result = ''.join(random.choice(pattern) for i in range(self.__short_link_len))

        return result
