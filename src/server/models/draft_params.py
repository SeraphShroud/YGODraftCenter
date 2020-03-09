class DraftParams(object):
    """description of class"""
    def __init__(self):
        self.main_list = []
        self.extra_list = []
        self.player_length = 0
        self.round_time = 0
        self.pack_size = 0

    def setMainList(self, main_list):
        self.main_list = main_list

    def getMainList(self):
        return self.main_list

    def setExtraList(self, extra_list):
        self.extra_list = extra_list

    def getExtraList(self):
        return self.extra_list

    def setPlayerLength(self, player_length):
        self.player_length = player_length

    def getPlayerLength(self):
        return self.player_length

    def setRoundTime(self, round_time):
        self.round_time = round_time

    def getRoundTime(self):
        return self.round_time

    def setPackSize(self, pack_size):
        self.pack_size = pack_size

    def getPackSize(self):
        return self.pack_size
