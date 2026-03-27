import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import easyocr
import pandas as pd
import numpy as np
import regex as re
import io
import mysql.connector

def image_to_text(path):

    # Extract text from business card image using EasyOCR

    input_img = Image.open(path)
    image_arr = np.array(input_img)

    reader = easyocr.Reader(['en'], gpu=False)
    text_list = reader.readtext(image_arr, detail=0)

    return text_list, input_img


def extracted_text(texts):

  extrd_dict = {"NAME":[], "DESIGNATION":[], "COMPANY_NAME":[], "CONTACT":[], "EMAIL":[], "WEBSITE":[],
                "ADDRESS":[], "PINCODE":[]}

  extrd_dict["NAME"].append(texts[0])
  extrd_dict["DESIGNATION"].append(texts[1])

  for i in range(2,len(texts)):

    if texts[i].startswith("+") or (texts[i].replace("-","").isdigit() and '-' in texts[i]):

      extrd_dict["CONTACT"].append(texts[i])

    elif "@" in texts[i] and ".com" in texts[i]:
      extrd_dict["EMAIL"].append(texts[i])

    elif "WWW" in texts[i] or "www" in texts[i] or "Www" in texts[i] or "wWw" in texts[i] or "wwW" in texts[i]:
      small= texts[i].lower()
      extrd_dict["WEBSITE"].append(small)

    elif "Tamil Nadu" in texts[i] or "TamilNadu" in texts[i] or texts[i].isdigit():
      extrd_dict["PINCODE"].append(texts[i])


    elif re.match(r'^[A-Za-z]', texts[i]):
      extrd_dict["COMPANY_NAME"].append(texts[i])

    else:
      remove_colon= re.sub(r'[,;]','',texts[i])
      extrd_dict["ADDRESS"].append(remove_colon)

  for key,value in extrd_dict.items():
    if len(value)>0:
      concadenate= " ".join(value)
      extrd_dict[key] = [concadenate]

    else:
      value = "NA"
      extrd_dict[key] = [value]

  return extrd_dict

def get_connection():
    conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345",
    database="bizcard_db"
    )
    return conn

# ---------- COLORFUL CSS ----------
st.markdown("""
<style>

.main {
background: linear-gradient(120deg,#667eea,#764ba2);
}

.block-container {
padding-top: 2rem;
}

.kpi {
background: white;
padding: 20px;
border-radius: 16px;
box-shadow: 0px 6px 18px rgba(0,0,0,0.15);
text-align:center;
}

.sidebar .sidebar-content {
background: linear-gradient(#ff9966,#ff5e62);
}

</style>
""", unsafe_allow_html=True)
# streamlit part

st.set_page_config(page_title="BizCardX", layout="wide")
st.title("📇 BizCardX - Business Card OCR Extraction")

# ---------- SIDEBAR MENU ----------
with st.sidebar:

    menu = option_menu(
        "📊 BizCardX Menu",
        ["Home","Upload Card","Preview","Modify","Delete"],
        icons=["house","cloud-upload","table","pencil-square","trash"],
        menu_icon="grid",
        default_index=0,
        styles={
            "container":{"padding":"5px"},
            "icon":{"color":"white","font-size":"20px"},
            "nav-link":{
                "color":"white",
                "font-size":"16px",
                "text-align":"left",
                "margin":"3px",
                "--hover-color":"#ffffff30"
            },
            "nav-link-selected":{
                "background":"#ffffff40"
            }
        }
    )


# HOME PAGE
if menu == "Home":

    st.header("Project Overview")
    st.write("""
    This application extracts business card information using EasyOCR.
    
    Features:
    - Upload business card image
    - Extract Name, Phone, Email, Website, Address
    - Store data in database
    - View, modify and delete records
    """)

    st.subheader("🛠 Tools & Technologies Used")

    st.write("""
    - **Python** → Core programming language  
    - **Streamlit** → Web application framework  
    - **EasyOCR** → Optical Character Recognition for text extraction  
    - **MySQL** → Database for storing structured contact details  
    - **Pandas** → Data processing and table handling  
    - **NumPy** → Image array manipulation  
    - **Pillow (PIL)** → Image processing  
    - **Regex** → Pattern matching for contact/email extraction  
    """)

