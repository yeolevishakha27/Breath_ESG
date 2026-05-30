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

        try:
            df = pd.read_csv(
                uploaded_file,
                sep=None,
                engine="python"
            )

        except Exception:
            try:
                uploaded_file.seek(0)

                df = pd.read_csv(uploaded_file)

            except Exception as e:
                return Response(
                    {
                        "error": f"CSV Read Error: {str(e)}"
                    },
                    status=400
                )

        lower_map = {
            c.lower().strip(): c
            for c in df.columns
        }

        def find_col(candidates):
            for c in candidates:
                if c.lower().strip() in lower_map:
                    return lower_map[
                        c.lower().strip()
                    ]
            return None

        qty_col = find_col([
            "Quantity",
            "Menge",
            "Qty"
        ])

        unit_col = find_col([
            "Unit",
            "Einheit"
        ])

        activity_col = find_col([
            "Fuel",
            "Activity",
            "Material",
            "Kraftstoff"
        ])

        if not qty_col:
            return Response(
                {
                    "error":
                    "Quantity column not found",
                    "columns":
                    list(df.columns)
                },
                status=400
            )

        if not unit_col:
            return Response(
                {
                    "error":
                    "Unit column not found",
                    "columns":
                    list(df.columns)
                },
                status=400
            )

        if not activity_col:
            return Response(
                {
                    "error":
                    "Fuel/Activity column not found",
                    "columns":
                    list(df.columns)
                },
                status=400
            )

        company, created = Company.objects.get_or_create(
            name="Breathe ESG Demo"
        )

        source = DataSource.objects.create(
            company=company,
            source_type="SAP",
            file_name=uploaded_file.name
        )

        suspicious_count = 0
        records_created = 0
        errors = []

        def normalize_unit(value, unit):

            try:
                value = float(value)
            except:
                return None, unit

            u = str(unit).lower().strip()

            if u == "ml":
                return value / 1000, "L"

            if u in [
                "liter",
                "litre",
                "l",
                "ltr"
            ]:
                return value, "L"

            if u in [
                "gallon",
                "gallons",
                "gal"
            ]:
                return value * 3.78541, "L"

            return value, unit

        for index, row in df.iterrows():

            try:

                qty = row[qty_col]
                unit = row[unit_col]
                activity = row[activity_col]

                try:
                    qty = float(str(qty))
                except:
                    qty = None

                normalized_value, normalized_unit = normalize_unit(
                    qty,
                    unit
                )

                suspicious = False

                if normalized_value is None:
                    suspicious = True

                if (
                    normalized_value is not None
                    and normalized_value < 0
                ):
                    suspicious = True

                if suspicious:
                    suspicious_count += 1

                EmissionRecord.objects.create(
                    company=company,
                    source=source,
                    scope="Scope 1",
                    category="Fuel Consumption",
                    activity_type=str(activity),
                    original_value=qty or 0,
                    original_unit=str(unit),
                    normalized_value=
                    normalized_value or 0,
                    normalized_unit=
                    normalized_unit,
                    is_suspicious=suspicious
                )

                records_created += 1

            except Exception as e:

                errors.append({
                    "row": index,
                    "error": str(e)
                })

        return Response({
            "message":
            "Upload processed successfully",
            "file_name":
            uploaded_file.name,
            "rows_read":
            len(df),
            "records_created":
            records_created,
            "suspicious_records":
            suspicious_count,
            "errors":
            errors[:10]
        })