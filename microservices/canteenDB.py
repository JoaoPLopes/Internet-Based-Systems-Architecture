import pickle


class canteenDB:
        def __init__(self, name):
                self.name = name
                try:
                        f = open('bd_dump'+name, 'rb')
                        self.db = pickle.load(f)
                        f.close()
                except IOError:
                        self.db = {}

        def addSemana(self, semana):
                for dia in semana:
                    s_id = len(self.db)
                    self.db[dia['day']] = dia['meal']
                    f = open('bd_dump'+self.name, 'wb')
                    pickle.dump(self.db, f)
                    f.close()
                return s_id
                
        def showDia(self, data):
            try:
                meal = self.db[data]
            except:
                meal = {}
            return meal
