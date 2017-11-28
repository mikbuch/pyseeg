import datetime


def generate_output_path(name, user, sub='00', date_and_time=True):

    time_code = datetime.datetime.today().strftime('%Y-%m-%d-%h-%s')
    print('\nTime started:\n%s\n' % time_code)

    if date_and_time:
        path = '/home/%s/%s_%s_%s.csv' % (user, name, sub, time_code)
    else:
        path = '/home/%s/%s_%s_.csv' % (user, name, sub)

    return path
