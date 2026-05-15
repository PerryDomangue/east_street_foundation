# East Street Foundation - Flask Website

Professional, mobile-responsive Flask website for **East Street Foundation**, an estate planning support business focused on wills, trusts, and related planning documents.

## 1. Install Dependencies

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 2. Create `.env`

Copy `.env.example` to `.env` and fill in your real values:

```bash
copy .env.example .env
```

Required environment variables:

- `FLASK_SECRET_KEY`
- `MAIL_USERNAME`
- `MAIL_APP_PASSWORD`
- `MAIL_RECIPIENT`
- `MAIL_SERVER` (default `smtp.gmail.com`)
- `MAIL_PORT` (default `587`)

## 3. Run the Flask App

```bash
python app.py
```

Then open: `http://127.0.0.1:5000`

## 4. Image Placement

Place or replace your image assets in:

- `static/images/logo.png`
- `static/images/slide_show_1.png` (or `.jpg`, `.jpeg`, `.webp`)
- `static/images/slide_show_2.png` (or `.jpg`, `.jpeg`, `.webp`)
- `static/images/slide_show_3.png` (or `.jpg`, `.jpeg`, `.webp`)
- `static/images/slide_show_4.png` (or `.jpg`, `.jpeg`, `.webp`)
- `static/images/slide_show_5.png` (or `.jpg`, `.jpeg`, `.webp`)
- `static/images/about.jpg`

The slideshow auto-detects files named `slide_show_*.png/.jpg/.jpeg/.webp` and keeps graceful fallback behavior if images are missing.

## 5. Start Your Plan Form Behavior

The `/start-your-plan` form:

- Validates required fields server-side (`first_name`, `last_name`, `email`, `phone`, consent)
- Rejects likely spam if hidden honeypot field `website` is filled
- Sends owner notification email via SMTP
- Sends customer confirmation email
- Uses safe flash messages and does not expose raw SMTP errors

## 6. Change Service Prices

Update placeholder pricing values in:

- `templates/index.html` (pricing preview)
- `templates/pricing.html` (full package cards)

Search for `Starting at $___` and replace with your real numbers.

## 7. Security Notes

- Never commit `.env` to GitHub.
- Keep your Gmail app password secret.
- In production, set a strong `FLASK_SECRET_KEY`.
- Consider using a production WSGI server (for example `gunicorn`) and HTTPS.
