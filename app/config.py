from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # OpenAI key kept but optional - not used anymore
    OPENAI_API_KEY: str = ""
    # Groq is our free LLM provider
    GROQ_API_KEY: str
    TAVILY_API_KEY: str
    MONGODB_URI: str
    DATABASE_NAME: str = "travel_agent"

    class Config:
        env_file = ".env"

settings = Settings()