import streamlit as st
from PIL import Image
from datetime import datetime
import urllib.parse

# --- تحميل صورة اللوجو كأيقونة للمتجر (Favicon) ---
try:
    logo_icon = Image.open("logo.jpg")
except:
    logo_icon = "👑"

# --- إعدادات الصفحة ---
st.set_page_config(
    page_title="MORA STORE", 
    page_icon=logo_icon, 
    layout="centered"
)

# --- ربط ملف المظهر الخارجي manifest.json ---
st.markdown("""
    <head>
        <link rel="manifest" href="manifest.json">
    </head>
""", unsafe_allow_html=True)

# --- إدارة حالات Session State ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'is_admin' not in st.session_state:
    st.session_state['is_admin'] = False
if 'user_name' not in st.session_state:
    st.session_state['user_name'] = ""
if 'cart' not in st.session_state:
    st.session_state['cart'] = []
if 'discount' not in st.session_state:
    st.session_state['discount'] = 0.0
if 'all_orders' not in st.session_state:
    st.session_state['all_orders'] = []

# إدارة المخزون الافتراضي للمنتجات
if 'inventory' not in st.session_state:
    st.session_state['inventory'] = {
        "tshirt": 15, "pants": 20, "suit": 10, "perfume1": 8, "perfume2": 12,
        "watch": 5, "sneakers": 14, "jacket": 7, "sunglasses": 9, "bracelet": 25
    }

