# Health Protocol App

A Streamlit application for tracking and managing health protocols, including LLLT (Low-Level Light Therapy) and Mobility Training sessions.

## Features

- Track daily exercises and treatments
- Visual progress tracking with charts
- Export functionality (CSV and Calendar)
- Mobile-responsive design
- Local data persistence

## Setup

1. Clone the repository:
```bash
git clone https://github.com/fugisawa/health_app.git
cd health_app
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
streamlit run main_app.py
```

## Deployment

### Streamlit Cloud (Recommended)

1. Push your code to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub
4. Deploy your app by selecting your repository

### Local Data Storage

The app stores data locally in `~/.health_protocol/`. When deploying:
- For Streamlit Cloud: Data will be stored in the cloud instance
- For local deployment: Data will be stored in your home directory

## Usage

1. Select your session type (LLLT or Mobility)
2. Follow the protocol for your current session
3. Mark exercises as complete
4. Track your progress over time
5. Export your data as needed

## License

MIT License
