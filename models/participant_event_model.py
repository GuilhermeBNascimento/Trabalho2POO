class ParticipantEvent:
    def __init__(self, event, participant, time_entrance, time_leave):
        self.__event = event
        self.__participant = participant
        self.__time_entrance = time_entrance
        self.__time_leave = time_leave

    def __get_formatted_hour(self, hour):
        if (hour):
            return hour.strftime('%H:%M')
        else:
            return 'x'

    def to_raw(self):
        return {
            "event": self.event.to_raw(),
            "participant": self.participant.to_raw(),
            "time_entrance": self.__get_formatted_hour(self.time_entrance),
            "time_leave": self.__get_formatted_hour(self.time_leave),
        }

    @property
    def event(self):
        return self.__event

    @event.setter
    def event(self, event: str):
        self.__event = event

    @property
    def participant(self):
        return self.__participant

    @participant.setter
    def participant(self, participant: str):
        self.__participant = participant

    @property
    def time_entrance(self):
        return self.__time_entrance

    @time_entrance.setter
    def time_entrance(self, time_entrance: str):
        self.__time_entrance = time_entrance

    @property
    def time_leave(self):
        return self.__time_leave

    @time_leave.setter
    def time_leave(self, time_leave: str):
        self.__time_leave = time_leave
