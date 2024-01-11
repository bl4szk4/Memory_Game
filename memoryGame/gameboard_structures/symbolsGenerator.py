import os


class SymbolsGenerator:
    """
    This class generates all information about symbols used in memory memoryGame
    """
    @staticmethod
    def generate_symbols_dict() -> {}:
        """Generates dictionary with all symbols names and empty list for storing their coordinates"""
        symbols_dict = {}
        for filename in os.listdir('images'):
            symbols_dict[filename[:-4]] = []
        return symbols_dict

    @staticmethod
    def generate_symbols_revealed() -> {}:
        symbols_dict = {}
        for filename in os.listdir('images'):
            symbols_dict[filename[:-4]] = 0
        return symbols_dict
