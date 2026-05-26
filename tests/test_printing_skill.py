import pytest

from aimesh.skills.printing import parse_sticker_quote, quote_stickers


def test_quote_stickers_prices_laminated_vinyl_job():
    quote = quote_stickers(
        quantity=100,
        width_mm=50,
        height_mm=30,
        material="vinyl",
        laminated=True,
    )

    assert quote.skill_name == "quote_stickers"
    assert quote.total_eur == pytest.approx(42.0)
    assert quote.currency == "EUR"
    assert quote.inputs["material"] == "vinyl"
    assert "lamination" in quote.reason.lower()


def test_parse_sticker_quote_extracts_required_fields():
    request = parse_sticker_quote(
        "Quote 100 stickers, 50mm x 30mm, vinyl, laminated"
    )

    assert request.quantity == 100
    assert request.width_mm == 50
    assert request.height_mm == 30
    assert request.material == "vinyl"
    assert request.laminated is True


def test_parse_sticker_quote_rejects_missing_size():
    with pytest.raises(ValueError, match="size"):
        parse_sticker_quote("Quote 100 vinyl stickers")
