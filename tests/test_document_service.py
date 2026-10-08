"""Tests for upload filename sanitization and PDF validation."""

import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tests.helpers import ensure_sentence_transformers_importable

ensure_sentence_transformers_importable()

from app.config.settings import settings  # noqa: E402
from app.services.document_service import (  # noqa: E402
    DocumentService,
    InvalidUploadError,
    safe_pdf_filename,
)

PDF_BYTES = b"%PDF-1.4\n%fake test pdf\n"


class SafePdfFilenameTests(unittest.TestCase):
    def test_keeps_a_plain_pdf_name(self):
        self.assertEqual(safe_pdf_filename("notes.pdf"), "notes.pdf")

    def test_strips_directory_traversal_and_absolute_paths(self):
        cases = {
            "../../etc/evil.pdf": "evil.pdf",
            "/etc/evil.pdf": "evil.pdf",
            "..\\..\\windows\\evil.pdf": "evil.pdf",
            "C:\\Users\\me\\evil.pdf": "evil.pdf",
            "nested/dir/report.PDF": "report.PDF",
        }
        for raw, expected in cases.items():
            with self.subTest(raw=raw):
                self.assertEqual(safe_pdf_filename(raw), expected)

    def test_rejects_empty_and_dot_names(self):
        for raw in [None, "", "   ", ".", "..", "../", "dir/.."]:
            with self.subTest(raw=raw):
                with self.assertRaises(InvalidUploadError):
                    safe_pdf_filename(raw)

    def test_rejects_non_pdf_extensions(self):
        for raw in ["evil.sh", "notes.pdf.exe", "pdf", "archive.zip"]:
            with self.subTest(raw=raw):
                with self.assertRaises(InvalidUploadError):
                    safe_pdf_filename(raw)

    def test_rejects_null_bytes(self):
        with self.assertRaises(InvalidUploadError):
            safe_pdf_filename("evil\x00.pdf")


class SavePdfTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.upload_dir = self.root / "uploads"
        patcher = mock.patch.object(settings, "upload_dir", self.upload_dir)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.addCleanup(self.tmp.cleanup)
        self.service = DocumentService()

    def test_saves_valid_pdf_inside_upload_dir(self):
        saved = Path(self.service.save_pdf("notes.pdf", PDF_BYTES))

        self.assertEqual(saved.parent, self.upload_dir.resolve())
        self.assertEqual(saved.read_bytes(), PDF_BYTES)

    def test_traversal_name_cannot_escape_upload_dir(self):
        saved = Path(self.service.save_pdf("../../escaped.pdf", PDF_BYTES))

        self.assertEqual(saved.parent, self.upload_dir.resolve())
        self.assertFalse((self.root / "escaped.pdf").exists())

    def test_rejects_content_without_pdf_signature(self):
        with self.assertRaises(InvalidUploadError):
            self.service.save_pdf("notes.pdf", b"#!/bin/sh\necho pwned\n")

        self.assertFalse((self.upload_dir / "notes.pdf").exists())


if __name__ == "__main__":
    unittest.main()
