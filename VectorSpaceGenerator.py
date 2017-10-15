from storedb.database import Database

__author__ = 'tintin'

class VectorSpaceMaker():
    def __init__(self):
        self.database = Database("http://localhost:7474/db/data/")
        self.allcontent = {}

    def getLinksandContents(self):
        pages = self.database.gdb.nodes.indexes.get("WebPageIndex").all()
        for page in pages:
            try:
                self.allcontent[page.properties['weburl']] = page.properties['content']
            except:
                print("Error getting value from database index trainer.py")
                continue
        '''get all content webpages and make a dimension out of it, initially'''
        '''for i in range(1, 1600):
            try:
                self.allcontent[self.database.gdb.nodes.get(i).properties['weburl']] = \
                    self.database.gdb.nodes.get(i).properties['content']
            except:
                continue'''
        return self.allcontent