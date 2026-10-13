import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import re
import uuid

# --- إعدادات النظام العالمي السيادي (v16.1 Professional UI & FAO Management) ---
st.set_page_config(
    page_title="FAO-UNV Sovereign Enterprise Hub v16.1",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- تخصيص واجهة المستخدم المتقدمة والمتجاوبة (Enterprise CSS & Professional Frontend) ---
st.markdown("""
    <style>
    body, [data-testid="stAppViewContainer"] {
        direction: rtl;
        text-align: right;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background-color: #f4f6f9;
    }
    .stTabs [data-baseweb="tab-list"] {
        flex-direction: row-reverse;
        flex-wrap: wrap;
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 52px;
        background-color: #ffffff;
        border-radius: 8px 8px 0px 0px;
        font-weight: 700;
        color: #002b49;
        border: 1px solid #cbd5e1;
        padding: 0 18px;
        font-size: 14px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    .stTabs [aria-selected="true"] {
        background-color: #0076a8 !important;
        color: white !important;
    }
    .hero-v16-banner {
        background: linear-gradient(135deg, #001f3f 0%, #0076a8 100%);
        color: white;
        padding: 45px;
        border-radius: 14px;
        margin-bottom: 25px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.15);
        text-align: right;
    }
    .v16-badge {
        background-color: #e2f0d9;
        color: #276749;
        padding: 6px 14px;
        border-radius: 6px;
        font-weight: bold;
        font-size: 13px;
        border: 1px solid #c6f6d5;
        display: inline-block;
    }
    .v16-card {
        background-color: white;
        padding: 24px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        border-right: 6px solid #0076a8;
        margin-bottom: 18px;
        text-align: right;
    }
    .fao-admin-card {
        background-color: white;
        padding: 24px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        border-right: 6px solid #10b981;
        margin-bottom: 18px;
        text-align: right;
    }
    [data-testid="stMetricValue"], [data-testid="stMetricDelta"] {
        direction: rtl;
        text-align: right;
    }
    .v16-footer {
        text-align: center;
        padding: 30px;
        color: #4a5568;
        font-size: 14px;
        border-top: 1px solid #cbd5e1;
        margin-top: 50px;
    }
    @media (max-width: 768px) {
        .hero-v16-banner { padding: 20px; }
        .stTabs [data-baseweb="tab"] { font-size: 12px; height: 45px; padding: 0 10px; }
    }
    </style>
""", unsafe_allow_html=True)

# --- الحالة والتخزين المؤقت للبيانات التشغيلية ---
if 'v16_interstellar_status' not in st.session_state:
    st.session_state.v16_interstellar_status = {
        "Interstellar Food Logistics": "🟢 نشط (تتبع شحنات الغذاء)",
        "Molecular Nanotechnology": "🟢 مفعل (أسراب الروبوتات النانوية)"
    }

if 'interstellar_shipments' not in st.session_state:
    st.session_state.interstellar_shipments = [
        {"shipment_id": "#MARS-SUPPLY-01", "origin": "محطة الأرض المركزية للفاو", "destination": "مستعمرة أريس - كوكب المريخ", "cargo": "بذور قمح معدلة وراثياً", "status": "في مسار الالتفاف الكوكبي"},
        {"shipment_id": "#LUNAR-SUPPLY-04", "origin": "إقليم الدلتا - الأرض", "destination": "قاعدة القمر الزراعية الحية", "cargo": "مغذيات حيوية نانوية", "status": "تم التسليم بنجاح"}
    ]

def sanitize_v16_input(text):
    if not text:
        return ""
    clean = re.sub(r'<[^>]*>', '', text)
    return clean.strip()

# --- الشريط الجانبي للإصدار المحترف ---
with st.sidebar:
    st.markdown("### **FAO Global Enterprise Gateway**")
    st.markdown('<p class="v16-badge">🌐 v16.1 Sovereign Production</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("#### 🌠 مؤشرات الإدارة والتشغيل")
    for tech, st_v in st.session_state.v16_interstellar_status.items():
        st.markdown(f"**{tech}**\n{st_v}")
        
    st.markdown("---")
    st.markdown("**المعماري ومبتكر النظام السيادي:**\nمهندس/ كريم عمرو محمد")

# --- واجهة البطل الكبرى ---
st.markdown("""
    <div class="hero-v16-banner">
        <h1>🌍 منظمة الأغذية والزراعة للأمم المتحدة (FAO)</h1>
        <h3>المنظومة السيادية المركزية v16.1 (إدارة الفاو المؤسسية، الخريطة العالمية مع فلسطين، وتقنيات المستقبل)</h3>
        <p>منصة إدارية وتشغيلية متكاملة تخدم قطاعات الفاو الرسمية، تدعم الصمود الزراعي في فلسطين، وتدير سلاسل الإمداد الكونية.</p>
    </div>
""", unsafe_allow_html=True)

# --- التبويبات الرئيسية (شاملة الإدارة، فلسطين، الخريطة العالمية، والمستقبل) ---
tab_fao_mgmt, tab_palestine_desk, tab_space_logistics, tab_global_gis, tab_nanobots, tab_bi_v16 = st.tabs([
    "🏛️ إدارة الفاو والقطاعات التشغيلية", 
    "🇵🇸 مكتب فلسطين والصمود الزراعي", 
    "🚀 الإمداد الزراعي عابر الكواكب", 
    "🗺️ الخريطة العالمية (World GIS Map)", 
    "🔬 تكنولوجيا النانو والتربة", 
    "📊 المؤشرات الاستراتيجية (BI)"
])

# ================= TAB 0: إدارة الفاو والقطاعات التشغيلية =================
with tab_fao_mgmt:
    st.subheader("🏛️ قطاعات وأقسام الإدارة المركزية لمنظمة الفاو (FAO Central Management)")
    st.markdown("الوحدات الأساسية المسؤولة عن التخطيط، الإنذار المبكر، والأمن الغذائي العالمي:")
    
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.markdown("""
            <div class="fao-admin-card">
                <h4>🚨 إدارة الطوارئ الغذائية والإنذار المبكر</h4>
                <p>مراقبة مؤشرات المجاعة العالمية، تقييم نقص المحاصيل الناتج عن التغيرات المناخية، والتنسيق الفوري مع الحكومات.</p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("""
            <div class="fao-admin-card">
                <h4>🌾 قطاع الأمن الغذائي وتنمية الموارد المائية</h4>
                <p>إدارة استراتيجيات المياه المستدامة، دعم أنظمة الري الحديثة، وتطوير سلاسل القيمة الغذائية في الدول النامية.</p>
            </div>
        """, unsafe_allow_html=True)
    with col_m2:
        st.markdown("""
            <div class="fao-admin-card">
                <h4>🛡️ سياسات 'الصحة الواحدة' ومقاومة المضادات (AMR)</h4>
                <p>تنفيذ البروتوكولات الدولية للحد من الاستخدام المفرط لمضادات الميكروبات في الثروة الحيوانية والزراعة.</p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("""
            <div class="fao-admin-card">
                <h4>📡 قسم الأقمار الصناعية والاستشعار عن بُعد</h4>
                <p>معالجة صور الأقمار الصناعية الحية لتقييم صحة الغطاء النباتي (NDVI) وتوقع الإنتاجية الزراعية.</p>
            </div>
        """, unsafe_allow_html=True)

# ================= TAB 1: مكتب فلسطين والصمود الزراعي =================
with tab_palestine_desk:
    st.subheader("🇵🇸 مكتب فلسطين - الدعم الإقليمي والصمود الزراعي")
    st.markdown("متابعة ودعم الأمن الغذائي، المزارعين، والتعاونيات الزراعية في فلسطين الأبية:")
    
    st.markdown("""
        <div class="fao-admin-card" style="border-right-color: #dc2626;">
            <h4>🇵🇸 برامج الدعم والتمكين الزراعي في فلسطين</h4>
            <p>• <b>مراصد الأمن الغذائي:</b> تتبع وتوثيق حالة المحاصيل، شبكات الري، والموارد المائية في الأراضي الفلسطينية.</p>
            <p>• <b>برامج الإغاثة الفورية:</b> تنسيق المساعدات الزراعية، البذور المحسنة، والمغذيات للتعاونيات والمزارعين.</p>
            <p>• <b>السيادة المكانية:</b> تم إثبات وتثبيت إحداثيات دولة <b>فلسطين الحبيبة</b> على الخرائط التفاعلية للمنظومة.</p>
        </div>
    """, unsafe_allow_html=True)

# ================= TAB 2: الإمداد الزراعي عابر الكواكب =================
with tab_space_logistics:
    st.subheader("🚀 الإمداد الزراعي وسلاسل التوريد عابرة الكواكب (Interstellar Logistics)")
    st.markdown("تتبع شحنات الغذاء والمحاصيل المعدلة وراثياً عبر الفضاء السحيق بين كوكب الأرض والمستعمرات على المريخ والقمر:")
    
    for shp in st.session_state.interstellar_shipments:
        st.markdown(f"""
            <div class="v16-card">
                <h4>🚀 شحنة فضائية: {shp['shipment_id']}</h4>
                <p><b>من نقطة الإطلاق:</b> {shp['origin']}</p>
                <p><b>إلى المستعمرة الوجهة:</b> {shp['destination']}</p>
                <p><b>طبيعة الحمولة الزراعية:</b> {shp['cargo']}</p>
                <p><b>حالة المسار الفضائي:</b> <span style="color: #7e22ce; font-weight: bold;">{shp['status']}</span></p>
            </div>
        """, unsafe_allow_html=True)
        
    with st.form("interstellar_form"):
        st.markdown("#### ➕ إطلاق شحنة إمداد غذائي جديدة نحو الكواكب الأخرى:")
        dest_colony = st.text_input("المستعمرة الفضائية الوجهة (المريخ، القمر، إلخ):")
        cargo_desc = st.text_input("وصف الشحنة الزراعية أو البذور:")
        ship_btn = st.form_submit_button("إطلاق الشحنة عبر الفضاء السحيق 🌌")
        
        if ship_btn and dest_colony and cargo_desc:
            new_sid = f"#SPACE-SUP-{str(uuid.uuid4())[:4].upper()}"
            st.session_state.interstellar_shipments.append({
                "shipment_id": new_sid,
                "origin": "محطة الأرض المركزية للفاو",
                "destination": sanitize_v16_input(dest_colony),
                "cargo": sanitize_v16_input(cargo_desc),
                "status": "في مسار الالتفاف الكوكبي نحو الفضاء السحيق"
            })
            st.success(f"✨ تم إطلاق الشحنة بنجاح برقم تعريف كوني {new_sid}!")
            st.rerun()

# ================= TAB 3: الخريطة العالمية (World GIS Map) =================
with tab_global_gis:
    st.subheader("🗺️ خريطة العالم التفاعلية ومكاتب الفاو الإقليمية (World GIS & Palestine Sovereignty)")
    st.markdown("خريطة عالمية شاملة تظهر دول العالم مع تثبيت إحداثيات **فلسطين الحبيبة** بشكل دقيق:")
    
    # خريطة عالمية طبيعية عادية، مع إضافة إحداثيات عالمية وفلسطين بدون أي تمركز مزعج
    world_map_df = pd.DataFrame({
        'lat': [30.0444, 31.9522, 40.7128, 51.5074, 35.6762, -1.2921],
        'lon': [31.2357, 35.2332, -74.0060, -0.1278, 139.6503, 36.8219],
        'location': ['مقر الفاو الإقليمي - القاهرة', 'فلسطين الأبية (القدس / غزة / الضفة)', 'المقر الأمريكي', 'المقر الأوروبي (روما/لندن)', 'مكتب آسيا', 'مكتب إفريقيا']
    })
    st.map(world_map_df, size=60, color='#0076a8')

# ================= TAB 4: تكنولوجيا النانو والتربة =================
with tab_nanobots:
    st.subheader("🔬 تكنولوجيا النانو الجزيئية وروبوتات التربة الحية (Molecular Nanotechnology)")
    st.markdown("أسراب من الروبوتات النانوية المجهرية المحقونة في التربة لإصلاح الخلايا التالفة للمحاصيل:")
    
    st.markdown("""
        <div class="v16-card">
            <h4>🔬 شبكة النانوبات المجهرية (Soil Nanobots Network)</h4>
            <p>• <b>الإصلاح الخلوي الذاتي:</b> ترصد أسراب النانوبات أي خلل في خلايا جذور النباتات وتقوم بإصلاحها مجهرياً.</p>
            <p>• <b>التعديل الجيني الميداني:</b> إعادة برمجة تسلسل الـ DNA للمحاصيل لتتحمل الجفاف الشديد والملوحة المطلقة.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("تفعيل أسراب النانوبات لإصلاح الحقول ميدانياً (Deploy Nanobots) ⚡"):
        st.success("🔬 تم حقن وتفعيل أسراب الروبوتات النانوية في التربة بنجاح! جاري إصلاح الخلايا النباتية وتعديل الجينات.")

# ================= TAB 5: المؤشرات الاستراتيجية =================
with tab_bi_v16:
    st.subheader("📊 لوحات المؤشرات الإستراتيجية لمنظمة الفاو (Enterprise BI)")
    fig_v16 = px.bar(
        pd.DataFrame({'Metric': ['إدارة الطوارئ', 'دعم فلسطين', 'الأمن الغذائي', 'التكنولوجيا الكونية'], 'Score': [100, 100, 100, 100]}),
        x='Metric', y='Score', color='Score', color_continuous_scale='Teal'
    )
    st.plotly_chart(fig_v16, use_container_width=True)

# --- التذييل النهائي المعتمد ---
st.markdown("""
    <div class="v16-footer">
        FAO Representation in Egypt & Palestine Regional Office | Sovereign Enterprise System v16.1 <br>
        Engineered with World GIS, Palestine Sovereignty, and FAO Central Management by <b>Eng. Kareem Amr Mohamed</b>.
    </div>
""", unsafe_allow_html=True)