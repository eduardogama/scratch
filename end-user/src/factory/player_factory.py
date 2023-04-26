from model.Player import Player, DASHPlayer
from emulator import Config
from emulator.event_logger import EventLogger


def build_dash_player() -> Player:
    """
    Build a MPEG-DASH Player
    Returns
    -------
    player: Player
        A MPEG-DASH Player
    """
    cfg = Config
    event_logger = EventLogger()

    return DASHPlayer(cfg.update_interval, min_rebuffer_duration=1, min_start_buffer_duration=2,
                      listeners=[event_logger])