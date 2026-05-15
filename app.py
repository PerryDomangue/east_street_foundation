import os
import re
import smtplib
from datetime import datetime
from email.message import EmailMessage
from glob import glob

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "change-this-secret-key")
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME", "").strip()
app.config["MAIL_APP_PASSWORD"] = os.getenv("MAIL_APP_PASSWORD", "").strip()
app.config["MAIL_RECIPIENT"] = os.getenv("MAIL_RECIPIENT", "").strip()
app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER", "smtp.gmail.com").strip()

try:
    app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT", "587"))
except ValueError:
    app.config["MAIL_PORT"] = 587

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@app.context_processor
def inject_globals():
    full_company_path = os.path.join(app.root_path, "static", "images", "full_company.png")
    full_company_info_path = os.path.join(
        app.root_path, "static", "images", "full_company_info.png"
    )

    if os.path.exists(full_company_path):
        footer_brand_image = "images/full_company.png"
    elif os.path.exists(full_company_info_path):
        footer_brand_image = "images/full_company_info.png"
    else:
        footer_brand_image = "images/logo.png"

    return {
        "current_year": datetime.now().year,
        "contact_email": app.config["MAIL_RECIPIENT"] or "contact@eaststreetfoundation.com",
        "footer_brand_image": footer_brand_image,
    }


def is_valid_email(email: str) -> bool:
    return bool(EMAIL_REGEX.match(email or ""))


def get_slideshow_images() -> list[str]:
    images_dir = os.path.join(app.root_path, "static", "images")
    patterns = [
        os.path.join(images_dir, "slide_show_*.png"),
        os.path.join(images_dir, "slide_show_*.jpg"),
        os.path.join(images_dir, "slide_show_*.jpeg"),
        os.path.join(images_dir, "slide_show_*.webp"),
    ]

    paths = []
    for pattern in patterns:
        paths.extend(glob(pattern))

    def image_sort_key(path: str):
        name = os.path.basename(path).lower()
        match = re.search(r"slide_show_(\d+)", name)
        return int(match.group(1)) if match else 9999

    filenames = [os.path.basename(path) for path in sorted(paths, key=image_sort_key)]
    if filenames:
        return filenames

    return [
        "slide_show_1.jpg",
        "slide_show_2.jpg",
        "slide_show_3.jpg",
        "slide_show_4.jpg",
        "slide_show_5.jpg",
    ]


def build_form_data(form) -> dict:
    return {
        "first_name": form.get("first_name", "").strip(),
        "last_name": form.get("last_name", "").strip(),
        "email": form.get("email", "").strip(),
        "phone": form.get("phone", "").strip(),
        "city": form.get("city", "").strip(),
        "state": form.get("state", "").strip(),
        "service": form.get("service", "Not Sure Yet").strip() or "Not Sure Yet",
        "preferred_contact": form.get("preferred_contact", "Email").strip() or "Email",
        "message": form.get("message", "").strip(),
        "consent": bool(form.get("consent")),
        "website": form.get("website", "").strip(),
    }


def send_inquiry_emails(form_data: dict) -> None:
    mail_username = app.config["MAIL_USERNAME"]
    mail_password = app.config["MAIL_APP_PASSWORD"]
    mail_recipient = app.config["MAIL_RECIPIENT"]
    mail_server = app.config["MAIL_SERVER"]
    mail_port = app.config["MAIL_PORT"]

    if not all([mail_username, mail_password, mail_recipient, mail_server, mail_port]):
        raise RuntimeError("Email configuration is incomplete.")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    owner_subject = (
        "New East Street Foundation Inquiry from "
        f"{form_data['first_name']} {form_data['last_name']}"
    )
    owner_body = f"""
New East Street Foundation inquiry

First name: {form_data['first_name']}
Last name: {form_data['last_name']}
Email: {form_data['email']}
Phone: {form_data['phone']}
City: {form_data['city']}
State: {form_data['state']}
Service interested in: {form_data['service']}
Preferred contact method: {form_data['preferred_contact']}
Message: {form_data['message'] or '(No message provided)'}
Timestamp: {timestamp}
""".strip()

    owner_message = EmailMessage()
    owner_message["Subject"] = owner_subject
    owner_message["From"] = mail_username
    owner_message["To"] = mail_recipient
    owner_message["Reply-To"] = form_data["email"]
    owner_message.set_content(owner_body)

    customer_message = EmailMessage()
    customer_message["Subject"] = "East Street Foundation Received Your Inquiry"
    customer_message["From"] = mail_username
    customer_message["To"] = form_data["email"]
    customer_message.set_content(
        "Thank you for contacting East Street Foundation. "
        "We received your inquiry and will contact you soon."
    )

    with smtplib.SMTP(mail_server, mail_port, timeout=30) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(mail_username, mail_password)
        smtp.send_message(owner_message)
        if form_data["email"]:
            smtp.send_message(customer_message)


@app.route("/")
def home():
    return render_template("index.html", slideshow_images=get_slideshow_images())


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/services")
def services():
    return render_template("services.html")


@app.route("/pricing")
def pricing():
    return render_template("pricing.html")


@app.route("/start-your-plan", methods=["GET", "POST"])
def start_plan():
    empty_form = {
        "first_name": "",
        "last_name": "",
        "email": "",
        "phone": "",
        "city": "",
        "state": "",
        "service": "Not Sure Yet",
        "preferred_contact": "Email",
        "message": "",
        "consent": False,
        "website": "",
    }

    if request.method == "POST":
        form_data = build_form_data(request.form)

        if form_data["website"]:
            flash(
                "Something went wrong while sending your inquiry. Please try again or contact us directly.",
                "error",
            )
            return render_template("start_plan.html", form_data=form_data), 400

        missing_required = [
            key
            for key in ["first_name", "last_name", "email", "phone"]
            if not form_data[key]
        ]

        if missing_required or not form_data["consent"]:
            flash(
                "Please complete all required fields and consent before submitting your inquiry.",
                "error",
            )
            return render_template("start_plan.html", form_data=form_data), 400

        if not is_valid_email(form_data["email"]):
            flash("Please enter a valid email address.", "error")
            return render_template("start_plan.html", form_data=form_data), 400

        try:
            send_inquiry_emails(form_data)
            flash(
                "Thank you. Your inquiry has been received. East Street Foundation will contact you soon.",
                "success",
            )
            return redirect(url_for("start_plan"))
        except Exception:
            app.logger.exception("Failed to send inquiry email.")
            flash(
                "Something went wrong while sending your inquiry. Please try again or contact us directly.",
                "error",
            )
            return render_template("start_plan.html", form_data=form_data), 500

    return render_template("start_plan.html", form_data=empty_form)


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/legal-disclaimer")
def legal_disclaimer():
    return render_template("legal_disclaimer.html")


if __name__ == "__main__":
    app.run(debug=True)