# --- تصميم الألوان والطباعة الاحترافية (CSS) ---
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #1f4068 0%, #162447 50%, #1b1b2f 100%);
            color: #ffffff;
        }
        
        h1, h2, h3 {
            color: #e4e4e4;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            text-align: center;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.4);
        }

        div.stButton > button {
            background: linear-gradient(45deg, #ff416c, #ff4b2b);
            color: white;
            border-radius: 25px;
            border: none;
            padding: 10px 20px;
            font-size: 15px;
            font-weight: bold;
            width: 100%;
            box-shadow: 0 4px 15px rgba(255, 65, 108, 0.4);
            transition: all 0.3s ease;
        }
        
        div.stButton > button:hover {
            background: linear-gradient(45deg, #ff4b2b, #ff416c);
            box-shadow: 0 6px 20px rgba(255, 75, 43, 0.6);
            transform: translateY(-2px);
        }
        
        div.stTextInput > div > div > input, div.stSelectbox > div > div, div.stRadio > div {
            border-radius: 12px;
            border: 2px solid #00adb5;
            background-color: #0f172a;
            color: white;
        }

        @media print {
            header, footer, .stButton, div[data-testid="stToolbar"], .no-print {
                display: none !important;
            }
            .stApp {
                background: white !important;
                color: black !important;
            }
            .invoice-box {
                color: black !important;
                border: 2px solid #000 !important;
                padding: 20px !important;
                background-color: #fff !important;
            }
        }
    </style>
""", unsafe_allow_html=True)

# --- صفحة تسجيل الدخول ---
def show_login_page():
    col_l1, col_l2, col_l3 = st.columns([1, 1, 1])
    with col_l2:
        try:
            st.image("logo.jpg", use_column_width=True)
        except:
            st.write("👑")
            
    st.markdown("<h1>MORA STORE</h1>", unsafe_allow_html=True)
    st.markdown("<h3>مرحباً بك، يرجى تسجيل الدخول للبدء</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.write("---")
        username = st.text_input("اسم المستخدم", placeholder="ادخل اسمك هنا...")
        password = st.text_input("كلمة المرور", type="password", placeholder="••••••••")
        
        login_button = st.button("تسجيل الدخول")
        
        if login_button:
            # دخول الأدمن الخاص
            if username.strip() == "admin" and password == "admin123":
                st.session_state['logged_in'] = True
                st.session_state['is_admin'] = True
                st.session_state['user_name'] = "الأدمن (عمر)"
                st.success("تم تسجيل الدخول كأدمن بنجاح!")
                st.rerun()
            # دخول العميل العادي
            elif username.strip() != "" and password == "12345":
                st.session_state['logged_in'] = True
                st.session_state['is_admin'] = False
                st.session_state['user_name'] = username.strip()
                st.success("تم تسجيل الدخول بنجاح!")
                st.rerun()
            elif username == "" or password == "":
                 st.warning("الرجاء إدخال اسم المستخدم وكلمة المرور.")
            else:
                st.error("كلمة المرور غير صحيحة، يرجى المحاولة مرة أخرى.")

    st.write("\n\n")
    st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 14px;'>© 2026 MORA STORE. All Rights Reserved.</p>", unsafe_allow_html=True)

# --- لوحة تحكم الأدمن ---
def show_admin_page():
    st.markdown("<h1>🛠️ لوحة تحكم الإدارة - MORA STORE</h1>", unsafe_allow_html=True)
    st.write("---")
    
    st.markdown("### 📊 إحصائيات المبيعات العامة")
    total_revenue = sum(order['total'] for order in st.session_state['all_orders'])
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.metric("عدد الطلبات المؤكدة", len(st.session_state['all_orders']))
    with col_s2:
        st.metric("إجمالي المبيعات", f"{total_revenue:.1f} جنيه")

    st.write("---")
    st.markdown("### 📦 حالة المخزون الحالي")
    inv_cols = st.columns(3)
    idx = 0
    for key, val in st.session_state['inventory'].items():
        with inv_cols[idx % 3]:
            st.info(f"<b>{key}</b>: {val} قطعة متوفرة", icon="📦")
        idx += 1

    st.write("---")
    st.markdown("### 🧾 سجل الطلبات الأخيرة")
    if not st.session_state['all_orders']:
        st.write("لا توجد طلبات مسجلة حتى الآن.")
    else:
        for ord_idx, o in enumerate(reversed(st.session_state['all_orders']), 1):
            st.markdown(f"**طلب #{ord_idx}** - العميل: `{o['user']}` | طريقة الدفع: `{o['payment']}` | الإجمالي: `{o['total']:.1f} جنيه` | الوقت: `{o['time']}`")

    st.write("\n")
    col_bt1, col_bt2, col_bt3 = st.columns([1, 2, 1])
    with col_bt2:
        if st.button("🚪 تسجيل الخروج", key="logout_admin"):
            st.session_state['logged_in'] = False
            st.session_state['is_admin'] = False
            st.session_state['user_name'] = ""
            st.rerun()

# --- صفحة المنتجات والتسوق ---
def show_products_page():
    user = st.session_state['user_name']
    
    col_top1, col_top2 = st.columns([3, 1])
    with col_top1:
        st.markdown(f"<h2>Hello, {user}! 👋</h2>", unsafe_allow_html=True)
    with col_top2:
        cart_count = len(st.session_state['cart'])
        if st.button(f"🛒 الفاتورة ({cart_count})"):
            st.session_state['show_cart'] = True
            st.rerun()

    col_img1, col_img2, col_img3 = st.columns([1, 1, 1])
    with col_img2:
        try:
            st.image("logo.jpg", width=120)
        except:
            pass

    st.markdown("<p style='text-align: center; color: #00adb5; font-size: 18px;'>استمتع بأحدث تشكيلة من منتجات وعطور وأكسسوارات MORA CLOTHING الفخمة</p>", unsafe_allow_html=True)
    st.write("---")
    
    products = [
        {"name": "هودي MORA الأسود", "price": 450, "img": "tshirt.jpg", "category": "ملابس", "has_variants": True, "key": "tshirt"},
        {"name": "شروال MORA الرياضي", "price": 350, "img": "pants.jpg", "category": "ملابس", "has_variants": True, "key": "pants"},
        {"name": "الطقم الكامل MORA", "price": 750, "img": "full_suit.jpg", "category": "ملابس", "has_variants": True, "key": "suit"},
        {"name": "عطر MORA كلاسيك", "price": 500, "img": "perfume.jpg", "category": "عطور", "has_variants": False, "key": "perfume1"},
        {"name": "عطر MORA الملكي", "price": 600, "img": "perfume2.jpg", "category": "عطور", "has_variants": False, "key": "perfume2"},
        {"name": "ساعة MORA الفاخرة", "price": 850, "img": "watch.jpg", "category": "أكسسوارات", "has_variants": False, "key": "watch"},
        {"name": "الحذاء الرياضي العصري", "price": 550, "img": "sneakers.jpg", "category": "أكسسوارات", "has_variants": True, "key": "sneakers"},
        {"name": "الجاكيت الجلد العصري", "price": 950, "img": "jacket.jpg", "category": "ملابس", "has_variants": True, "key": "jacket"},
        {"name": "النظارة الشمسية MORA", "price": 400, "img": "sunglasses.jpg", "category": "أكسسوارات", "has_variants": False, "key": "sunglasses"},
        {"name": "السوار المعدني الفاخر", "price": 250, "img": "bracelet.jpg", "category": "أكسسوارات", "has_variants": False, "key": "bracelet"}
    ]

    c_search, c_cat = st.columns([2, 1])
    with c_search:
        search_query = st.text_input("🔍 بحث عن منتج...", placeholder="اكتب اسم المنتج هنا...")
    with c_cat:
        selected_cat = st.selectbox("الأقسام", ["الكل", "ملابس", "عطور", "أكسسوارات"])

    filtered_products = [
        p for p in products 
        if (selected_cat == "الكل" or p["category"] == selected_cat)
        and (search_query.strip().lower() in p["name"].lower())
    ]

    st.write("---")

    if not filtered_products:
        st.warning("لم يتم العثور على منتجات تطابق بحثك.")
    
    for i in range(0, len(filtered_products), 2):
        col1, col2 = st.columns(2)
        
        with col1:
            p1 = filtered_products[i]
            st.subheader(p1["name"])
            st.image(p1["img"], use_column_width=True)
            st.markdown(f"**السعر:** {p1['price']} جنيه")
            
            stock1 = st.session_state['inventory'].get(p1['key'], 0)
            st.caption(f"المخزون المتاح: {stock1} قطعة")

            size_selected, color_selected = "", ""
            if p1["has_variants"]:
                if p1["key"] == "sneakers":
                    size_selected = st.selectbox("المقاس", ["40", "41", "42", "43", "44", "45"], key=f"sz_{p1['key']}")
                else:
                    size_selected =