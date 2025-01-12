from flask import Flask, render_template, request, send_file
import os

app = Flask(__name__)

# Root directory where the data is stored
ROOT_DIR = "data"

# Search function
def search_files(coupon_rate=None, company_name=None):
    results = []
    for root, dirs, files in os.walk(ROOT_DIR):
        for file in files:
            if file.endswith(".xlsx") or file.endswith(".xls"):
                coupon_match = str(coupon_rate) in file if coupon_rate else True
                company_match = company_name.lower() in root.lower() if company_name else True
                if coupon_match and company_match:
                    # Parse Coupon Rate and Maturity Year from the file name
                    parts = file.split("_")
                    if len(parts) >= 3:
                        parsed_coupon = parts[1]  # Second part is the coupon rate
                        maturity_year = parts[2].split(".")[0]  # Third part is maturity year
                    else:
                        parsed_coupon = "Unknown"
                        maturity_year = "Unknown"
                    
                    results.append({
                        "issuer": os.path.basename(root),
                        "coupon_rate": parsed_coupon,
                        "file_name": file,
                        "maturity_year": maturity_year,
                        "file_path": os.path.join(root, file)
                    })
    return results

# Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    coupon_rate = request.form.get("coupon_rate", "").strip()
    company_name = request.form.get("company_name", "").strip()
    results = search_files(coupon_rate, company_name)
    return render_template("results.html", results=results)

@app.route("/download/<path:filepath>")
def download(filepath):
    # Serve the file for download
    try:
        return send_file(filepath, as_attachment=True)
    except Exception as e:
        return f"Error downloading file: {e}"

if __name__ == "__main__":
    app.run(debug=True)
