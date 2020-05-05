import unittest

from link_shorter import LinkShorter
from tests.alias_provider_mock import AliasProviderMock
from tests.redis_mock import RedisMock


class LinkShorterTests(unittest.TestCase):

    def test_getting_saved_link(self):

        link_shorter = LinkShorter(RedisMock())

        test_link = "http://sample"

        short_link = link_shorter.save_link(test_link)
        saved_link = link_shorter.get_source_link(short_link)

        self.assertEqual(saved_link, test_link)

    def test_getting_unsaved_link(self):

        link_shorter = LinkShorter(RedisMock())

        not_existing_link_result = link_shorter.get_source_link("not_existing_short_link")

        self.assertEqual(not_existing_link_result, None)

    def test_save_link_two_times(self):
        redis_mock = RedisMock()
        link_shorter = LinkShorter(redis_mock)

        test_link = "http://sample"

        short_link1 = link_shorter.save_link(test_link)
        short_link2 = link_shorter.save_link(test_link)

        saved_link1 = link_shorter.get_source_link(short_link1)
        saved_link2 = link_shorter.get_source_link(short_link2)

        self.assertEqual(saved_link1, test_link)
        self.assertEqual(saved_link2, test_link)
        self.assertEqual(short_link1, short_link2)

    def test_save_links_with_same_hash(self):
        redis_mock = RedisMock()
        alias_provider_mock = AliasProviderMock()

        link_shorter = LinkShorter(redis_mock, alias_provider_mock)

        links_with_same_hash = \
            ['https://sample1.ru',
             'https://sample2.ru',
             'https://sample3.ru']

        # imitate that this links has one hash set new method
        mocked_hash_generator = lambda l: "samehash"
        alias_provider_mock.override_get_alias_by_md5_hash(mocked_hash_generator)

        checking_dict = {}

        for link in links_with_same_hash:
            alias = link_shorter.save_link(link)
            checking_dict[alias] = link

        # reset overrode method
        alias_provider_mock.override_get_alias_by_md5_hash(None)

        links_with_diff_hash = \
            ['https://sample4.ru',
             'https://sample5.ru',
             'https://sample6.ru']

        for link in links_with_diff_hash:
            alias = link_shorter.save_link(link)
            checking_dict[alias] = link

        for k in checking_dict:
            self.assertEqual(checking_dict[k], link_shorter.get_source_link(k))

    def test_save_one_link_with_dif_case(self):
        redis_mock = RedisMock()
        link_shorter = LinkShorter(redis_mock)

        test_link1 = 'http://sample1'
        test_link2 = 'http://sample1'.upper()
        test_link3 = 'http://SaMpLe1'

        short_link1 = link_shorter.save_link(test_link1)
        short_link2 = link_shorter.save_link(test_link2)
        short_link3 = link_shorter.save_link(test_link3)

        self.assertEqual(short_link1, short_link2)
        self.assertEqual(short_link2, short_link3)
        self.assertEqual(short_link1, short_link3)

    def test_short_link_with_dif_case(self):
        redis_mock = RedisMock()
        link_shorter = LinkShorter(redis_mock)

        test_link = 'http://sample1'

        short_link = link_shorter.save_link(test_link)
        short_link_upper = short_link.upper()

        result_by_original_short_link = link_shorter.get_source_link(short_link)
        result_by_upper_short_link = link_shorter.get_source_link(short_link_upper)

        self.assertEqual(test_link, result_by_original_short_link)
        self.assertEqual(test_link, result_by_upper_short_link)


if __name__ == '__main__':
    unittest.main()
