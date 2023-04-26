import asyncio
import time

from abc import ABC, abstractmethod
from . import State, MPD


class Player(ABC):
    @property
    @abstractmethod
    def state(self) -> State:
        """
        Get current state
        Returns
        -------
        state: State
            The current state
        """
        raise NotImplementedError

    @abstractmethod
    async def start(self, mpd_url) -> None:
        """
        Start the playback
        Parameters
        ----------
        mpd_url
        """
        raise NotImplementedError

    @abstractmethod
    def stop(self) -> None:
        """
        Stop the playback and reset everything
        """
        raise NotImplementedError

    @abstractmethod
    def pause(self) -> None:
        """
        Pause the playback
        """
        pass


class DASHPlayer(Player):
    def __init__(self,
                 update_interval: float,
                 min_rebuffer_duration: float,
                 min_start_buffer_duration: float,
                 buffer_manager: BufferManager,
                 mpd_provider: MPDProvider,
                 scheduler: Scheduler,
                 listeners: List[PlayerEventListener],
                 services: List[AsyncService] = None):
        """
        Parameters
        """

        self.update_interval = update_interval

        self.min_start_buffer_duration = min_start_buffer_duration
        self.min_rebuffer_duration = min_rebuffer_duration

        self.buffer_manager = buffer_manager
        self.scheduler = scheduler
        self.mpd_provider = mpd_provider
        self.listeners = listeners


        self.services = services if services is not None else []

        # MPD related
        self._mpd_obj: Optional[MPD] = None

        # State related
        self._state = State.IDLE

        # Actions related
        self._main_loop_task = None

        # Playback related
        self._playback_started = False
        self._position = 0.0


        async def main_loop(self) -> None:

            timestamp = 0
            while True:
                now = time.time()
                interval = now - timestamp
                timestamp = now
                
                # Update MPD object
                self._mpd_obj = self.mpd_provider.mpd

                buffer_level = self.buffer_manager.buffer_level

                await asyncio.sleep(min(buffer_level, self.update_interval) if buffer_level > 0 else self.update_interval)