import re
import datetime


TIME_MULT = {
    'h': 60 * 60,
    'm': 60,
    's': 1
}


def parse_query(query, default_text='Time is up!'):
    """
    >>> '5m hello world'
    <<< (300, '5m', 'hello world')
    >>> '3h Go'
    <<< (3*60*60, '3h', 'Go')
    >>> '5'
    <<< (300, '5', 'Time is up!')
    >>> 'at 15:30'
    <<< (timedelate_from_now_in_seconds, '15:30', 'Time is up!')
    >>> 'at 15'
    <<< (timedelate_from_now_in_seconds, '15', 'Time is up!')
    """
    try:
        regex = r'''
        ^((
            (?P<at>at\ )            # at
            (?P<clock>
                (2[0-3]|[01]?[0-9]) # 0-23
                (:([0-5][0-9]))?    # :0-59 (optional)
            )
        )|                          # OR
            ^(?P<time>\d+)          # 0-infinite digit
            (?P<measure>[mhs])?     # mhs (optional, default: m)
        )                              
        (?P<message>\ .*)?$         # optional message
        '''
        m = re.match(regex, query, re.IGNORECASE | re.VERBOSE)
        
        if m.group('at') is not None:
            now = datetime.datetime.now()
            clock = m.group('clock').split(":")

            # if input has no minutes set to 0
            if(len(clock) == 1):
                  clock.append(0)
            # calculate delta between now and inputed clock
            # if clock > now: set timer to next day
            time_sec = int((datetime.timedelta(hours=24) - (now - now.replace(hour=int(clock[0]), minute=int(clock[1])))).total_seconds() % (24 * 3600)) 
            time_arg = m.group('clock')
        else:
            time_sec = int(m.group('time')) * TIME_MULT[(m.group('measure') or 'm').lower()]
            time_arg = m.group('time') + (m.group('measure') or "")

        message = m.group('message') or default_text

        return (time_sec, time_arg, message[1:])
    except Exception as e:
        raise ParseQueryError(str(e))


class ParseQueryError(Exception):
    pass
