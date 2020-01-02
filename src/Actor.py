class Actor:

    def __init__(self, actor_name=None, birth_year=None, data=None):
        if (data is None):
            self.actor_name = actor_name
            self.birth_year = birth_year
        else:
            self.actor_name = data["actor_name"]
            self.birth_year = data["birth_year"]


    def to_JSON(self):
        return {"actor_name": self.actor_name,
                "birth_year": self.birth_year}
