from typing import Callable

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    # Multiplication settings
    multiply_by: int = Field(
        default=3, description="Default number to multiply by in questions"
    )
    num_questions: int = Field(default=3, description="Number of questions to generate")
    division_prob: float = Field(
        default=0.2, description="Probability of division questions"
    )

    # Flask settings
    debug: bool = Field(default=True, description="Run Flask in debug mode")
    host: str = Field(default="0.0.0.0", description="Host to run the application on")
    port: int = Field(default=5001, description="Port to run the application on")

    # Reward settings
    reward_gifs: list[Callable] = Field(
        default=[
            lambda: "https://cataas.com/cat/gif",
            # lambda: requests.get("https://random-d.uk/api/v1/random?type=gif").json()[
            #     "url"
            # ],
            # giphy key jbbnggkvU58AHYQUO02UiQNYjIzezPgv
        ],
        description="List of cute animal GIF URLs for rewards",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="LEARNY_",
    )


# Create a global instance of the settings
settings = Settings()
