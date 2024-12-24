import pytest
import os
from app.game.word_generator import WordGenerator

@pytest.mark.usefixtures("requires_openai")
def test_word_generator_initialization():
    generator = WordGenerator()
    assert generator is not None

@pytest.mark.usefixtures("requires_openai")
def test_generate_spangram():
    generator = WordGenerator()
    spangram = generator.generate_spangram("animals")
    assert isinstance(spangram, str)
    assert len(spangram) > 0

@pytest.mark.usefixtures("requires_openai")
def test_generate_theme_words():
    generator = WordGenerator()
    spangram = "DOLPHINS"
    words = generator.generate_theme_words(spangram, "animals")
    assert isinstance(words, list)
    assert len(words) > 0
    for word in words:
        assert isinstance(word, str)
        assert len(word) > 0 