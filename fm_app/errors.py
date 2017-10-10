import sys
import traceback


class Error(Exception):

    @staticmethod
    def get_text_from_error(error):
        _, _, tb = sys.exc_info()
        traceback.print_tb(tb)
        tb_info = traceback.extract_tb(tb)
        filename_, line_, func_, text_ = tb_info[-1]
        message = '\nAn error occurred on File "{file}" line {line}\n {assert_message}'.\
            format(line=line_, file=filename_, assert_message=error.args,)
        return message


class IcesException(Error):
    def __init__(self, message, err=None):
        self.message = message
        if err:
            self.message += self.get_text_from_error(err)
        super(IcesException, self).__init__(message)


class PlaylistException(IcesException):
    pass
