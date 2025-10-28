# 🚀 AIShortsDownloader

<div align="center">

[![GitHub stars](https://img.shields.io/github/stars/yusufnightin/AIShortsDownloader?style=for-the-badge)](https://github.com/yusufnightin/AIShortsDownloader/stargazers)

[![GitHub forks](https://img.shields.io/github/forks/yusufnightin/AIShortsDownloader?style=for-the-badge)](https://github.com/yusufnightin/AIShortsDownloader/network)

[![GitHub issues](https://img.shields.io/github/issues/yusufnightin/AIShortsDownloader?style=for-the-badge)](https://github.com/yusufnightin/AIShortsDownloader/issues)

[![Python](https://img.shields.io/badge/python-3.x-blue?style=for-the-badge&logo=python)](https://www.python.org/)

**Automate YouTube Shorts discovery, intelligent selection, and high-quality downloading from specified channels.**

</div>

## 📖 Overview

The `AIShortsDownloader` is a robust Python-based system designed to automate the process of finding, selecting, and downloading short videos from designated YouTube channels. It's built for content creators, marketers, or anyone needing to collect relevant short-form video content based on defined criteria (keywords, channel IDs) for analysis, curation, or creative projects. The system manages downloaded content, logs operations, generates reports, and provides backup functionalities, ensuring an efficient and organized workflow.

## ✨ Features

-   🎯 **YouTube Channel Monitoring**: Automatically fetches video data from a configurable list of YouTube channels.
-   💡 **Intelligent Short Video Selection**: Filters and selects shorts based on user-defined keywords and criteria, ensuring relevance.
-   ⬇️ **High-Quality Video Downloading**: Leverages `yt-dlp` to download selected YouTube Shorts in the best available quality.
-   🗄️ **Local Database Management**: Uses SQLite to track downloaded shorts, preventing duplicates and managing metadata.
-   ⚙️ **Highly Configurable Settings**: All operational parameters, including API keys, channels, keywords, and paths, are easily managed via `settings.json`.
-   📊 **Automated Logging & Reporting**: Records all operations and activities, and generates reports for oversight and analysis.
-   💾 **Built-in Backup Mechanism**: Automatically backs up critical data at configurable intervals.

## 🛠️ Tech Stack

**Runtime:**

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

**Libraries:**

[![yt-dlp](https://img.shields.io/badge/yt--dlp-latest-green?style=for-the-badge)](https://github.com/yt-dlp/yt-dlp)

[![Google API Python Client](https://img.shields.io/badge/Google_API_Client-Python-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://github.com/googleapis/google-api-python-client)

**Database:**

[![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/index.html)

**Configuration:**

[![JSON](https://img.shields.io/badge/JSON-000000?style=for-the-badge&logo=json&logoColor=white)](https://www.json.org/json-en.html)

## 🚀 Quick Start

### Prerequisites
-   **Python 3.x**: Ensure Python 3.x is installed on your system.
    ```bash
    python --version
    ```
-   **YouTube Data API Key**: Obtain a YouTube Data API v3 key from the Google Cloud Console.

### Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/yusufnightin/AIShortsDownloader.git
    cd AIShortsDownloader
    ```

2.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configuration setup**
    *   Open `settings.json` in the root directory.
    *   Replace `"YOUR_YOUTUBE_API_KEY"` with your actual Google YouTube Data API Key.
    *   Update `channel_ids` with the YouTube channel IDs you wish to monitor.
    *   Modify `keywords` to include relevant terms for selecting shorts.
    *   Adjust `download_path`, `log_level`, `max_shorts_per_channel`, and `backup_interval_days` as needed.

    Example `settings.json`:
    ```json
    {
      "youtube_api_key": "YOUR_YOUTUBE_API_KEY",
      "channel_ids": [
        "UC_x5XG1OV2P6uZZ5FSM9Ttw",
        "UC-9-kyTW8ZkZNDHQJ6FgpwQ"
      ],
      "keywords": [
        "tutorial",
        "coding",
        "funny moments",
        "tech review"
      ],
      "download_path": "downloaded_shorts",
      "log_level": "INFO",
      "max_shorts_per_channel": 5,
      "backup_interval_days": 3
    }
    ```

4.  **Run the downloader**
    ```bash
    python main.py
    ```
    The script will start monitoring channels, selecting, and downloading shorts based on your configuration.

## 📁 Project Structure

```
AIShortsDownloader/
├── main.py             # Main application logic and entry point
├── requirements.txt    # Python dependency list
├── settings.json       # Configuration file for API keys, channels, keywords, etc.
├── shorts_manager.db   # SQLite database for tracking downloaded shorts
├── backups/            # Directory for database backups
├── logs/               # Directory for application log files
├── reports/            # Directory for generated operational reports
└── README.md           # Project documentation
```

## ⚙️ Configuration

The `settings.json` file is central to customizing the behavior of `AIShortsDownloader`.

| Variable                   | Description                                                 | Example Value      | Required |

|----------------------------|-------------------------------------------------------------|--------------------|----------|

| `youtube_api_key`          | Your Google YouTube Data API v3 key.                        | `AIzaSyD...`       | Yes      |

| `channel_ids`              | List of YouTube channel IDs to monitor for shorts.          | `["UC_x...", "UC-..."]` | Yes      |

| `keywords`                 | List of keywords used to filter and select relevant shorts. | `["tech", "review"]` | Yes      |

| `download_path`            | Directory where downloaded shorts will be saved.            | `"downloaded_shorts"` | Yes      |

| `log_level`                | Minimum level for logging messages (e.g., `DEBUG`, `INFO`, `WARNING`, `ERROR`). | `"INFO"`           | No       |

| `max_shorts_per_channel`   | Maximum number of shorts to download per channel in each run. | `5`                | No       |

| `backup_interval_days`     | How often (in days) the SQLite database should be backed up. | `7`                | No       |

## 🤝 Contributing

We welcome contributions! If you have suggestions for improvements, new features, or bug fixes, please open an issue or submit a pull request.

### Development Setup
1.  Fork the repository.
2.  Clone your forked repository: `git clone https://github.com/YOUR_USERNAME/AIShortsDownloader.git`
3.  Create a virtual environment: `python -m venv venv`
4.  Activate the environment:
    *   Windows: `.\venv\Scripts\activate`
    *   macOS/Linux: `source venv/bin/activate`
5.  Install dependencies: `pip install -r requirements.txt`
6.  Make your changes and ensure they are tested.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. <!-- TODO: Add LICENSE file -->

## 🙏 Acknowledgments

-   [yt-dlp](https://github.com/yt-dlp/yt-dlp) for robust video downloading capabilities.
-   [Google API Python Client](https://github.com/googleapis/google-api-python-client) for seamless interaction with the YouTube Data API.

## 📞 Support & Contact

-   🐛 Issues: [GitHub Issues](https://github.com/yusufnightin/AIShortsDownloader/issues)

---

<div align="center">

**⭐ Star this repo if you find it helpful!**

Made with ❤️ by [yusufnightin](https://github.com/yusufnightin)

</div>

