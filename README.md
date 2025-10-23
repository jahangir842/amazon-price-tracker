# Amazon Price Tracker

This project tracks prices of Amazon products and sends notifications when prices drop, fully automated and containerized for cloud deployment.

---

## **Features**

* Track multiple Amazon products and their prices
* Send notifications via Slack when price drops below target
* Persist product and price data in CSV (can be extended to DB)
* Run headless browsers using **Xvfb** in Docker
* CI/CD integration with GitHub Actions for automated runs
* Optional scheduling using GitHub cron or cloud cron jobs
* Fully containerized and portable for deployment on AWS, GCP, or local servers

---

## **Tech Stack**

* **Python 3** with **Selenium** and **chromedriver-autoinstaller**
* **Chrome Browser / Headless Chrome**
* **Docker & Xvfb** for running browsers without GUI
* **GitHub Actions** for CI/CD & scheduled execution
* **Slack** notifications (configurable for other services)

---

## **Project Structure**

```
amazon-price-tracker/
│
├── .github/workflows/ci.yml    # GitHub Actions pipeline
├── docker/Dockerfile           # Docker container for tracker
├── src/
│   ├── tracker.py              # Main price tracking logic
│   ├── notifier.py             # Notification logic
│   └── utils.py                # Helper functions
├── products.csv                # Products to track
├── requirements.txt            # Python dependencies
├── README.md
└── .gitignore
```

---

## **Getting Started**

### **Prerequisites**

* Python 3.11+
* Docker (optional for containerized execution)
* Slack Webhook URL for notifications (optional)

### **Local Installation**

```bash
git clone git@github.com:jahangir80842/amazon-price-tracker.git
cd amazon-price-tracker
pip install -r requirements.txt
```

### **Running the Tracker Locally**

```bash
python src/tracker.py
```

> By default, it runs in **headless mode**. Remove `--headless` in `tracker.py` to run headful for debugging.

### **Running in Docker**

```bash
docker build -t amazon-tracker ./docker
docker run --rm amazon-tracker
```

---

## **GitHub Actions CI/CD**

A pipeline is included to run the tracker automatically:

```yaml
on:
  push:
    branches: [main]
  schedule:
    - cron: '0 9 * * *'  # Runs daily at 9 AM UTC
```

The workflow installs dependencies, runs the tracker using `xvfb-run`, and sends Slack notifications if prices drop.

---

## **Products Configuration**

Edit `products.csv` to track new products:

```
url,desired_price,last_price
https://www.amazon.com/dp/B08N5WRWNW,300,0
https://www.amazon.com/dp/B09G3HRMVB,150,0
```

* `url`: Amazon product URL
* `desired_price`: Alert threshold
* `last_price`: Updated automatically after each run

---

## **Advanced Features & Extensions**

* **Database support:** Replace CSV with SQLite/PostgreSQL for large-scale tracking
* **Multiple browsers:** Run parallel trackers using multiple `Xvfb` displays
* **Additional notifications:** Email, Discord, Telegram
* **Error handling & retries:** Handle page layout changes or network errors
* **Cloud deployment:** Deploy on **AWS EC2**, **AWS Fargate**, or **GCP Cloud Run**

---

## **DevOps Relevance**

* Version control & modular structure for maintainability
* Containerized workflow for portability
* Automated CI/CD & scheduling for production-grade deployment
* Scalable design to track hundreds of products concurrently

---

## **License**

MIT License – see LICENSE file

---
