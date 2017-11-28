import os
from urllib2 import urlopen, URLError, HTTPError
import zipfile


def dlfile(url, dst=None):
    if dst is None:
        dst = os.path.basename(url)
    # Open the url
    try:
        f = urlopen(url)
        print "Downloading file:\n%s\n" % url

        # Open our local file for writing
        with open(dst, "wb") as local_file:
            local_file.write(f.read())

    #handle errors
    except HTTPError, e:
        print "HTTP Error:", e.code, url
    except URLError, e:
        print "URL Error:", e.reason, url


def fetch_stimuli(stim_type, target_dir):

    # Check if dir exists.
    final_dir = os.path.join(target_dir, '%s_img' % stim_type)
    if os.path.exists(final_dir):
        print('Stimuli already present on this machine.\n')

    else:
        print('Downloading and unzipping ...\n')
        # Download file.
        if stim_type == 'p300':
            url = 'http://mj19648.home.amu.edu.pl/p300_img.zip'
        path_to_zip_file = '/tmp/%s_img.zip' % stim_type

        # Download file.
        dlfile(url, path_to_zip_file)

        # Prepare directory.
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        # Extract zip.
        print('Extracting file: %s\n' % path_to_zip_file)
        zip_ref = zipfile.ZipFile(path_to_zip_file, 'r')
        zip_ref.extractall(target_dir)
        zip_ref.close()
