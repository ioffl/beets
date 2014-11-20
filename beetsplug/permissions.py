"""Fixes file permissions after the file gets written on import. Put something
like the following in your config.yaml to configure:

    permissions:
            file: 644
"""
import os
from beets import config, util
from beets.plugins import BeetsPlugin


def convert_perm(perm):
    """If the perm is a int it will first convert it to a string and back
    to an oct int. Else it just converts it to oct.
    """
    if isinstance(perm, int):
        return int(str(perm), 8)
    else:
        return int(perm, 8)


def check_permissions(path, permission):
    """Checks the permissions of a path.
    """
    return oct(os.stat(path).st_mode & 0o777) == oct(permission)


class Permissions(BeetsPlugin):
    def __init__(self):
        super(Permissions, self).__init__()

        # Adding defaults.
        self.config.add({
            u'file': 644
        })


@Permissions.listen('item_copied')
def permissions(item, source, destination):
    """Running the permission fixer.
    """
    # Getting the config.
    file_perm = config['permissions']['file'].get()

    # Converts file permissions to oct.
    file_perm = convert_perm(file_perm)

    # Changing permissions on the destination path.
    os.chmod(util.bytestring_path(destination), file_perm)

    # Checks if the destination path has the permissions configured.
    if not check_permissions(util.bytestring_path(destination), file_perm):
        message = 'There was a problem setting permission on {}'.format(
            destination)
        print(message)