elif menu == "Upload Card":

    img = st.file_uploader(
        "Upload a business card image",
        type=["jpg", "jpeg", "png"]
    )

    if img is not None:

        # Show uploaded image
        st.image(img, width="stretch", caption="Uploaded Card")

        try:
            # OCR Processing
            text_image, input_image = image_to_text(img)

            # Extract structured data
            text_dict = extracted_text(text_image)

            if text_dict and len(text_dict) > 0:
                st.success("✅ Text extracted successfully!")

                df = pd.DataFrame(text_dict)
                Image_bytes = io.BytesIO()
                input_image.save(Image_bytes, format='PNG')
                image_data = Image_bytes.getvalue()


                # Createing Disctionary to store the extracted data and image
                data_dict = {"IMAGE":[image_data]}
                df_1 = pd.DataFrame(data_dict)

                concat_df = pd.concat([df, df_1], axis=1)


                st.dataframe(concat_df, width="stretch")

                button_1 = st.button("Upload Database", width="stretch")

                if button_1:
                 
                  conn = get_connection()
                  cursor = conn.cursor()

                  create_table_query = """
                  CREATE TABLE IF NOT EXISTS bizcard_details (
                      id INT AUTO_INCREMENT PRIMARY KEY,
                      name TEXT,
                      designation TEXT,
                      company TEXT,
                      contact TEXT,
                      email TEXT,
                      website TEXT,
                      address TEXT,
                      pincode TEXT,
                      image LONGBLOB
                  );
                  """

                  cursor.execute(create_table_query)

                  query = """
                  INSERT INTO bizcard_details
                  (name, designation, company, contact, email, website, address, pincode, image)
                  VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                  """

                  values = (concat_df["NAME"].astype(str).values[0],
                          concat_df["DESIGNATION"].astype(str).values[0],
                          concat_df["COMPANY_NAME"].astype(str).values[0],
                          concat_df["CONTACT"].astype(str).values[0],
                          concat_df["EMAIL"].astype(str).values[0],
                          concat_df["WEBSITE"].astype(str).values[0],
                          concat_df["ADDRESS"].astype(str).values[0],
                          concat_df["PINCODE"].astype(str).values[0],
                          concat_df["IMAGE"].values[0])

                  cursor.execute(query, values)
                  conn.commit()
                  conn.close()

                  st.success("SAVED SUCCESSFULLY")

            else:
                st.warning("⚠️ No text detected. Try another image.")

        except Exception as e:
            st.error(f"❌ Error while processing image: {e}")


# ---------- PREVIEW ----------
elif menu == "Preview":

    st.header("📋 Stored Contacts")

    conn = get_connection()
    df = pd.read_sql("SELECT * FROM bizcard_details", conn)

    st.dataframe(
        df.drop(columns=["image"]),
        width="stretch",
        hide_index=True
    )

elif menu == "Modify":
    st.header("✏ Modify Business Card Details")

    conn = get_connection()
    df = pd.read_sql("SELECT * FROM bizcard_details", conn)

    if df.empty:
        st.warning("No records available")
        st.stop()

    col1, col2 = st.columns([1,2])

    with col1:
        selected_name = st.selectbox("Select Contact", df["name"])

    record = df[df["name"] == selected_name].iloc[0]

    st.markdown("<div class='edit-card'>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        mo_name = st.text_input("👤 Name", record["name"])
        mo_desig = st.text_input("💼 Designation", record["designation"])
        mo_comp = st.text_input("🏢 Company", record["company"])
        mo_cont = st.text_input("📞 Contact", record["contact"])
        mo_email = st.text_input("📧 Email", record["email"])

    with c2:
        mo_web = st.text_input("🌐 Website", record["website"])
        mo_addr = st.text_area("📍 Address", record["address"])
        mo_pin = st.text_input("📮 Pincode", record["pincode"])

        if record["image"]:
            st.image(record["image"], width=180)

    st.markdown("</div>", unsafe_allow_html=True)

    st.divider()

    if st.button("🚀 Update Contact", type="primary", width="stretch"):

        cursor = conn.cursor()

        update_query = """
        UPDATE bizcard_details
        SET name=%s, designation=%s, company=%s,
            contact=%s, email=%s, website=%s,
            address=%s, pincode=%s
        WHERE id=%s
        """

        cursor.execute(update_query, (
            mo_name,
            mo_desig,
            mo_comp,
            mo_cont,
            mo_email,
            mo_web,
            mo_addr,
            mo_pin,
            int(record["id"])
        ))

        conn.commit()
        conn.close()

        st.success("🎉 Contact Updated Successfully")  
 

elif menu == "Delete":

    st.header("🗑 Delete Business Card")

    conn = get_connection()

    df = pd.read_sql(
        "SELECT id,name,designation FROM bizcard_details",
        conn
    )

    if df.empty:
        st.warning("No records available")
        st.stop()

    col1, col2 = st.columns(2)

    with col1:
        selected_name = st.selectbox(
            "Select Name",
            df["name"]
        )

    record_df = df[df["name"] == selected_name]

    with col2:
        selected_desig = st.selectbox(
            "Select Designation",
            record_df["designation"]
        )

    record = record_df[
        record_df["designation"] == selected_desig
    ].iloc[0]

    st.markdown("<div class='delete-card'>", unsafe_allow_html=True)

    st.write("### Selected Record")
    st.write("👤 Name :", record["name"])
    st.write("💼 Role :", record["designation"])

    st.markdown("</div>", unsafe_allow_html=True)

    st.divider()

    if st.button("🚨 Confirm Delete", type="primary", width="stretch"):

        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM bizcard_details WHERE id=%s",
            (int(record["id"]),)
        )

        conn.commit()
        cursor.close()
        conn.close()

        st.success("✅ Record Deleted Successfully")