from services.extractor import Extractor


def test_extract_all():
    extractor = Extractor()
    s = """
    Jean Dupont
    Master Informatique - Université X
    Email: jean.dupont@example.com
    Tel: 06 12 34 56 78
    """
    result = extractor.extract_all(s)

    assert result.email == "jean.dupont@example.com"
    assert result.phone == "06 12 34 56 78"
    assert "master" in result.degree.lower()
