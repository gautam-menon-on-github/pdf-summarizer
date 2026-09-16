from src import pdf_reader

def test_extract_text():

    # using the research paper "Attention Is All You Need" from Google
    with open("tests/fixtures/attention_is_all_you_need.pdf", "rb") as f:
        doc_text = pdf_reader.extract_text(f.read())

    assert "Attention" in doc_text