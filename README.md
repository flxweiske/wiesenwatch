# 🌿 Wiesenwatch

> Do your outside greens need watering today? Wiesenwatch checks the rain forecast for today and tomorrow and sends you a daily gmail so you never have to guess.

Wiesenwatch fetches rain predictions from the [Open-Meteo API](https://open-meteo.com/) for your location and compares them against a configurable threshold. If it looks dry, you get a red alert to water. If rain is on the way, you get the all-clear to relax.

---

## How It Works

1. Fetches today's and tomorrow's predicted rain sum from Open-Meteo for your configured coordinates
2. Compares each value against your `RAIN_SUM_THRESHOLD`
3. Renders an HTML email from `mail_template.html` with colour-coded indicators
4. Sends the email to yourself via Gmail SMTP

---

## Prerequisites

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) for dependency management
- A Gmail account with an [App Password](https://myaccount.google.com/apppasswords) (required — Google blocks regular passwords for SMTP)
- Docker (optional, for containerised runs)

---

## Configuration

Copy `.env.template` to `.env` and fill in your values:

```env
MAIL=your-gmail@gmail.com
KEY=your-gmail-app-password
LATITUDE=your-latitude
LONGITUDE=your-longitude
RAIN_SUM_THRESHOLD=0.3
```

| Variable | Description |
|---|---|
| `MAIL` | Your Gmail address — used as both sender and recipient |
| `KEY` | Your Gmail [App Password](https://myaccount.google.com/apppasswords) — **not** your account password |
| `LATITUDE` | Latitude of your location |
| `LONGITUDE` | Longitude of your location |
| `RAIN_SUM_THRESHOLD` | Rain sum in mm below which watering is recommended (default: `0.3`) |

> **Note:** Do not use quotes around values in the `.env` file. Docker's env-file parser passes them literally, which will cause authentication errors.

---

## Running Locally

```bash
# Install dependencies
uv sync

# Run the script
uv run python main.py
```

---

## Running with Docker

**Build the image:**
```bash
docker build -t wiesenwatch .
```

**Run with your `.env` file:**
```bash
docker run --env-file .env wiesenwatch
```

---

## Automated Daily Runs with GitHub Actions

The recommended way to run Wiesenwatch on a schedule — free, no infrastructure required.

Create `.github/workflows/wiesenwatch.yml`:

```yaml
name: Wiesenwatch

on:
  schedule:
    - cron: '0 5 * * *'
  workflow_dispatch:

jobs:
  run:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build and run container
        run: |
          docker build -t wiesenwatch .
          docker run \
            -e MAIL=${{ secrets.MAIL }} \
            -e KEY=${{ secrets.KEY }} \
            -e LATITUDE=${{ secrets.LATITUDE }} \
            -e LONGITUDE=${{ secrets.LONGITUDE }} \
            -e RAIN_SUM_THRESHOLD=${{ vars.RAIN_SUM_THRESHOLD }} \
            wiesenwatch
```

Add `MAIL`, `KEY`, `LATITUDE` and `LONGITUDE` as **Secrets** in your repository settings, and `RAIN_SUM_THRESHOLD` as **Variables**.

---

## Gmail Setup

Wiesenwatch uses Gmail SMTP to send emails. Google requires an App Password rather than your account password for SMTP access:

1. Enable 2-Step Verification on your Google account
2. Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
3. Generate a new App Password
4. Use the generated password as your `KEY` value — no quotes

---

## License

MIT