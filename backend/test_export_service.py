import unittest
from unittest.mock import patch, MagicMock
from backend.export_service import export_articles
from uuid import uuid4
from datetime import datetime

class TestExportService(unittest.TestCase):

    @patch('backend.export_service.Session')
    @patch('backend.export_service.os.path.exists')
    @patch('backend.export_service.os.makedirs')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_export_by_date(self, mock_open, mock_makedirs, mock_exists, mock_session_class):
        mock_exists.return_value = False
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        
        # Mocking Article
        article = MagicMock()
        article.id = uuid4()
        article.title = "Test Article"
        article.source_url = "http://example.com"
        article.published_at = datetime(2026, 5, 5, 12, 0)
        article.link = "http://example.com/article"
        article.full_text = "Full text content"
        
        mock_session.exec.return_value.all.return_value = [article]
        
        export_articles("test_export", export_date_str="2026-05-05")
        
        mock_makedirs.assert_called_with("test_export")
        mock_session.exec.assert_called()
        mock_open.assert_called()
        
    @patch('backend.export_service.Session')
    @patch('backend.export_service.os.path.exists')
    @patch('backend.export_service.os.makedirs')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_export_by_uuid(self, mock_open, mock_makedirs, mock_exists, mock_session_class):
        mock_exists.return_value = True
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        
        article_id = uuid4()
        article = MagicMock()
        article.id = article_id
        article.title = "Test Article UUID"
        article.source_url = "http://example.com"
        article.published_at = datetime(2026, 5, 5, 12, 0)
        article.link = "http://example.com/article"
        article.full_text = "Full text content"
        
        mock_session.exec.return_value.all.return_value = [article]
        
        export_articles("test_export", article_ids=[str(article_id)])
        
        mock_session.exec.assert_called()
        mock_open.assert_called()

if __name__ == '__main__':
    unittest.main()
