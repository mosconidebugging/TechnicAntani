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

from django.db import models
from django.contrib.auth.models import User


class RepoSecret(models.Model):
    owner = models.ForeignKey(User)
    repoName = models.CharField(max_length=255, primary_key=True, unique=True)
    secret = models.CharField(max_length=255)


class Error(models.Model):
    """
    Errors to display to the user
    """
    user = models.ForeignKey(User)
    error = models.TextField()