import unittest

from link_shorter import LinkShorter
from tests.redis_mock import RedisMock


class LinkShorterTests(unittest.TestCase):

    def test_save_link(self):

        redis_mock = RedisMock()
        link_shorter = LinkShorter(redis_mock)

        test_link = "http://sample"

        short_link = link_shorter.save_link(test_link)
        saved_link = redis_mock.get(short_link)

        self.assertEqual(saved_link, test_link)

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
        self.assertNotEqual(short_link1, short_link2)


if __name__ == '__main__':
    unittest.main()
