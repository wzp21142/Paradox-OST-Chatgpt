class ymlFile:
    def __init__(self):
        self.content = None
        self.filePath = None
    def __init__(self, content, filePath):
        self.content = content
        self.filePath = filePath
    def __str__(self):
        return self.filePath+"\n"+str(self.content)+"\n"