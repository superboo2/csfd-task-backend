from rest_framework import routers
from . import views


router = routers.DefaultRouter(trailing_slash=False)
router.register("actor", views.ActorViewSet, basename="actor")
router.register("film", views.FilmViewSet, basename="film")

urlpatterns = router.urls
