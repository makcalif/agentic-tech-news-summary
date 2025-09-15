import requests
from autogen.tools import Tool
import autogen

class WebBrowser:
    """
    A web browser class that fetches and processes web page content for LLM analysis.
    """
    
    def __init__(self, max_content_length: int = 30000, timeout: int = 15):
        """
        Initialize the WebBrowser.
        
        Args:
            max_content_length: Maximum length of content to return (default 30000)
            timeout: Request timeout in seconds (default 15)
        """
        self.max_content_length = max_content_length
        self.timeout = timeout
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
    
    def fetch_url(self, url: str) -> str:
        """
        Fetches and processes web page content.
        
        Args:
            url: The URL of the web page to fetch
            
        Returns:
            str: Processed content from the web page
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            
            # Process the content
            content = self._process_content(response.text)
            
            return f"Content from {url}:\n\n{content}"
            
        except requests.RequestException as e:
            return f"Error fetching {url}: {str(e)}"
        except Exception as e:
            return f"Error processing web page {url}: {str(e)}"
    
    def _process_content(self, html_content: str) -> str:
        """
        Process HTML content by removing scripts, styles, and HTML tags.
        
        Args:
            html_content: Raw HTML content
            
        Returns:
            str: Cleaned text content
        """
        # Remove script and style tags and their content
        content = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
        content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL | re.IGNORECASE)
        
        # Remove HTML tags but keep the text
        content = re.sub(r'<[^>]+>', ' ', content)
        
        # Clean up whitespace
        content = re.sub(r'\s+', ' ', content).strip()
        
        # Limit content length
        if len(content) > self.max_content_length:
            content = content[:self.max_content_length] + "... [Content truncated]"
        
        return content
    
    def get_raw_html(self, url: str) -> str:
        """
        Fetches raw HTML content without processing.
        
        Args:
            url: The URL of the web page to fetch
            
        Returns:
            str: Raw HTML content
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            
            html_content = response.text
            
            # Limit content length
            if len(html_content) > self.max_content_length:
                html_content = html_content[:self.max_content_length] + "\n... [Content truncated due to length]"
            
            return f"Raw HTML from {url}:\n\n{html_content}"
            
        except requests.RequestException as e:
            return f"Error fetching {url}: {str(e)}"
        except Exception as e:
            return f"Error processing web page {url}: {str(e)}"