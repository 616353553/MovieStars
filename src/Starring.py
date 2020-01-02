class Starring:

    def __init__(self, actor_name=None, movie_name=None, weight=None, data=None):
        if (data is None):
            self.actor_name = actor_name
            self.movie_name = movie_name
            self.weight = weight
        else:
            self.actor_name = data["actor_name"]
            self.movie_name = data["movie_name"]
            self.weight = data["weight"]


    def to_JSON(self):
        return {"actor_name": self.actor_name,
                "movie_name": self.movie_name,
                "weight": self.weight}