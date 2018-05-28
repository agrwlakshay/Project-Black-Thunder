from .views import app
from .models import Unique


Unique.topic_uniqueness_constraint()
Unique.event_uniqueness_constraint()
