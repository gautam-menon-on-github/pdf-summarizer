from fastapi.testclient import TestClient
from src import main, summarizer
import pymupdf
import pytest

client = TestClient(main.app)


def _read_empty_pdf_fixture():
    with open("tests/fixtures/empty_pdf_file.pdf", "rb") as f:
        return f.read()


def _make_whitespace_only_pdf():
    with pymupdf.open() as doc:
        page = doc.new_page()
        page.insert_text((72, 72), "   ")
        return doc.tobytes()


def test_read_root():
    response = client.get("/status")

    assert response.status_code == 200
    assert response.json() == {"message": "FastAPI is working"}


def test_summarize_success(monkeypatch):
    monkeypatch.setattr(main.summarizer, "summarize", lambda text: "fake summary")

    with open("tests/fixtures/attention_is_all_you_need.pdf", "rb") as f:
        response = client.post(
            "/summarize",
            files={"file": ("test.pdf", f, "application/pdf")}
        )

    assert response.status_code == 200
    assert response.json() == {"summary": "fake summary"}


# here, note that main.summarize is being called
# NOT summarizer.summarize
# Hence, the param in fake_summarize() is "text"
def test_summarize_failure(monkeypatch):
    def fake_summarize(text):
        raise summarizer.SummarizationError("simulated LLM failure")

    monkeypatch.setattr(main.summarizer, "summarize", fake_summarize)

    with open("tests/fixtures/attention_is_all_you_need.pdf", "rb") as f:
        response = client.post(
            "/summarize",
            files={"file": ("test.pdf", f, "application/pdf")}
        )

        assert response.status_code == 500


@pytest.mark.parametrize(
    "content",
    [
        b"",  # empty
        b"%JPG-0001111",  # not a PDF
        b"%PDF-" + b"0" * (main.validator.MAX_PDF_SIZE_BYTES + 1 - len(b"%PDF-")),  # too large
        b"%PDF-12345",  # valid header, corrupt body
    ],
    ids=["empty", "not_pdf", "too_large", "corrupt"],
)
def test_summarize_invalid_input_returns_400(monkeypatch, content):
    def guard(text):
        raise AssertionError("summarize must not be called with invalid inputs!")

    monkeypatch.setattr(main.summarizer, "summarize", guard)

    response = client.post(
        "/summarize",
        files={"file": ("test.pdf", content, "application/pdf")},
    )

    assert response.status_code == 400


@pytest.mark.parametrize(
    "pdf_factory",
    [_read_empty_pdf_fixture, _make_whitespace_only_pdf],
    ids=["blank_fixture", "whitespace_only"],
)
def test_summarize_pdf_without_extractable_text_returns_422(monkeypatch, pdf_factory):
    def guard(text):
        raise AssertionError("summarize must not be called without extractable text")

    monkeypatch.setattr(main.summarizer, "summarize", guard)

    response = client.post(
        "/summarize",
        files={"file": ("test.pdf", pdf_factory(), "application/pdf")},
    )

    assert response.status_code == 422
    assert response.json() == {
        "detail": "The uploaded PDF contains no extractable text."
    }
