import unittest
from Actor import Actor

class testActor(unittest.TestCase):

    def test_value_constructor(self):
        actor = Actor("Morgan Freeman", "06/01/1937")
        self.assertEqual(actor.actor_name, "Morgan Freeman", "incorrect actor name")
        self.assertEqual(actor.birth_year, "06/01/1937", "incorrect birth year")


    def test_data_constructor(self):
        data = {"actor_name": "Morgan Freeman",
                "birth_year": "06/01/1937"}
        actor = Actor(data=data)
        self.assertEqual(actor.actor_name, "Morgan Freeman", "incorrect actor name")
        self.assertEqual(actor.birth_year, "06/01/1937", "incorrect birth year")


    def test_to_JSON(self):
        actor = Actor("Morgan Freeman", "06/01/1937")
        expected = {"actor_name": "Morgan Freeman",
                    "birth_year": "06/01/1937"}
        self.assertDictEqual(actor.to_JSON(), expected, "invalid to JSON")


if __name__ == '__main__':
    unittest.main()