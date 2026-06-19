from datetime import datetime, timezone
from database.mongo import get_db

class ActivityService:
    @staticmethod
    def log(user, action, entity='', status='Success'):
        name = getattr(user, 'name', None) or str(user or 'System')
        get_db().activity_logs.insert_one({
            'user': name,
            'action': action,
            'entity': entity,
            'status': status,
            'timestamp': datetime.now(timezone.utc),
        })

    @staticmethod
    def recent(limit=10, skip=0):
        return list(get_db().activity_logs.find().sort('timestamp', -1).skip(skip).limit(limit))
