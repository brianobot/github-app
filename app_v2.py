import httpx

from icecream import ic
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    
    GITHUB_ACCESS_TOKEN: str
    

class GithubClient:
    def __init__(self, settings: Settings):
        self.settings  = settings
        
    def get_authenticated_headers(self) -> dict[str, str]:
        """
        Returns a dictionary containing authentication credentials for the current setting user
        """
        return {
            "Accept": "application/vnd.github+json",
            "Authorization": f"token {self.settings.GITHUB_ACCESS_TOKEN}",
        }
        
    def check_rate_limit(self) -> dict[str, str]:
        """
        Check the Rate Limit for the Current Authenticated Access Token
        """
        rate_limit_url = "https://api.github.com/rate_limit"
        rate_limit_response = httpx.get(rate_limit_url, headers=self.get_authenticated_headers())
        return rate_limit_response.json()
        
    def get_profile_url(self, profile_name: str) -> str:
        return f"https://github.com/{profile_name}"
        
    def get_commit_count(self, profile_name: str) -> int:
        response = httpx.get(
            f"https://api.github.com/search/commits?q=author:{profile_name}+author-date:2025-01-01", 
            headers=self.get_authenticated_headers())
        
        ic(response.json())
        return response.json().get("total_count", 0)
    
    
    
if __name__ == "__main__":
    github_client = GithubClient(Settings())
    
    # rate_limit = github_client.check_rate_limit()
    # ic(rate_limit)
    # 
    github_client.get_commit_count("brianobot")
    
    