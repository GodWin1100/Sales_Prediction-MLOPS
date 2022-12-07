# ? traceback module provides deep traceback of the exception where it occurred
# https://stackoverflow.com/a/47659065
import sys


class SalesPredictionException(Exception):
    def __init__(self, error_message: Exception):
        """Return error message with filename, line number where it was captured and message of the exception.
        Nested captured traceback included.

        Args:
            error_message (Exception): exception object
        """
        super().__init__(error_message)
        self.error_message = SalesPredictionException.__get_detailed_error_message(error_message)

    @staticmethod
    def __get_detailed_error_message(error_message: Exception) -> str:
        """Return detailed error traceback

        Args:
            error_message (Exception): Exception Object

        Returns:
            str: Error description
        """
        _, _, exec_tb = sys.exc_info()
        # exc_info() #? (type, value, traceback) return information about the most recent exception caught by an except clause in the current stack frame
        line_no = exec_tb.tb_lineno  # this will give line no. of where exception occurred
        except_line_no = exec_tb.tb_frame.f_lineno  # ! This will give line no. of except block
        file_name = exec_tb.tb_frame.f_code.co_filename
        error_detail = f"\n\tError occurred in:\n\t{file_name}: [{line_no}],\n\tError captured at [{except_line_no}],\n\tError Message: {error_message}"
        return error_detail

    def __str__(self) -> str:
        return self.error_message

    def __repr__(self) -> str:
        return SalesPredictionException.__name__.str()
