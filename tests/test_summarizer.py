from src import summarizer
import pytest
from types import SimpleNamespace

class FakeResponse:
    def __init__(self, content):
        self.choices = [SimpleNamespace(message=SimpleNamespace(content=content))]


# test that the summarize function works fine.
def test_summarize_success(monkeypatch):

    # faking the client.chat.completions.create() function from summarizer.py
    # It thus needs the same parameters as that function, i.e., messages and model here.
    def fake_create(messages, model):
        return FakeResponse(content="This is a fake summary")

    # now setting up monkeypatch for the create() function
    monkeypatch.setattr(summarizer.client.chat.completions, "create", fake_create)

    result = summarizer.summarize("Some input text to be summarized")
    assert result == "This is a fake summary"


# test that the custom SummarizationError exception is raised if it doesn't work.
def test_summarize_failure(monkeypatch):
    def fake_create(messages, model):
        raise Exception("simulated API failure")

    monkeypatch.setattr(summarizer.client.chat.completions, "create", fake_create)

    with pytest.raises(summarizer.SummarizationError):
        summarizer.summarize("Some input text to be summarized")
    