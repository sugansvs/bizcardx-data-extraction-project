# 📇 BizCardX – Business Card Data Extraction using OCR

## 🚀 Project Overview

BizCardX is a Streamlit-based application that extracts information from business card images using Optical Character Recognition (OCR). The app processes uploaded images, extracts relevant text, and stores structured data into a database for easy access and management.

---

## 🎯 Features

* Upload business card images
* Extract text using EasyOCR
* Identify key fields:

  * Name
  * Designation
  * Company Name
  * Contact Number
  * Email
  * Website
  * Address
* Store extracted data in MySQL database
* View saved records
* Delete records

---

## 🛠️ Technologies Used

* Python
* Streamlit
* EasyOCR
* Pandas & NumPy
* MySQL
* Regex (for data cleaning)

---

## 📂 Project Structure

```
BizCardX/
│
├── app.py                # Main Streamlit application
├── database.py           # Database connection and operations
├── requirements.txt      # Required libraries
├── README.md             # Project documentation
└── images/               # Sample business card images
```

---

## ⚙️ Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/bizcardx.git
cd bizcardx
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the Streamlit app:

```bash
streamlit run app.py
```

---

## 🧠 How It Works

1. User uploads a business card image
2. EasyOCR extracts raw text from the image
3. Regex and logic are applied to classify fields
4. Structured data is displayed
5. Data is stored in MySQL database

---

## 📊 Database Schema

| Field Name   | Description   |
| ------------ | ------------- |
| Name         | Person's Name |
| Designation  | Job Title     |
| Company Name | Company       |
| Contact      | Phone Number  |
| Email        | Email Address |
| Website      | Website URL   |
| Address      | Full Address  |
| Pincode      | Postal Code   |

---

## 🎥 Demo Video

[Watch Demo](https://drive.google.com/drive/folders/18jGdNZrK4glWeL5IU-DsicYbo0LIW4Uh)

---

## ✅ Use Cases

* Digital business card management
* Contact information automation
* Data entry reduction

---

## 🔮 Future Enhancements

* Improve OCR accuracy
* Add support for multiple languages
* Export data to Excel/CSV
* Deploy on cloud (Streamlit Cloud)

---

## 👤 Author

**Sugan**

---

## ⭐ Acknowledgements

* EasyOCR documentation
* Streamlit community

---

## 📌 License

This project is for educational purposes.
