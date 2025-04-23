# Learny

A simple web application for practicing multiplication tables.

## Configuration

Learny now uses Pydantic Settings for configuration. You can customize the application in several ways:

1. **Environment Variables**: Set variables with the `LEARNY_` prefix
   - Example: `LEARNY_MULTIPLY_BY=5 LEARNY_NUM_QUESTIONS=10 flask run`

2. **Configuration File**: Create a `.env` file in the project root
   - Copy the `.env.example` file to `.env` and customize it
   - The `.env` file should not be committed to version control

### Available Settings

| Setting | Description | Default |
|---------|-------------|---------|
| `LEARNY_MULTIPLY_BY` | Number to multiply by in questions | 3 |
| `LEARNY_NUM_QUESTIONS` | Number of questions to generate | 3 |
| `LEARNY_DEBUG` | Run Flask in debug mode | `true` |
| `LEARNY_HOST` | Host to run the app on | `0.0.0.0` |
| `LEARNY_PORT` | Port to run the app on | 5001 |
| `LEARNY_REWARD_GIFS` | List of GIF URLs for rewards | [`https://cataas.com/cat/gif`] |

## Installation

```bash
# Using uv
uv pip install -e .
```

## Running the Application

```bash
python app.py
```

Visit http://localhost:5001 in your browser to use the application.