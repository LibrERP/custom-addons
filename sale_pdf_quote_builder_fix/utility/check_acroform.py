#!/usr/bin/env python3
# This script check if pdf contains the form fields

import sys
from pypdf import PdfReader


def check_acroform(pdf_path):
    print(f"\nChecking file: {pdf_path}\n")

    reader = PdfReader(pdf_path)

    # Access trailer and root catalog
    trailer = reader.trailer
    root = trailer.get("/Root")

    if not root:
        print("❌ No /Root found in trailer.")
        return

    print("✔ /Root found.")

    acroform = root.get("/AcroForm")

    if not acroform:
        print("❌ No /AcroForm referenced in /Root.")
        return

    print("✔ /AcroForm found in /Root.")

    # Resolve indirect object if necessary
    acroform_obj = acroform.get_object()

    fields = acroform_obj.get("/Fields")

    if not fields:
        print("⚠ /AcroForm exists but /Fields is empty or missing.")
        return

    print(f"✔ Found {len(fields)} field(s):\n")

    for i, field in enumerate(fields, 1):
        field_obj = field.get_object()
        name = field_obj.get("/T")
        field_type = field_obj.get("/FT")
        print(f"{i}. Name: {name}, Type: {field_type}")

    print("\nDone.\n")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_acroform.py <pdf_file>")
        sys.exit(1)

    check_acroform(sys.argv[1])
