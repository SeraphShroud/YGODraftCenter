class DraftParams(object):
    """description of class"""
    def __init__(self):
        self.main_list = []
        self.extra_list = []
        self.player_length = 0
        self.round_time = 0
        self.pack_size = 0

    def set_main_list(self, main_list):
        self.main_list = main_list

    def get_main_list(self):
        return self.main_list

    def set_extra_list(self, extra_list):
        self.extra_list = extra_list

    def get_extra_list(self):
        return self.extra_list

    def set_player_length(self, player_length):
        self.player_length = player_length

    def get_player_length(self):
        return self.player_length

    def set_round_time(self, round_time):
        self.round_time = round_time

    def get_round_time(self):
        return self.round_time

    def set_pack_size(self, pack_size):
        self.pack_size = pack_size

    def get_pack_size(self):
        return self.pack_size
