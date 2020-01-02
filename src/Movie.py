class Movie:

    def __init__(self, movie_name=None, release_year=None, gross_value=None, data=None):
        if (data is None):
            self.movie_name = movie_name
            self.release_year = release_year
            self.gross_value = gross_value
        else:
            self.movie_name = data["movie_name"]
            self.release_year = data["release_year"]
            self.gross_value = data["gross_value"]


    def to_JSON(self):
        return {"movie_name": self.movie_name,
                "release_year": self.release_year,
                "gross_value": self.gross_value}

        
