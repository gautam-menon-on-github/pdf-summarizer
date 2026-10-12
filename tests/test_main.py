from fastapi.testclient import TestClient
from src import main, summarizer
import pytest

client = TestClient(main.app)

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
        b"",                                  # empty
        b"%JPG-0001111",                      # not a PDF
        b"%PDF-" + b"0" * 11 * 1024 * 1024,   # too large
        b"%PDF-12345",                        # valid header, corrupt body
    ],
    ids=["empty", "not_pdf", "too_large", "corrupt"]
)
def test_summarize_invalid_input_returns_400(monkeypatch, content):
    def guard():
        raise AssertionError("summarize must not be called with invalid inputs!")

    monkeypatch.setattr(main.summarizer, "summarize", content)

    response = client.post(
        "/summarize",
        files={"file": ("test.pdf", content, "application/pdf")}
    )

    assert response.status_code == 400
    