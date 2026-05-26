import warnings

# Mutes the specific DeprecationWarning
warnings.filterwarnings("ignore", category=DeprecationWarning, message=".*_UnionGenericAlias.*")

import pytest
import requests
import sys
from project import user
from project import start
from project import get_content

# We need fake data that matches the shape your function expects
mock_table_data = [
    "1: 'https://aljazeera.com/africa' ]",
    "2: 'https://aljazeera.com/asia' ]"
]

def test_user(monkeypatch):
    """Scenario 1: The user types '1' immediately and it works."""
    
    # Arrange
    monkeypatch.setattr("builtins.input", lambda _:"1")
    
    # Act
    result = user(mock_table_data)
    
    # Assert
    assert result == "https://aljazeera.com/africa"

    # users type 2 inputs wrong and final input was right

    user_inputs = iter(["abc", "99", "2"])
    monkeypatch.setattr('builtins.input', lambda _: next(user_inputs))
    
    # Act
    result = user(mock_table_data)
    
    # Assert
    assert result == "https://aljazeera.com/asia"

    #users hit the limits by wrong inputs

    user_inputs = iter(["0", "text", "500"])
    monkeypatch.setattr('builtins.input', lambda _: next(user_inputs))
    
    # Act & Assert
    # We use pytest.raises to "catch" the sys.exit so it doesn't crash our test suite!
    with pytest.raises(SystemExit) as error_catcher:
        user(mock_table_data)
          # Verify the exit message was exactly "Bye"
    assert str(error_catcher.value) == "Bye"

def test_start():
    class Response:
        def __init__(self, sample):
            self.text = sample
        def success(self):
            pass
    def failed(*args, **kwargs):
        raise requests.RequestException("Simulated Network Error")
    
    def test_start_easy(monkeypatch):
        fake_html = """
        <li class="menu__item--aje"><a href="/middle-east">Middle East</a></li>
        <li> class = "menu__item--aje"><a href="/africa">Africa</a></li>
        """       
        # Tell monkeypatch to replace requests.get with our fake response
        monkeypatch.setattr("requests.get", lambda *args, **kwargs: Response(fake_html) )       
        # Act: Run the function with an empty starting list
        result = start([]) 
        # Assert: Verify the formatting and that the first item ("Home") was skipped by your slice
        assert len(result) == 2
        assert result[0] == [1, "Middle East: https://www.aljazeera.com/middle-east"]
        assert result[1] == [2, "Africa: https://www.aljazeera.com/africa"]

    def test_start_filters(monkeypatch):
        fake_html = """
        <li class="menu__item--aje"><a href="/skip-me">Skip Me</a></li>
        <li class="menu__item--aje"><a href="/video">Video</a></li>
        <li class="menu__item--aje"><a href="/sports">Sports</a></li>
        <li class="menu__item--aje"><a href="/sports">Sports</a></li>
    """
        monkeypatch.setattr("requests.get", lambda *args, **kwargs:Response(fake_html))
        existing_categories = ["Pre-existing: https://www.aljazeera.com/old", "Sports: https://www.aljazeera.com/sports"]
        result = start(existing_categories)
        simple_results = [item[1] for item in result]
        assert "Video: https://www.aljazeera.com/video" not in simple_results
        assert simple_results.count("Sports: https://www.aljazeera.com/sports") == 1

    def test_start_failure(monkeypatch):
        monkeypatch.setattr("requests.get", failed())
        result = start([])
        assert result == []

def test_get_content():
    class Content:
        def __init__(self, fake_html):
            self.text = fake_html
    def mock_failed_request(*args, **kwargs):
        raise requests.RequestException("Simulated Network Timeout")
        
    def test_get_content_happy(monkeypatch):
        fake_html = """
            <div class="wysiwyg wysiwyg--all-content">
                <p>This is paragraph one.</p>
                <p>This is paragraph two.</p>
        """
        monkeypatch.setattr("requests.get", lambda *args, **kwargs: Content(fake_html))  
        result = get_content(["https://fake-link.com"])
        assert len(result) == 1
        assert result[0] == "This is paragraph one. This is paragraph two."

    def test_get_content_missing_structure(monkeypatch):
        fake_html = """
            <div>
                <p>I am in the wrong container!</p>
            </div>
        """
        monkeypatch.setattr("requests.get", lambda *args, **kwargs:Content(fake_html))
        result = get_content(["https://fake-link.com"])
        assert result == []
    
    def test_get_content_empty_paragraphs(monkeypatch):

        fake_html = """
            <div class="wysiwyg wysiwyg--all-content">
                <p>Valid text.</p>
                <p></p>
                <p></p>
                <p>More valid text.</p>
            </div>
        """
        monkeypatch.setattr("requests.get", lambda *args, **kwargs:Content(fake_html))
        result = get_content(["https://fake-link.com"])
        assert result == "Valid text.More valid text."