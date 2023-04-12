class Translator:
    def __init__(self):
        self.translation_table = {
                ord('æ'): 'a',
                ord('ø'): 'o',
                ord('å'): 'a',
                ord('Æ'): 'A',
                ord('Ø'): 'O',
                ord('Å'): 'A'
            }

    def replace(self, string: str):
        return string.translate(self.translation_table)
