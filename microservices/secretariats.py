class secretariats:
    def __init__(self, location, name, description, openHours, b_id):
        self.location = location
        self.description = description
        self.name = name
        self.openHours = openHours
        self.id = b_id

        self.likes = 0

    def __str__(self):
        return "%s - %s - %s - %s - %s" % (self.id, self.location, self.name, self.description, self.openHours)

