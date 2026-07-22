# FaceApart

**FaceApart** is an automated apartment-hunting bot designed specifically for the Israeli real estate market on Facebook. By leveraging Playwright for dynamic browser automation and BeautifulSoup for parsing, it scans listings and displays them on a local web dashboard.

## Features

* **Browser Automation**: Uses Playwright to navigate Facebook listings seamlessly.
* **Hebrew Text Normalization**: Cleans and processes right-to-left text data using Python's `unicodedata`.
* **Multi-threaded Architecture**: Runs the browser scraping engine and the Flask server concurrently.
* **Local Web Dashboard**: Displays parsed apartment results instantly through a lightweight web interface.

## Repository Structure

* `app.py`: Main application code handling automation, parsing, multi-threading, and the Flask server.
* `terminal_working.png`: Visual guide showing the console logger running.
* `webpage.png`: Visual interface preview of the local application dashboard.
* `LICENSE`: MIT License guidelines.

## Prerequisites

Before setting up, ensure you have **Python 3.8+** installed on your machine.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com
   cd FaceApart
   ```

2. **Install required Python packages**:
   ```bash
   pip install flask beautifulsoup4 playwright
   ```

3. **Install Playwright browser binaries**:
   ```bash
   playwright install chromium
   ```

## Usage

Run the main application script to initialize both the scraper and the web interface:
```bash
python app.py
```

Once running, open your web browser and navigate to the address provided by Flask (typically `http://127.0.0.1:5000`) to view real-time apartment listings.

## License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.
