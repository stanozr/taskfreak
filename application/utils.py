import datetime, pytz

class utils:

    @staticmethod
    def get_timezones():
        tzgroups = {}
        tzlist = pytz.common_timezones
        for tz in tzlist:
            if '/' in tz:
                tzn = tz.split('/')
                if tzn[0] not in tzgroups:
                    tzgroups[tzn[0]] = []
                tzgroups[tzn[0]].append(tzn[1])
            else:
                tzgroups[tz] = [ tz ]
        return tzgroups