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
        return Response({"message": "SAP Upload API Working"})

    def post(self, request):
        uploaded_file = request.FILES.get("file")

        if not uploaded_file:
            return Response({"error": "No file uploaded"}, status=400)

        # Try to read CSV and be tolerant of different delimiters/locales
        try:
            # let pandas sniff the separator
            df = pd.read_csv(uploaded_file, sep=None, engine='python')
        except Exception:
            # fallback to a simpler read with common separators
            try:
                uploaded_file.seek(0)
                df = pd.read_csv(uploaded_file)
            except Exception as e:
                return Response({"error": f"CSV Read Error: {str(e)}"}, status=400)

        # Normalize column names to ease mapping (strip / lower)
        col_map = {c.strip(): c for c in df.columns}
        lower_map = {c.lower().strip(): c for c in df.columns}

        def find_col(candidates):
            for c in candidates:
                key = c.lower().strip()
                if key in lower_map:
                    return lower_map[key]
            return None

        qty_col = find_col(["Quantity", "Menge", "Qty", "qty", "quantity"])
        unit_col = find_col(["Unit", "Einheit", "unit", "u"])
        activity_col = find_col(["Fuel", "Kraftstoff", "Activity", "activity", "Material"])

        if not qty_col or not unit_col or not activity_col:
            return Response({
                "error": "CSV missing required columns. Expected columns like Quantity/Menge, Unit/Einheit, Fuel/Activity",
                "found_columns": list(df.columns)
            }, status=400)

        company = Company.objects.first()
        if not company:
            return Response({"error": "Please create a Company first in Django Admin"}, status=400)

        source = DataSource.objects.create(company=company, source_type="SAP", file_name=uploaded_file.name)

        suspicious_count = 0
        records_created = 0
        errors = []

        # simple unit normalization map -> returns (value, unit)
        def normalize_unit(quantity, unit):
            if not isinstance(unit, str):
                unit = str(unit or "")
            u = unit.strip().lower()
            # Handle comma decimals in strings
            try:
                if isinstance(quantity, str):
                    q = float(quantity.replace(',', '').strip())
                else:
                    q = float(quantity)
            except Exception:
                # if unable to parse, propagate NaN
                q = None

            if q is None:
                return (None, unit)

            if u in ("ml", "milliliter", "millilitre"):
                return (q / 1000.0, "L")
            if u in ("l", "ltr", "liter", "litre"):
                return (q, "L")
            if u in ("gal", "gallon", "gallons"):
                return (q * 3.78541, "L")
            # default: return as-is
            return (q, unit)

        for idx, row in df.iterrows():
            try:
                raw_qty = row[qty_col]
                raw_unit = row[unit_col]
                activity = row[activity_col]

                # Attempt safe numeric parsing
                try:
                    if isinstance(raw_qty, str):
                        raw_qty_parsed = float(raw_qty.replace('.', '').replace(',', '.')) if ',' in raw_qty else float(raw_qty)
                    else:
                        raw_qty_parsed = float(raw_qty)
                except Exception:
                    raw_qty_parsed = None

                normalized_value, normalized_unit = normalize_unit(raw_qty_parsed, raw_unit)

                is_suspicious = False
                if normalized_value is None:
                    is_suspicious = True
                    suspicious_count += 1

                if normalized_value is not None and normalized_value < 0:
                    is_suspicious = True
                    suspicious_count += 1

                EmissionRecord.objects.create(
                    company=company,
                    source=source,
                    scope="Scope 1",
                    category="Fuel Consumption",
                    activity_type=str(activity),
                    original_value=raw_qty_parsed if raw_qty_parsed is not None else 0.0,
                    original_unit=str(raw_unit),
                    normalized_value=normalized_value if normalized_value is not None else 0.0,
                    normalized_unit=normalized_unit if normalized_unit else str(raw_unit),
                    is_suspicious=is_suspicious,
                )

                records_created += 1

            except Exception as e:
                errors.append({"row_index": int(idx), "error": str(e)})

        result = {
            "message": "Upload processed",
            "file_name": uploaded_file.name,
            "rows_read": len(df),
            "records_created": records_created,
            "suspicious_records": suspicious_count,
            "errors": errors[:10]
        }

        return Response(result)