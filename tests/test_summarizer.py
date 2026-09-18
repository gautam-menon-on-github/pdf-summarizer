from src import summarizer
import pytest

class FakeResponse:
    def __init__(self, text):
        self.text = text

# test that the summarize function works fine.
def test_summarize_success(monkeypatch):

    # faking the client.models.generate_content() function from summarizer.py
    # It thus needs the same parameters as that function, i.e., model and contents here.
    def fake_generate_content(model, contents):
        return FakeResponse(text="This is a fake summary")

    # now setting up monkeypatch for the generate_content function
    monkeypatch.setattr(summarizer.client.models, "generate_content", fake_generate_content)

    result = summarizer.summarize("Some input text to be summarized")
    assert result == "This is a fake summary"


# test that the custom SummarizationError exception is raised if it doesn't work.
def test_summarize_failure(monkeypatch):
    def fake_generate_content(model, contents):
        raise Exception("simulated API failure")

    monkeypatch.setattr(summarizer.client.models, "generate_content", fake_generate_content)

    with pytest.raises(summarizer.SummarizationError):
        summarizer.summarize("Some input text to be summarized")
    