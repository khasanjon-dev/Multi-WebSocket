from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

swagger_urlpatterns = [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"
    ),
]
