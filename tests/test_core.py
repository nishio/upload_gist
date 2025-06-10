import pytest
from unittest.mock import patch, Mock
from gist_uploader._core import upload_to_gist


@patch.dict('os.environ', {}, clear=True)
def test_token_missing():
    """Test that RuntimeError is raised when no token is provided."""
    with pytest.raises(RuntimeError, match="GitHub token not provided"):
        upload_to_gist("test content", filename="test.txt", token=None)


@patch.dict('os.environ', {}, clear=True)
def test_token_missing_no_env():
    """Test that RuntimeError is raised when no token in environment."""
    with pytest.raises(RuntimeError, match="GitHub token not provided"):
        upload_to_gist("test content", filename="test.txt")


@patch('gist_uploader._core.requests.post')
def test_create_gist_success(mock_post):
    """Test successful gist creation."""
    mock_response = Mock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"html_url": "https://gist.github.com/test"}
    mock_post.return_value = mock_response
    
    result = upload_to_gist(
        "test content", 
        filename="test.txt", 
        token="test_token"
    )
    
    assert result["html_url"] == "https://gist.github.com/test"
    mock_post.assert_called_once()


@patch('gist_uploader._core.requests.patch')
def test_update_gist_success(mock_patch):
    """Test successful gist update."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"html_url": "https://gist.github.com/test"}
    mock_patch.return_value = mock_response
    
    result = upload_to_gist(
        "updated content", 
        filename="test.txt", 
        token="test_token",
        gist_id="test_gist_id"
    )
    
    assert result["html_url"] == "https://gist.github.com/test"
    mock_patch.assert_called_once()


@patch('gist_uploader._core.requests.post')
def test_api_error(mock_post):
    """Test API error handling."""
    mock_response = Mock()
    mock_response.status_code = 401
    mock_response.text = "Unauthorized"
    mock_post.return_value = mock_response
    
    with pytest.raises(RuntimeError, match="GitHub API error 401: Unauthorized"):
        upload_to_gist("test content", filename="test.txt", token="bad_token")
