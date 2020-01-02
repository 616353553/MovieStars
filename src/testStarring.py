import unittest
from Starring import Starring

class testMovie(unittest.TestCase):

    def test_value_constructor(self):
        starring = Starring("Morgan Freeman", "Iron Man", 4)
        self.assertEqual(starring.actor_name, "Morgan Freeman", "incorrect actor name")
        self.assertEqual(starring.movie_name, "Iron Man", "incorrect movie name")
        self.assertEqual(starring.weight, 4, "incorrect weight")


    def test_data_constructor(self):
        data = {"actor_name": "Morgan Freeman",
                "movie_name": "Iron Man",
                "weight": 4}
        starring = Starring(data=data)
        self.assertEqual(starring.actor_name, "Morgan Freeman", "incorrect actor name")
        self.assertEqual(starring.movie_name, "Iron Man", "incorrect movie name")
        self.assertEqual(starring.weight, 4, "incorrect weight")


    def test_to_JSON(self):
        starring = Starring("Morgan Freeman", "Iron Man", 4)
        expected = {"actor_name": "Morgan Freeman",
                    "movie_name": "Iron Man",
                    "weight": 4}
        self.assertDictEqual(starring.to_JSON(), expected, "invalid to JSON")


if __name__ == '__main__':
    unittest.main()