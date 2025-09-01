# Retrackt Quickstart Guide

This guide will help you get up and running with Retrackt, a tool to trace and report non-consensual images on Reddit.

## Prerequisites

- Python 3.10 or higher
- Git (for cloning the repository)

## 1. Install uv

uv is a fast Python package manager that we use for dependency management. Install it using one of these methods:

### macOS/Linux (recommended)
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

### Windows (PowerShell)
  ```powershell
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```

### Alternative: Install via pip
  ```bash
  pip install uv
  ```

### Verify installation
  ```bash
  uv --version
  ```

## 2. Clone and Setup the Project

### Clone the repository
  ```bash
  git clone <your-repo-url>
  cd retrackt
  ```

### Install dependencies
  ```bash
  uv sync
  ```

This will:
- Create a virtual environment in `.venv/`
- Install all required dependencies from `uv.lock`
- Set up the project for development

## 3. Configuration

### Environment Setup

1. **Copy the environment template:**
  ```bash
  cp .env.example .env
  ```

2. **Configure Reddit API credentials:**
   
   First, get your Reddit API credentials:
   - Go to [Reddit App Preferences](https://www.reddit.com/prefs/apps)
   - Click "Create App" or "Create Another App"
   - Choose "script" as the app type
   - Note your `client_id` and `client_secret`

3. **Edit your `.env` file:**
   Open the `.env` file and replace the placeholder values:

  ```bash
  REDDIT_CLIENT_ID=your_actual_client_id_here
  REDDIT_CLIENT_SECRET=your_actual_client_secret_here
  REDDIT_USER_AGENT=Retrackt by u/yourusername
  ```

⚠️ **Security Note**: The `.env` file contains sensitive credentials and should never be committed to version control. It's already included in `.gitignore` for your protection.

## 4. Running the Application

### Start the Streamlit app
  ```bash
  uv run streamlit run app.py
  ```

The app will be available at `http://localhost:8501`

### Alternative: Activate the environment manually
  ```bash
  source .venv/bin/activate  # On Windows: .venv\Scripts\activate
  streamlit run app.py
  ```

## 5. Using the Application

1. **Upload an image** or provide an Instagram image URL
2. **Enter your details** (Instagram username, full name)
3. **Specify a subreddit** to scan (default: BeautifulIndianWomen)
4. **Click "Find Matches"** to start the analysis

The app will:
- Download your reference image
- Scan the specified subreddit for image posts
- Use facial recognition to find potential matches
- Display results with similarity scores

## 6. Development Workflow

### Adding new dependencies
  ```bash
  uv add package-name
  ```

### Removing dependencies
  ```bash
  uv remove package-name
  ```

### Updating all dependencies
  ```bash
  uv sync --upgrade
  ```

### Running commands in the environment
  ```bash
  uv run python script.py
  uv run streamlit run app.py
  ```

## 7. Project Structure

  ```
  retrackt/
  ├── app.py              # Main Streamlit application
  ├── pyproject.toml      # Project configuration and dependencies
  ├── uv.lock            # Locked dependency versions
  ├── render.yaml        # Deployment configuration
  ├── .env.example       # Environment variables template
  ├── .env               # Your environment variables (create from .env.example)
  ├── .gitignore         # Git ignore file (includes .env)
  ├── docs/              # Documentation
  │   └── quickstart.md  # This guide
  └── .venv/             # Virtual environment (created by uv)
  ```

## 8. Deployment

The project is configured for deployment on Render.com:

1. Push your code to a Git repository
2. Connect your repository to Render
3. The `render.yaml` file will automatically configure the deployment
4. Render will use uv to install dependencies and run the app

## Troubleshooting

### uv command not found
- Make sure uv is properly installed and in your PATH
- Try restarting your terminal
- Use the pip installation method as an alternative

### Virtual environment issues
- Delete `.venv/` folder and run `uv sync` again
- Ensure you're in the project directory when running uv commands

### Dependency conflicts
- Try `uv sync --refresh` to rebuild the lock file
- Check that your Python version meets the requirements (3.10+)

### Reddit API errors
- Verify your API credentials in the `.env` file are correct
- Ensure you've copied `.env.example` to `.env` and filled in the values
- Ensure your Reddit app is configured as a "script" type
- Check rate limits if you're making many requests

## Need Help?

- Check the main [README.md](../README.md) for more detailed information
- Review the application code in `app.py` for implementation details
- Ensure all API credentials are properly configured

## Security Note

⚠️ **Important**: 
- Never commit your `.env` file to version control
- The `.env` file is automatically ignored by Git
- Always use the `.env.example` template for sharing configuration structure
- Keep your Reddit API credentials secure and never share them publicly
