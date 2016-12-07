"""
App Engine config
`appengine_config` gets loaded when starting a new application instance.

"""

from google.appengine.ext import vendor

def gae_mini_profiler_should_profile_production():
    """Uncomment the first two lines to enable GAE Mini Profiler on production for admin accounts"""
    # from google.appengine.api import users
    # return users.is_current_user_admin()
    return False

# Add any libraries install in the "lib" folder.
vendor.add('lib')
