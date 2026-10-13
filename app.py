import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import re
import uuid

# --- إعدادات النظام العالمي السيادي (v17.0 FAO Enterprise Hub) ---
st.set_page_config(
    page_title="FAO Global Sovereign Enterprise Hub v17.0",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- تخصيص واجهة المستخدم المتقدمة والمتجاوبة (Enterprise UI & RTL) ---
st.markdown("""
    <style>
    body, [data-testid="stAppViewContainer"] {
        direction: rtl;
        text-align: right;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background-color: #f8fafc;
    }
    .stTabs [data-baseweb="tab-list"] {
        flex-direction: row-reverse;
        flex-wrap: wrap;
        gap: 6px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: #ffffff;
        border-radius: 6px 6px 0px 0px;
        font-weight: 700;
        color: #002b49;
        border: 1px solid #cbd5e1;
        padding: 0 15px;
        font-size: 14px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0076a8 !important;
        color: white !important;
    }
    .hero-banner {
        background: linear-gradient(135deg, #001f3f 0%, #0076a8 100%);
        color: white;
        padding: 40px;
        border-radius: 14px;
        margin-bottom: 25px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.15);
        text-align: right;
    }
    .fao-badge {
        background-color: #e2f0d9;
        color: #276749;
        padding: 6px 14px;
        border-radius: 6px;
        font-weight: bold;
        font-size: 13px;
        border: 1px solid #c6f6d5;
        display: inline-block;
    }
    .fao-card {
        background-color: white;
        padding: 24px;
        border-radius: 8px;
        box-shadow: 0 3px 6px rgba(0,0,0,0.06);
        border-right: 6px solid #0076a8;
        margin-bottom: 15px;
        text-align: right;
    }
    [data-testid="stMetricValue"], [data-testid="stMetricDelta"] {
        direction: rtl;
        text-align: right;
    }
    .fao-footer {
        text-align: center;
        padding: 30px;
        color: #4a5568;
        font-size: 14px;
        border-top: 1px solid #e2e8f0;
        margin-top: 50px;
    }
    @media (max-width: 768px) {
        .hero-banner { padding: 20px; }
        .stTabs [data-baseweb="tab"] { font-size: 12px; height: 45px; padding: 0 8px; }
    }
    </style>
""", unsafe_allow_html=True)

# --- حالة الأقسام الإدارية والعمليات (v17.0 State) ---
if 'fao_admin_status' not in st.session_state:
    st.session_state.fao_admin_status = {
        "Global Food Security Division": "🟢 نشط (مراقبة أسواق الغذاء العالمية)",
        "Early Warning & Crisis Response Center": "🟢 نشط (رصد الطوارئ المناخية والزراعية)",
        "Sustainable Agricultural Development": "🟢 نشط (إدارة مشاريع التنمية الإقليمية)",
        "One Health & AMR Surveillance": "🟢 نشط (مكافحة مقاومة مضادات الميكروبات)"
    }

if 'fao_reports' not in st.session_state:
    st.session_state.fao_reports = [
        {"id": "#FAO-REP-01", "department": "الأمن الغذائي العالمي", "region": "منطقة الشرق الأوسط وشمال إفريقيا", "summary": "تقييم مؤشرات الاكتفاء الذاتي وسلاسل الإمداد الإقليمية.", "date": "2026-10-13"},
        {"id": "#FAO-REP-02", "department": "مكتب فلسطين الإقليمي", "region": "فلسطين (الضفة الغربية وقطاع غزة)", "summary": "دعم الصمود الزراعي، توفير المدخلات، وإعادة تأهيل شبكات الري.", "date": "2026-10-13"}
    ]

# دالة تنقية المدخلات
def sanitize_input(text):
    if not text:
        return ""
    clean = re.sub(r'<[^>]*>', '', text)
    return clean.strip()

# --- الشريط الجانبي للإصدار 17.0 ---
with st.sidebar:
    st.markdown("### **FAO Global Gateway**")
    st.markdown('<p class="fao-badge">🌐 v17.0 Enterprise Management</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("#### 🏛️ حالة الأقسام الإدارية المركزية")
    for dept, stat in st.session_state.fao_admin_status.items():
        st.markdown(f"**{dept}**\n{stat}")
        
    st.markdown("---")
    st.markdown("**المعماري ومصمم النظام:**\nمهندس/ كريم عمرو محمد")

# --- واجهة البطل الكبرى ---
st.markdown("""
    <div class="hero-banner">
        <h1>🌍 منظمة الأغذية والزراعة للأمم المتحدة (FAO)</h1>
        <h3>المنظومة الإدارية والتشغيلية السيادية v17.0 (إدارة الفاو المركزية، الخريطة العالمية، ودعم فلسطين الأبية)</h3>
        <p>نظام إداري وتقني متكامل يدير أقسام الفاو العالمية، يتابع الأمن الغذائي، ويدعم العمليات الإقليمية بشفافية مطلقة.</p>
    </div>
""", unsafe_allow_html=True)

# --- التبويبات الرئيسية المحدثة ---
tab_admin_fao, tab_world_map, tab_operations, tab_bi_v17, tab_admin_control = st.tabs([
    "🏛️ الأقسام الإدارية والتشغيلية للفاو", 
    "🗺️ خريطة العالم ومكتب فلسطين الإقليمي", 
    "📋 سجل التقارير والتدخلات الميدانية", 
    "📊 لوحات التحليلات الاستراتيجية (BI)", 
    "⚙️ لوحة التحكم وإدارة النظام"
])

# ================= TAB 0: الأقسام الإدارية والتشغيلية للفاو =================
with tab_admin_fao:
    st.subheader("🏛️ قطاعات وإدارات منظمة الأغذية والزراعة (FAO Core Divisions)")
    st.markdown("الوحدات الاستراتيجية المسؤولة عن رسم السياسات وتوجيه العمليات الزراعية عالمياً:")
    
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        st.markdown("""
            <div class="fao-card">
                <h4>🌾 قسم الأمن الغذائي والأسواق العالمية</h4>
                <p>متابعة أسعار الغذاء العالمية، تحليل مؤشرات العرض والطلب، وتوفير قواعد البيانات الإحصائية لدعم استقرار الأسواق وتجنب الأزمات.</p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("""
            <div class="fao-card">
                <h4>🚨 مركز الإنذار المبكر وإدارة الأزمات</h4>
                <p>رصد التغيرات المناخية الحادة، الجفاف، والآفات الزراعية الطارئة لإنذار الحكومات وإطلاق خطط الاستجابة الإنسانية الفورية.</p>
            </div>
        """, unsafe_allow_html=True)
    with col_a2:
        st.markdown("""
            <div class="fao-card">
                <h4>🌱 إدارة التنمية الزراعية المستدامة</h4>
                <p>تطوير الممارسات الزراعية الحديثة، الحفاظ على الموارد المائية، وتحسين إنتاجية المحاصيل عبر تقنيات الاستشعار عن بعد والأقمار الصناعية.</p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("""
            <div class="fao-card">
                <h4>🛡️ مبادرة 'الصحة الواحدة' ومقاومة المضادات</h4>
                <p>تنسيق الجهود الدولية للحد من استخدام مضادات الميكروبات غير المنضبطة في الثروة الحيوانية والزراعة لحماية الصحة العامة.</p>
            </div>
        """, unsafe_allow_html=True)

# ================= TAB 1: خريطة العالم ومكتب فلسطين =================
with tab_world_map:
    st.subheader("🗺️ خريطة العالم ومتابعة المكاتب الإقليمية (Global Map & Palestine Office)")
    st.markdown("خريطة العالم التفاعلية لتوزيع العمليات الإدارية، مع إبراز العمل الإنساني والزراعي في **فلسطين الحبيبة**:")
    
    # خريطة العالم عادية غير متمركزة حصرياً، مع إدراج إحداثيات دولية وفلسطينية
    world_map_df = pd.DataFrame({
        'country': ['فلسطين', 'مصر (المكتب الإقليمي)', 'إيطاليا ( المقر الرئيسي بروما)', 'كينيا', تايلاند := 'تايلاند', 'الولايات المتحدة'],
        'lat': [31.9522, 30.0444, 41.9028, -1.2921, 13.7563, 38.8951],
        'lon': [35.2332, 31.2357, 12.4964, 36.8219, 100.5018, -77.0364],
        'status': ['نشط - دعم الصمود الزراعي', 'نشط - إقليمي', 'المقر الرئيسي للفاو', 'نشط - إفريقي', 'نشط - آسيوي', 'نشط - أمريكي']
    })
    
    st.map(world_map_df, latitude='lat', longitude='lon', size=60, color='#0076a8')
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
        <div class="fao-card" style="border-right-color: #dc2626;">
            <h4>🇵🇸 نشاط ومساهمات مكتب الفاو الإقليمي في فلسطين</h4>
            <p>• <b>دعم صمود المزارعين:</b> توفير البذور المعتمدة، الأسمدة، ومستلزمات الإنتاج الزراعي للتعاونيات المحلية.</p>
            <p>• <b>إعادة التأهيل:</b> إصلاح الآبار ومحطات المياه وشبكات الري المتضررة لضمان استمرار الأمن الغذائي المحلي.</p>
            <p>• <b>التنسيق الدولي:</b> إعداد التقارير الدورية حول حالة الأمن الغذائي في الأراضي الفلسطينية وتقديمها لمتخذي القرار في المقر الرئيسي بروما.</p>
        </div>
    """, unsafe_allow_html=True)

# ================= TAB 2: سجل التقارير والتدخلات =================
with tab_operations:
    st.subheader("📋 سجل التقارير والتدخلات الميدانية (FAO Operational Reports)")
    for rep in st.session_state.fao_reports:
        st.markdown(f"""
            <div class="fao-card">
                <h4>📄 مرجع التقرير: {rep['id']} | القسم: {rep['department']}</h4>
                <p><b>الإقليم المستهدف:</b> {rep['region']} | <b>تاريخ الإصدار:</b> {rep['date']}</p>
                <p>{rep['summary']}</p>
            </div>
        """, unsafe_allow_html=True)
        
    with st.form("add_fao_report_form"):
        st.markdown("#### ➕ إضافة تقرير إداري أو ميداني جديد:")
        rep_dept = st.selectbox("القسم المعني:", ["الأمن الغذائي العالمي", "مكتب فلسطين الإقليمي", "مركز الإنذار المبكر", "التنمية المستدامة"])
        rep_reg = st.text_input("الإقليم أو الدولة المستهدفة:")
        rep_sum = st.text_area("ملخص التقرير التنفيذي:")
        rep_btn = st.form_submit_button("إضافة التقرير للسجل الرسمي 🚀")
        
        if rep_btn and rep_reg and rep_sum:
            new_id = f"#FAO-REP-{str(uuid.uuid4())[:4].upper()}"
            st.session_state.fao_reports.append({
                "id": new_id,
                "department": rep_dept,
                "region": sanitize_input(rep_reg),
                "summary": sanitize_input(rep_sum),
                "date": str(datetime.now().date())
            })
            st.success(f"✨ تمت إضافة التقرير بنجاح برقم مرجعي {new_id}!")
            st.rerun()

# ================= TAB 3: لوحات التحليلات الاستراتيجية =================
with tab_bi_v17:
    st.subheader("📊 لوحات المؤشرات والتحليلات الاستراتيجية (Enterprise BI Dashboards)")
    fig_fao = px.bar(
        pd.DataFrame({'Department': ['الأمن الغذائي', 'الإنذار المبكر', 'التنمية المستدامة', 'مكتب فلسطين'], 'Efficiency': [96, 94, 98, 99]}),
        x='Department', y='Efficiency', color='Efficiency', color_continuous_scale='Teal'
    )
    st.plotly_chart(fig_fao, use_container_width=True)

# ================= TAB 4: لوحة التحكم وإدارة النظام =================
with tab_admin_control:
    st.subheader("⚙️ لوحة التحكم المركزي وإدارة المنظومة (Admin Control Center)")
    st.success("✅ كافة الأقسام الإدارية، الخريطة العالمية، ومكتب فلسطين تعمل بتناغم وتكامل مؤسسي تام.")

# --- التذييل الرسمي النهائي ---
st.markdown("""
    <div class="fao-footer">
        FAO Representation in Egypt & Palestine Regional Office | Global Enterprise System v17.0 <br>
        Engineered with Central FAO Management, Global World Map, and Palestine Office Integration by <b>Eng. Kareem Amr Mohamed</b>.
    </div>
""", unsafe_allow_html=True)