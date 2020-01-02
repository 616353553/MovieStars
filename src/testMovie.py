import unittest
from Movie import Movie

class testMovie(unittest.TestCase):

    def test_value_constructor(self):
        movie = Movie("Iron Man", "2008", 585200000)
        self.assertEqual(movie.movie_name, "Iron Man", "incorrect movie name")
        self.assertEqual(movie.release_year, "2008", "incorrect release year")
        self.assertEqual(movie.gross_value, 585200000, "inorrect gross value")


    def test_data_constructor(self):
        data = {"movie_name": "Iron Man",
                "release_year": "2008",
                "gross_value": 585200000}
        movie = Movie(data=data)
        self.assertEqual(movie.movie_name, "Iron Man", "incorrect movie name")
        self.assertEqual(movie.release_year, "2008", "incorrect release year")
        self.assertEqual(movie.gross_value, 585200000, "inorrect gross value")


    def test_to_JSON(self):
        movie = Movie("Iron Man", "2008", 585200000)
        expected = {"movie_name": "Iron Man",
                    "release_year": "2008",
                    "gross_value": 585200000}
        self.assertDictEqual(movie.to_JSON(), expected, "invalid to JSON")


if __name__ == '__main__':
    unittest.main()