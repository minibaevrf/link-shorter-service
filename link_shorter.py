import random
import string

import redis


class LinkShorter:
    __r_storage = redis.Redis(host='localhost', port=6379)

    __short_link_len = 8

    @staticmethod
    def save_link(source_link):
        short_link = LinkShorter.__get_random_str()
        LinkShorter.__save_link_in_db(short_link, source_link)
        return short_link

    @staticmethod
    def get_source_link(short_link):
        if LinkShorter.__r_storage.exists(short_link):
            return LinkShorter.__r_storage.get(short_link)
        return None

    @staticmethod
    def __save_link_in_db(short_link, source_link):
        LinkShorter.__r_storage.set(short_link, source_link)

    """
    Get a random string to use as short address for link
    """
    @staticmethod
    def __get_random_str():
        pattern = string.ascii_letters + string.digits
        result = ''.join(random.choice(pattern) for i in range(LinkShorter.__short_link_len))
        while True:
            if not LinkShorter.__r_storage.exists(result):
                break
            else:
                result = ''.join(random.choice(pattern) for i in range(LinkShorter.__short_link_len))

        return result
