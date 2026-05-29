from django.urls import path
from .views import SapUploadView

urlpatterns = [
    path(
        "upload/sap/",
        SapUploadView.as_view()
    ),
]