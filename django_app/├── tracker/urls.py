from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, LogViewSet

router = DefaultRouter()
router.register(r"tasks", TaskViewSet)
router.register(r"logs", LogViewSet)

urlpatterns = router.urls
