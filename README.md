# Retrackt

A Streamlit web application that helps you find if your photographs have been reposted on Reddit without your consent using facial recognition technology.

## What it does

Retrackt allows users to:
- Upload an image or provide an Instagram image URL
- Scan a specified Reddit subreddit for similar images
- Use DeepFace facial recognition to identify potential matches
- Display the top 3 most similar images found with similarity scores

The app is particularly useful for identifying non-consensual image sharing and helping users track unauthorized use of their photos.

## Demo

[Watch the demo](demo.mp4)

## Features

- **Image Upload**: Support for JPG, JPEG, and PNG files
- **URL Input**: Direct image URL support (Instagram URLs preferred)
- **Reddit Integration**: Scans Reddit subreddits for image posts
- **Facial Recognition**: Uses DeepFace library for accurate face matching
- **Real-time Progress**: Shows processing status as images are analyzed
- **Similarity Scoring**: Ranks matches by similarity distance

## Requirements

- Python 3.10 or higher
- uv (recommended) or pip for package management
- Reddit API credentials (free from Reddit)
- Required packages listed in `pyproject.toml`

## Installation

  ```bash
  # Clone the repository
  git clone <your-repo-url>
  cd retrackt

  # Install dependencies using uv (recommended)
  uv sync
  
  # Or using pip
  pip install -r requirements.txt
  ```

## Configuration

### Environment Setup

1. **Copy the environment template:**
  ```bash
  cp .env.example .env
  ```

2. **Configure Reddit API credentials:**
   - Go to [Reddit App Preferences](https://www.reddit.com/prefs/apps)
   - Click "Create App" or "Create Another App"
   - Choose "script" as the app type
   - Copy your `client_id` and `client_secret`
   - Edit `.env` file with your credentials:

  ```bash
  REDDIT_CLIENT_ID=your_actual_client_id_here
  REDDIT_CLIENT_SECRET=your_actual_client_secret_here
  REDDIT_USER_AGENT=Retrackt by u/yourusername
  ```

⚠️ **Important**: Never commit your `.env` file to version control. The `.env` file is already included in `.gitignore`.

## Running the Application

### Local Development

  ```bash
  # Using uv (recommended)
  uv run streamlit run app.py
  
  # Or activate the virtual environment first
  source .venv/bin/activate  # On Windows: .venv\Scripts\activate
  streamlit run app.py
  ```

The app will be available at `http://localhost:8501`

### Streamlit Cloud Deployment

This app is configured for easy deployment on Streamlit Cloud:

1. Ensure your GitHub repository includes `requirements.txt` (created for dependency management).
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click "New app" and select your repository and branch (main or master).
4. Set the main file path to `app.py`.
5. In the app configuration, add the following secrets by going to app settings > Secrets (get these from https://www.reddit.com/prefs/apps):
   - `REDDIT_CLIENT_ID`: Your Reddit app client ID
   - `REDDIT_CLIENT_SECRET`: Your Reddit app client secret
   - `REDDIT_USER_AGENT`: Your Reddit app user agent (e.g., "Retrackt by u/yourusername")
6. Click "Deploy"!

The app will be accessible at a public URL provided by Streamlit Cloud. Deployment may take time due to heavy dependencies like TensorFlow.

For deployment on other platforms (e.g., Render), keep the included `render.yaml`.

## Usage

1. **Enter Image**: Either upload an image file or provide an Instagram image URL
2. **Add Details**: Enter your Instagram username and full name (optional)
3. **Select Subreddit**: Choose which subreddit to scan (defaults to "BeautifulIndianWomen")
4. **Find Matches**: Click the "Find Matches" button to start scanning
5. **Review Results**: View any matches found with similarity scores

## Technical Details

- **Frontend**: Streamlit web interface
- **Image Processing**: OpenCV and DeepFace for facial recognition
- **Reddit API**: PRAW library for Reddit data access
- **Image Downloading**: Requests library for fetching images
- **Temporary Storage**: Uses temporary files for image processing

## Important Notes

- Processing time depends on the number of images in the target subreddit
- The app processes up to 1000 recent posts from the specified subreddit
- Only direct image links (jpg, jpeg, png) are processed
- Temporary files are automatically cleaned up after processing

## Privacy & Ethics

This tool is designed to help users identify unauthorized use of their images. Please use responsibly and respect others' privacy rights.
