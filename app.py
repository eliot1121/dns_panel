from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import datetime

app = Flask(__name__)

# فایل برای ذخیره اطلاعات DNS‌ها
dns_file = 'dns_data.json'

# بررسی و بارگذاری داده‌ها از فایل JSON
def load_dns_data():
    if os.path.exists(dns_file):
        with open(dns_file, 'r') as f:
            return json.load(f)
    else:
        return {"dns_records": []}

# ذخیره داده‌ها در فایل JSON
def save_dns_data(data):
    with open(dns_file, 'w') as f:
        json.dump(data, f, indent=4)

# صفحه اصلی - نمایش DNS‌ها
@app.route('/')
def index():
    dns_data = load_dns_data()
    # بررسی تاریخ انقضا و غیرفعال کردن DNS‌ها
    for record in dns_data["dns_records"]:
        expire_date = datetime.strptime(record["expire_date"], "%Y-%m-%d")
        if expire_date < datetime.now():
            record["status"] = "inactive"
    save_dns_data(dns_data)
    return render_template('index.html', dns_data=dns_data)

# صفحه برای اضافه کردن DNS جدید
@app.route('/add', methods=['GET', 'POST'])
def add_dns():
    if request.method == 'POST':
        dns = request.form['dns']
        expire_date = request.form['expire_date']
        new_record = {
            "dns": dns,
            "expire_date": expire_date,
            "status": "active"
        }
        dns_data = load_dns_data()
        dns_data["dns_records"].append(new_record)
        save_dns_data(dns_data)
        return redirect(url_for('index'))
    return render_template('add_dns.html')

# صفحه برای حذف DNS
@app.route('/delete/<int:index>', methods=['GET'])
def delete_dns(index):
    dns_data = load_dns_data()
    dns_data["dns_records"].pop(index)
    save_dns_data(dns_data)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)