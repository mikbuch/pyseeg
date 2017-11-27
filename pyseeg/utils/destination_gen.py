import datetime


def generate_output_path(name, user, sub='00', date_and_time=True):

    time_code = datetime.datetime.today().strftime('%Y-%m-%d-%h-%s')

    if date_and_time:
        path = '/home/%s/%s_%s.csv' % (user, name, time_code)
    else:
        path = '/home/%s/%s_.csv' % (user, name)

    return path
