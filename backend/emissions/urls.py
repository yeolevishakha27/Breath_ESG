from django.urls import path

from .views import (
    SapUploadView,
    ReviewQueueView,
    UpdateStatusView
)

urlpatterns = [
    path(
        "upload/sap/",
        SapUploadView.as_view()
    ),

    path(
        "review/",
        ReviewQueueView.as_view()
    ),

    path(
        "review/<int:record_id>/",
        UpdateStatusView.as_view()
    ),
]