from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser

import pandas as pd

from emissions.models import (
    Company,
    DataSource,
    EmissionRecord
)


class SapUploadView(APIView):

    parser_classes = [MultiPartParser]

    def get(self, request):
        return Response({
            "message": "SAP Upload API Working"
        })

    def post(self, request):

        uploaded_file = request.FILES.get("file")

        if not uploaded_file:
            return Response(
                {"error": "No file uploaded"},
                status=400
            )

        df = pd.read_csv(uploaded_file)

        company = Company.objects.first()

        if not company:
            return Response(
                {
                    "error": "Please create a Company first in Django Admin"
                },
                status=400
            )

        source = DataSource.objects.create(
            company=company,
            source_type="SAP",
            file_name=uploaded_file.name
        )

        suspicious_count = 0

        for _, row in df.iterrows():

            quantity = float(row["Quantity"])
            unit = str(row["Unit"])

            is_suspicious = False

            if quantity < 0:
                is_suspicious = True
                suspicious_count += 1

            normalized_value = quantity
            normalized_unit = unit

            if unit.lower() == "ml":
                normalized_value = quantity / 1000
                normalized_unit = "L"

            EmissionRecord.objects.create(
                company=company,
                source=source,

                scope="Scope 1",
                category="Fuel Consumption",
                activity_type=row["Fuel"],

                original_value=quantity,
                original_unit=unit,

                normalized_value=normalized_value,
                normalized_unit=normalized_unit,

                is_suspicious=is_suspicious
            )

        return Response({
            "message": "Upload successful",
            "rows_processed": len(df),
            "suspicious_records": suspicious_count
        })


class ReviewQueueView(APIView):

    def get(self, request):

        records = EmissionRecord.objects.all()

        data = []

        for record in records:
            data.append({
                "id": record.id,
                "fuel": record.activity_type,
                "value": record.original_value,
                "unit": record.original_unit,
                "normalized_value": record.normalized_value,
                "normalized_unit": record.normalized_unit,
                "status": record.status,
                "suspicious": record.is_suspicious
            })

        return Response(data)


class UpdateStatusView(APIView):

    def post(self, request, record_id):

        status = request.data.get("status")

        record = EmissionRecord.objects.get(id=record_id)

        record.status = status

        if status == "APPROVED":
            record.locked_for_audit = True

        record.save()

        return Response({
            "message": "Status Updated"
        })