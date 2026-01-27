# RIB Data Scraper

A Python-based automation tool designed to extract performance data from rib.gg match series. The script automates the collection of player statistics, including advanced metrics like multi-kills and clutches, and aggregates them into a structured CSV file.

> [!WARNING]
> This was built for the rib.gg website as of 2026-1-27. If it doesn't work then rib.gg most likely updated it.

## Features

- **Automated Data Extraction**: Pulls statistics from both the main scoreboard and the specialized multi-kill tables.
- **Data Aggregation**: Automatically combines stats for players across multiple matches entered in a single session.
- **Calculated Averages**: Computes average Rating, ACS, KAST, ADR, and Headshot percentage.
- **Persistent Session**: Uses a persistent browser context to maintain local data and improve scraping reliability.

## System Requirements

- **Windows OS**: The included setup scripts are designed for Windows environment (.bat).
- **Python 3.10+**: (Handled by the setup script if missing).
- **VS Code**: Recommended for script execution and data review.

## Installation

1. **Download**: Save the project files to a local directory.
2. **Run Setup**: Double-click `setup_scraper.bat`.
   - This script verifies your Python installation.
   - Installs the Playwright library and necessary dependencies.
   - Downloads the required Chromium browser engine.
   - *Note: If Python is installed for the first time by this script, restart the .bat file once the Python installer finishes.*

## Usage Instructions

1. **Start the Program**: Run `run_scraper.bat`.
2. **Input Match IDs**: When prompted in the terminal, enter the Match ID found at the end of the rib.gg URL.
   - Example: For `https://www.rib.gg/series/12345`, the ID is `12345`.
3. **Session Processing**: You can input multiple Match IDs sequentially. The script will navigate to each page, extract data, and update the internal player totals.
4. **Finalize and Save**: Type `exit` to stop scraping. The script will then calculate final averages and write all data to `valorant_stats.csv`.
5. **Data Access**: Open `valorant_stats.csv` using Excel, Google Sheets, or a text editor to view the results.

## Technical Overview

The application utilizes the Playwright framework to simulate a real user environment:

- **Browser Logic**: The script launches a Chromium instance in a non-headless mode, allowing users to see the navigation process.
- **Data Selection**: It uses CSS selectors and locator logic to identify specific table rows (`.MuiTableRow-root`) and cells containing player names and performance numbers.
- **Data Cleaning**: The script includes internal functions to strip percentage signs and handle null/empty values (represented as dashes on the website) to ensure mathematical accuracy.
- **Aggregation Logic**: Statistics are stored in a dictionary where the player's name is the unique key. If a player appears in multiple matches, their totals are updated and then divided by the total match count at the end of the session.

## File Structure

- `ribscraper.py`: The core Python logic.
- `setup_scraper.bat`: Environment and dependency installer.
- `run_scraper.bat`: Execution shortcut for the scraper.
- `valorant_stats.csv`: The generated output file (created after the first run).
- `browser_session/`: Local directory created to store browser state and cookies (created after the first run).

## Limitations

- **Network Dependency**: The script requires a stable internet connection to load the heavy JavaScript elements on the target website.
- **Selector Stability**: If rib.gg updates their website layout or CSS class names, the scraper selectors may require adjustment.

Last updated 2026-1-27
