import secretariats
import pickle


class secretariatsDB:
        def __init__(self, name):
                self.name = name
                try:
                        f = open('bd_dump'+name, 'rb')
                        self.db = pickle.load(f)
                        f.close()
                except IOError:
                        self.db = {}

        def addSecretariats(self,location, name, description, openHours):
                s_id = len(self.db)
                self.db[s_id] = secretariats.secretariats(location, name, description, openHours, s_id)
                f = open('bd_dump'+self.name, 'wb')
                pickle.dump(self.db, f)
                f.close()
                return s_id
                
        def showSecretariat(self, b_id):
                return self.db[b_id]

        def listSecretariats(self):
                return list(self.db.values())

        def chageSecretariats(self, location, name, description, openHours, s_id):
                self.db[s_id].location = location
                self.db[s_id].name = name
                self.db[s_id].description = description
                self.db[s_id].openHours = openHours
                f = open('bd_dump'+self.name, 'wb')
                pickle.dump(self.db, f)
                f.close()
