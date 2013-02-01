from bitdeli.widgets import set_theme, Description, Title
from bitdeli.chain import Profiles
from collections import Counter
from datetime import datetime, timedelta

TIMELINE_DAYS = 30 
TFORMAT = '%Y-%m-%d'

text = {'window': TIMELINE_DAYS}


def activity(profiles):
    limit = datetime.now() - timedelta(days=TIMELINE_DAYS)
    limit_str = limit.strftime(TFORMAT)
    
    def recent_days(pageviews):
        for pageview in pageviews:
            day = pageview[0].split('T')[0]
            if day >= limit_str:
                yield day
    
    def timeline(stats):
        for i in range(TIMELINE_DAYS + 1):
            day = (limit + timedelta(days=i)).strftime(TFORMAT)
            yield day, stats[day]

    def top_day(uniques):
        top_day = uniques.most_common(1)[0]
        return (datetime.strptime(top_day[0], TFORMAT).strftime('%B %d'),
                top_day[1])
            
    pageviews = Counter()
    uniques = Counter()
    for profile in profiles:
        if '$pageview' not in profile:
            continue
        pageviews.update(recent_days(profile['$pageview']))
        uniques.update(frozenset(recent_days(profile['$pageview'])))

    if uniques:
        text['top_day'] = top_day(uniques)
    text['total'] = len(list(uniques.elements()))

    Title("{total} daily unique visitors in total "
          "over the last {window} days",
          text)
    if 'top_day' in text:
        Description("{top_day[0]} was the most active day with "
                    "{top_day[1]} unique visitors.",
                    text)
    
    yield {'type': 'line',
           'label': 'Daily Visitors',
           'data': [{'label': 'Pageviews',
                     'data': list(timeline(pageviews))},
                    {'label': 'Unique Visitors',
                     'data': list(timeline(uniques))}],
           'size': (12, 4)}
     

Profiles().map(activity).show()
