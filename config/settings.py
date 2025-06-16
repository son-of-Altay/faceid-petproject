import dotenv
from split_settings.tools import include

dotenv.load_dotenv()

include(
    'components/base.py',
    'components/apps.py',
    'components/middleware.py',
    'components/templates.py',
    'components/database.py',
    'components/auth.py',
    'components/logging.py',
    'components/i18n.py',
    'components/static.py',
)
