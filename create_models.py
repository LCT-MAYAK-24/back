from gigachat.models import db, Conversation, Message
from users.models import User, Settings, Place
from places.models import Favorite
from feedback.models import Feedback

db.connect()
# db.create_tables([User, Settings, Place, Conversation, Message, Favorite])
db.create_tables([Feedback])
