#############################################################################
#                                                                           #
#    This program is free software: you can redistribute it and/or modify   #
#    it under the terms of the GNU General Public License as published by   #
#    the Free Software Foundation, either version 3 of the License, or      #
#    (at your option) any later version.                                    #
#                                                                           #
#    This program is distributed in the hope that it will be useful,        #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of         #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
#    GNU General Public License for more details.                           #
#                                                                           #
#    You should have received a copy of the GNU General Public License      #
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.  #
#                                                                           #
#############################################################################

import logging
from cachebuilder.models import Error
from TechnicAntani.antanisettings import LOGLEVEL


class DatabaseLogger(logging.Handler):
    """
    Detain all the logs
    """
    def __init__(self, user=None):
        super.__init__(level=LOGLEVEL)
        self.user = user

    def handle(self, record):
        e = Error()
        e.user = self.user

        msg = record.getMessage()
        if record.exc_info:
            msg += "\n"
            for e in record.exc_info:
                msg += e.__str__() + "\n"
        if record.levelno is not None:
            with record.levelno as lvl:
                if lvl == logging.INFO:
                    e.style = "info"
                if lvl == logging.WARNING:
                    e.style = "warning"
                if lvl == logging.ERROR:
                    e.style = "error"
                if lvl == logging.DEBUG:
                    e.style = "success"

        e.error = msg
        e.save()