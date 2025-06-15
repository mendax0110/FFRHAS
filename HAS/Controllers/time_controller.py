import time
from datetime import datetime, timezone
from flask.json import dumps
from threading import Thread, Event, Lock

from Services.Repositories import LoggingRepository, LoggingData, LoggingType, Source
from Services.http_clients import EswClient


class TimeController:
    def __init__(self):
        self.__logger = LoggingRepository()
        self.__timeIntervalInSeconds = 60
        self.__worstCaseDriftInSeconds = 2
        self.__timer_thread = None
        self.__stop_event = Event()
        self.__thread_lock = Lock()  # Protects access to thread/event objects

    def get_time(self):
        now = datetime.now(timezone.utc)  # Get current time in UTC
        iso_string = now.strftime("%Y-%m-%dT%H:%M:%SZ")
        response = {"time": iso_string}

        loggingData = LoggingData(Source.HAS, LoggingType.Info, "time was requested", iso_string)
        self.__logger.write_one(loggingData)

        # Stop existing thread if it's running
        with self.__thread_lock:
            if self.__timer_thread and self.__timer_thread.is_alive():
                self.__stop_event.set()
                self.__timer_thread.join()

            # Start new thread and reset event
            self.__stop_event = Event()
            self.__timer_thread = Thread(
                target=self.start_timer_for_next_request,
                args=(self.__stop_event,),
                daemon=True
            )
            self.__timer_thread.start()

        return dumps(response), 200

    def start_timer_for_next_request(self, stop_event: Event):
        with EswClient.lock:
            EswClient.pauseEndpointQueue = False

        sleep_time = self.__timeIntervalInSeconds - self.__worstCaseDriftInSeconds
        for _ in range(sleep_time):
            if stop_event.is_set():
                return  # Exit early if cancelled
            time.sleep(1)

        if not stop_event.is_set():
            with EswClient.lock:
                EswClient.pauseEndpointQueue = True
