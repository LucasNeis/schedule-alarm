class FileReader:

    _stored = dict()

    def read_into_list(self, path:str, store=False) -> list:
        if (path in self._stored):
            return self._stored[path]
        text_file = open(path)
        phrases = text_file.readlines()
        phrases = [i.replace("\n", "") for i in phrases]
        if store:
            self._stored[path] = phrases
        return phrases