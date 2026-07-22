# FaceApart

**FaceApart** is a automated Python tool designed to simplify hunting for apartments on Facebook in Israel. The bot monitors groups or marketplace postings to help users quickly find relevant listings without manual scrolling.

## Features

* **Automated Scanning**: Tracks real-time rental listings across specified Facebook sources.
* **Smart Filtering**: Filters results based on custom keywords tailored for the Israeli housing market.
* **Lightweight Interface**: Includes a local web UI view alongside terminal logging capabilities.

## Repository Structure

* `app.py`: The primary Python application script containing the bot logic.
* `terminal_working.png`: Demonstration screenshot of the terminal interface execution.
* `webpage.png`: Visual preview of the application's web interface dashboard.
* `LICENSE`: MIT License guidelines for open-source distribution.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com
   cd FaceApart
   ```

2. **Install dependencies**:
   Ensure you have Python 3 installed, then set up the required packages:
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: Add your specific dependencies like Selenium, Beautiful Soup, Flask, or Playwright to a requirements.txt file).*

## Usage

Launch the main script to run the bot and initialize its tracking engine:
```bash
python app.py
```

## License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.
