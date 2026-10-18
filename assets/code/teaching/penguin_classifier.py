
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
import json
import os
from datetime import datetime
import hashlib

from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix, roc_curve, auc,
    roc_auc_score, log_loss
)
from sklearn.pipeline import Pipeline

# ============================================
# ۱. تنظیمات صفحه
# ============================================

st.set_page_config(
    page_title="🐧 سیستم شناسایی پنگوئن | Palmer Station",
    page_icon="🐧",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/streamlit/streamlit',
        'Report a bug': 'https://github.com/streamlit/streamlit/issues',
        'About': "# پنگوئن کلاسیفایر\nاین اپلیکیشن برای شناسایی گونه پنگوئن طراحی شده است."
    }
)

# ============================================
# ۲. استایل CSS سفارشی
# ============================================

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #E3F2FD, #BBDEFB);
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .prediction-box {
        background-color: #e8f5e9;
        padding: 2rem;
        border-radius: 15px;
        border-left: 5px solid #4CAF50;
        margin: 1rem 0;
    }
    .stButton>button {
        background-color: #1E88E5;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 0.5rem 2rem;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #1565C0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# ۳. توابع کمکی
# ============================================

def generate_session_id():
    """تولید شناسه یکتا برای هر سشن"""
    return hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8]

@st.cache_data(ttl=3600, show_spinner="🔄 در حال بارگذاری داده‌های پنگوئن...")
def load_penguin_data():
    """بارگذاری و پیش‌پردازش دیتاست پنگوئن"""
    try:
        df = sns.load_dataset("penguins")
        original_len = len(df)
        df = df.dropna()
        dropped = original_len - len(df)
        
        df["species_code"] = df["species"].astype('category').cat.codes
        df["island_code"] = df["island"].astype('category').cat.codes
        df["sex_code"] = df["sex"].astype('category').cat.codes
        
        df.attrs['loaded_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        df.attrs['source'] = "Palmer Station Antarctica"
        df.attrs['dropped_rows'] = dropped
        
        return df
    except Exception as e:
        st.error(f"❌ خطا در بارگذاری داده‌ها: {str(e)}")
        return None

@st.cache_resource(show_spinner="🔄 در حال ایجاد پایپلاین آموزش...")
def create_pipeline(algorithm, params=None):
    """ایجاد پایپلاین یادگیری ماشین"""
    
    # مرحله ۱: استانداردسازی
    scaler = StandardScaler()
    
    # مرحله ۲: انتخاب الگوریتم
    if algorithm == "رگرسیون لجستیک":
        classifier = LogisticRegression(random_state=42, max_iter=1000)
        param_grid = {
            'classifier__C': [0.01, 0.1, 1, 10],
            'classifier__solver': ['lbfgs', 'liblinear']
        }
    elif algorithm == "جنگل تصادفی":
        classifier = RandomForestClassifier(random_state=42)
        param_grid = {
            'classifier__n_estimators': [50, 100, 200],
            'classifier__max_depth': [5, 10, None],
            'classifier__min_samples_split': [2, 5, 10]
        }
    elif algorithm == "SVM":
        classifier = SVC(random_state=42, probability=True)
        param_grid = {
            'classifier__C': [0.1, 1, 10],
            'classifier__kernel': ['rbf', 'poly'],
            'classifier__gamma': ['scale', 'auto']
        }
    elif algorithm == "گرادیان بوستینگ":
        classifier = GradientBoostingClassifier(random_state=42)
        param_grid = {
            'classifier__n_estimators': [50, 100],
            'classifier__learning_rate': [0.01, 0.1, 0.2],
            'classifier__max_depth': [3, 5]
        }
    else:  # KNN
        classifier = KNeighborsClassifier()
        param_grid = {
            'classifier__n_neighbors': [3, 5, 7, 9],
            'classifier__weights': ['uniform', 'distance']
        }
    
    # ساخت پایپلاین
    pipeline = Pipeline([
        ('scaler', scaler),
        ('classifier', classifier)
    ])
    
    return pipeline, param_grid if params is None else None

@st.cache_data(ttl=300)
def train_and_evaluate(X_train, X_test, y_train, y_test, algorithm, use_grid_search=False):
    """آموزش و ارزیابی مدل"""
    
    pipeline, param_grid = create_pipeline(algorithm)
    
    if use_grid_search and param_grid:
        grid_search = GridSearchCV(
            pipeline, 
            param_grid, 
            cv=5, 
            scoring='accuracy',
            n_jobs=-1,
            verbose=0
        )
        grid_search.fit(X_train, y_train)
        best_model = grid_search.best_estimator_
        best_params = grid_search.best_params_
    else:
        pipeline.fit(X_train, y_train)
        best_model = pipeline
        best_params = None
    
    # پیش‌بینی
    y_pred = best_model.predict(X_test)
    y_proba = best_model.predict_proba(X_test) if hasattr(best_model, 'predict_proba') else None
    
    # محاسبه معیارها
    metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision_macro': precision_score(y_test, y_pred, average='macro'),
        'recall_macro': recall_score(y_test, y_pred, average='macro'),
        'f1_macro': f1_score(y_test, y_pred, average='macro'),
        'precision_weighted': precision_score(y_test, y_pred, average='weighted'),
        'recall_weighted': recall_score(y_test, y_pred, average='weighted'),
        'f1_weighted': f1_score(y_test, y_pred, average='weighted')
    }
    
    if y_proba is not None:
        try:
            metrics['log_loss'] = log_loss(y_test, y_proba)
            metrics['roc_auc'] = roc_auc_score(y_test, y_proba, multi_class='ovr')
        except:
            pass
    
    return best_model, metrics, y_pred, y_proba, best_params

# ============================================
# ۴. مقداردهی اولیه Session State
# ============================================

def init_session_state():
    """مقداردهی اولیه Session State"""
    
    defaults = {
        'session_id': generate_session_id(),
        'model': None,
        'scaler': None,
        'features': [],
        'metrics': {},
        'training_history': [],
        'predictions': [],
        'selected_features': ['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g'],
        'algorithm': 'رگرسیون لجستیک',
        'test_size': 0.2,
        'use_grid_search': False,
        'dark_mode': False,
        'show_code': False
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# ============================================
# ۵. بارگذاری داده
# ============================================

df = load_penguin_data()

if df is None:
    st.error("❌ خطا در بارگذاری داده‌ها. لطفا برنامه را مجدداً اجرا کنید.")
    st.stop()

# ============================================
# ۶. عنوان اصلی
# ============================================

st.markdown('<h1 class="main-header">🐧 سیستم هوشمند شناسایی گونه پنگوئن - ایستگاه پالمر</h1>', 
            unsafe_allow_html=True)

st.markdown("""
<div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin-bottom: 30px;'>
    <h4>🎯 درباره اپلیکیشن</h4>
    <p>
        این سیستم با استفاده از الگوریتم‌های یادگیری ماشین، گونه پنگوئن را بر اساس 
        ویژگی‌های فیزیکی شناسایی می‌کند. داده‌ها از ایستگاه تحقیقاتی Palmer در قطب جنوب 
        جمع‌آوری شده‌اند.
    </p>
    <p>
        <b>شناسه سشن:</b> {} | <b>آخرین بروزرسانی:</b> {}
    </p>
</div>
""".format(st.session_state.session_id, df.attrs['loaded_at']), unsafe_allow_html=True)

# ============================================
# ۷. سایدبار - تنظیمات کامل
# ============================================

with st.sidebar:
    st.image("https://allisonhorst.github.io/palmerpenguins/reference/figures/lter_penguins.png", 
             use_container_width=True)
    
    st.header("⚙️ پنل فرمان")
    
    with st.expander("📊 انتخاب ویژگی‌ها", expanded=True):
        all_features = ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]
        selected_features = st.multiselect(
            "ویژگی‌های ورودی:",
            all_features,
            default=st.session_state.selected_features,
            help="ویژگی‌های فیزیکی برای آموزش مدل"
        )
        st.session_state.selected_features = selected_features
    
    with st.expander("🤖 تنظیمات مدل", expanded=True):
        algorithm = st.selectbox(
            "الگوریتم یادگیری:",
            ["رگرسیون لجستیک", "جنگل تصادفی", "SVM", "گرادیان بوستینگ", "KNN"],
            index=["رگرسیون لجستیک", "جنگل تصادفی", "SVM", "گرادیان بوستینگ", "KNN"].index(
                st.session_state.algorithm
            ),
            help="انتخاب الگوریتم مناسب برای طبقه‌بندی"
        )
        st.session_state.algorithm = algorithm
        
        test_size = st.slider(
            "درصد داده تست:",
            min_value=0.1, max_value=0.4, value=st.session_state.test_size, step=0.05,
            format="%d%%",
            help="درصد داده برای ارزیابی مدل"
        )
        st.session_state.test_size = test_size
        
        use_grid_search = st.checkbox(
            "🔍 بهینه‌سازی خودکار (Grid Search)",
            value=st.session_state.use_grid_search,
            help="جستجوی خودکار بهترین پارامترها"
        )
        st.session_state.use_grid_search = use_grid_search
    
    with st.expander("🎨 تنظیمات ظاهری"):
        dark_mode = st.checkbox("🌙 حالت تاریک", value=st.session_state.dark_mode)
        st.session_state.dark_mode = dark_mode
        show_code = st.checkbox("📝 نمایش کد", value=st.session_state.show_code)
        st.session_state.show_code = show_code
    
    st.divider()
    
    # دکمه آموزش
    train_button = st.button(
        "🚀 شروع آموزش مدل",
        type="primary",
        use_container_width=True,
        disabled=len(selected_features) < 2
    )
    
    if len(selected_features) < 2:
        st.warning("⚠️ حداقل ۲ ویژگی انتخاب کنید")
    
    st.divider()
    
    # آمار کلی
    st.subheader("📊 آمار داده‌ها")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("تعداد نمونه", f"{len(df):,}")
        st.metric("ویژگی‌ها", df.shape[1] - 4)
    with col2:
        st.metric("گونه‌ها", df['species'].nunique())
        st.metric("جزایر", df['island'].nunique())
    
    if df.attrs['dropped_rows'] > 0:
        st.caption(f"⚠️ {df.attrs['dropped_rows']} نمونه گمشده حذف شد")
    
    st.divider()
    st.caption("🐧 Palmer Penguins v1.0.0")
    st.caption(f"© 2026 - Antarctic Research")

# ============================================
# ۸. نمایش داده‌ها و تحلیل اکتشافی
# ============================================

tab1, tab2, tab3, tab4 = st.tabs(
    ["📋 داده‌ها و آمار", "📈 مصورسازی", "🤖 آموزش و ارزیابی", "🔮 پیش‌بینی تعاملی"]
)

with tab1:
    st.header("📋 بررسی و تحلیل داده‌ها")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("نمونه داده‌ها")
        display_cols = ["species", "island", "sex"] + selected_features
        st.dataframe(
            df[display_cols].head(10),
            use_container_width=True,
            hide_index=True,
            column_config={
                "species": "گونه",
                "island": "جزیره",
                "sex": "جنسیت",
                "bill_length_mm": st.column_config.NumberColumn("طول نوک", format="%.1f mm"),
                "bill_depth_mm": st.column_config.NumberColumn("عمق نوک", format="%.1f mm"),
                "flipper_length_mm": st.column_config.NumberColumn("طول بالچه", format="%.0f mm"),
                "body_mass_g": st.column_config.NumberColumn("وزن", format="%.0f g")
            }
        )
    
    with col2:
        st.subheader("اطلاعات دیتاست")
        info_df = pd.DataFrame({
            "مشخصه": ["منبع", "تاریخ بارگذاری", "تعداد رکوردها", "تعداد ویژگی‌ها"],
            "مقدار": [
                df.attrs['source'],
                df.attrs['loaded_at'],
                len(df),
                df.shape[1]
            ]
        })
        st.dataframe(info_df, use_container_width=True, hide_index=True)
    
    st.subheader("📊 آمار توصیفی")
    
    stat_col1, stat_col2 = st.columns(2)
    
    with stat_col1:
        st.markdown("**ویژگی‌های عددی**")
        stats_df = df[selected_features].describe().round(2)
        st.dataframe(stats_df, use_container_width=True)
    
    with stat_col2:
        st.markdown("**توزیع گونه‌ها**")
        species_counts = df['species'].value_counts().reset_index()
        species_counts.columns = ['گونه', 'تعداد']
        
        fig = px.pie(
            species_counts,
            values='تعداد',
            names='گونه',
            title="توزیع گونه‌های پنگوئن",
            color_discrete_sequence=px.colors.qualitative.Set2,
            hole=0.4
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("📈 مصورسازی تعاملی داده‌ها")
    
    viz_col1, viz_col2 = st.columns([1, 3])
    
    with viz_col1:
        st.subheader("تنظیمات نمودار")
        
        plot_type = st.radio(
            "نوع نمودار:",
            ["پراکندگی", "هیستوگرام", "جعبه‌ای", "جفتی"],
            horizontal=False
        )
        
        if plot_type == "پراکندگی":
            x_axis = st.selectbox("محور X:", selected_features, index=0)
            y_axis = st.selectbox("محور Y:", selected_features, index=1 if len(selected_features) > 1 else 0)
            color_by = st.selectbox("رنگ‌بندی:", ["species", "island", "sex"], index=0)
            
        elif plot_type == "هیستوگرام":
            feature = st.selectbox("ویژگی:", selected_features, index=0)
            bins = st.slider("تعداد دسته‌ها:", 10, 50, 30)
            
        elif plot_type == "جعبه‌ای":
            feature = st.selectbox("ویژگی:", selected_features, index=0)
            group_by = st.selectbox("دسته‌بندی:", ["species", "island", "sex"], index=0)
    
    with viz_col2:
        if plot_type == "پراکندگی":
            fig = px.scatter(
                df,
                x=x_axis,
                y=y_axis,
                color=color_by,
                size="body_mass_g" if "body_mass_g" in df.columns else None,
                hover_data=['species', 'island'],
                title=f"{x_axis} vs {y_axis}",
                opacity=0.7,
                color_discrete_sequence=px.colors.qualitative.Set1
            )
            st.plotly_chart(fig, use_container_width=True)
            
        elif plot_type == "هیستوگرام":
            fig = px.histogram(
                df,
                x=feature,
                color="species",
                nbins=bins,
                marginal="box",
                title=f"توزیع {feature}",
                barmode="overlay",
                opacity=0.7
            )
            st.plotly_chart(fig, use_container_width=True)
            
        elif plot_type == "جعبه‌ای":
            fig = px.box(
                df,
                x=group_by,
                y=feature,
                color=group_by,
                title=f"توزیع {feature} بر اساس {group_by}",
                points="all"
            )
            st.plotly_chart(fig, use_container_width=True)
            
        elif plot_type == "جفتی":
            fig = px.scatter_matrix(
                df,
                dimensions=selected_features,
                color="species",
                title="نمودار جفتی ویژگی‌ها",
                opacity=0.7
            )
            fig.update_traces(diagonal_visible=False)
            st.plotly_chart(fig, use_container_width=True)

# ============================================
# ۹. آموزش و ارزیابی مدل
# ============================================

with tab3:
    st.header("🤖 آموزش و ارزیابی مدل")
    
    if train_button and len(selected_features) >= 2:
        with st.status("🔄 در حال آموزش مدل...", expanded=True) as status:
            
            # آماده‌سازی داده
            st.write("📊 آماده‌سازی داده‌ها...")
            X = df[selected_features]
            y = df["species_code"]
            
            # تقسیم داده
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=42, stratify=y
            )
            
            st.write(f"📈 اندازه مجموعه آموزش: {len(X_train)} نمونه")
            st.write(f"📉 اندازه مجموعه تست: {len(X_test)} نمونه")
            
            # آموزش مدل
            st.write(f"🤖 در حال آموزش با الگوریتم {algorithm}...")
            start_time = time.time()
            
            model, metrics, y_pred, y_proba, best_params = train_and_evaluate(
                X_train, X_test, y_train, y_test, algorithm, use_grid_search
            )
            
            training_time = time.time() - start_time
            
            # ذخیره در session state
            st.session_state.model = model
            st.session_state.metrics = metrics
            st.session_state.training_time = training_time
            st.session_state.best_params = best_params
            
            status.update(label="✅ آموزش مدل با موفقیت انجام شد!", state="complete")
        
        # ============================================
        # ۱۰. نمایش نتایج ارزیابی
        # ============================================
        
        st.subheader("📊 نتایج ارزیابی مدل")
        
        # متریک‌های اصلی
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "🎯 دقت (Accuracy)",
                f"{metrics['accuracy']:.2%}",
                help="درصد پیش‌بینی‌های صحیح"
            )
        with col2:
            st.metric(
                "📊 دقت میانگین (Precision)",
                f"{metrics['precision_macro']:.2%}",
                help="میانگین دقت برای همه کلاس‌ها"
            )
        with col3:
            st.metric(
                "🎯 یادآوری (Recall)",
                f"{metrics['recall_macro']:.2%}",
                help="میانگین حساسیت برای همه کلاس‌ها"
            )
        with col4:
            st.metric(
                "📈 F1-Score",
                f"{metrics['f1_macro']:.2%}",
                help="هارمونیک میانگین دقت و یادآوری"
            )
        
        # زمان آموزش و پارامترها
        col1, col2 = st.columns(2)
        with col1:
            st.metric("⏱️ زمان آموزش", f"{training_time:.2f} ثانیه")
        with col2:
            if best_params:
                st.metric("🔧 بهترین پارامترها", str(best_params))
        
        # گزارش طبقه‌بندی
        st.subheader("📋 گزارش کامل طبقه‌بندی")
        
        target_names = ['Adelie', 'Chinstrap', 'Gentoo']
        report_dict = classification_report(
            y_test, y_pred, 
            target_names=target_names,
            output_dict=True
        )
        report_df = pd.DataFrame(report_dict).transpose()
        
        # استایل دادن به گزارش
        styled_df = report_df.style.format({
            'precision': '{:.2%}',
            'recall': '{:.2%}',
            'f1-score': '{:.2%}',
            'support': '{:.0f}'
        }).highlight_max(axis=0, color='lightgreen')
        
        st.dataframe(styled_df, use_container_width=True)
        
        # ماتریس درهم‌ریختگی
        st.subheader("🎯 ماتریس درهم‌ریختگی")
        
        cm = confusion_matrix(y_test, y_pred)
        
        fig = px.imshow(
            cm,
            x=target_names,
            y=target_names,
            text_auto=True,
            aspect="auto",
            color_continuous_scale="Blues",
            title="Confusion Matrix - ماتریس درهم‌ریختگی"
        )
        
        fig.update_layout(
            xaxis_title="پیش‌بینی شده",
            yaxis_title="واقعی",
            width=500,
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # اعتبارسنجی متقابل
        st.subheader("🔄 اعتبارسنجی متقابل (Cross-Validation)")
        
        with st.spinner("در حال انجام اعتبارسنجی متقابل..."):
            from sklearn.model_selection import cross_val_score, StratifiedKFold
            
            cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
            cv_scores = cross_val_score(model, X, y, cv=cv, scoring='accuracy')
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("میانگین دقت CV", f"{cv_scores.mean():.2%}")
            with col2:
                st.metric("انحراف معیار", f"{cv_scores.std():.2%}")
            with col3:
                st.metric("بازه اطمینان", f"{cv_scores.mean() - 2*cv_scores.std():.2%} - {cv_scores.mean() + 2*cv_scores.std():.2%}")
            
            # نمودار امتیازات CV
            fig = px.line(
                x=range(1, 6),
                y=cv_scores,
                markers=True,
                title="امتیازات اعتبارسنجی متقابل",
                labels={"x": "فولد", "y": "دقت"}
            )
            fig.add_hline(y=cv_scores.mean(), line_dash="dash", line_color="red")
            st.plotly_chart(fig, use_container_width=True)
        
        # ذخیره تاریخچه آموزش
        st.session_state.training_history.append({
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'algorithm': algorithm,
            'features': selected_features,
            'test_size': test_size,
            'accuracy': metrics['accuracy'],
            'f1_score': metrics['f1_macro'],
            'training_time': training_time
        })
        
    else:
        st.info("👈 برای شروع آموزش، از پنل سمت راست ویژگی‌ها را انتخاب کرده و دکمه 'شروع آموزش مدل' را کلیک کنید.")
        
        if st.session_state.model is not None:
            st.success("✅ مدل قبلی依然 در حافظه موجود است. می‌توانید از آن برای پیش‌بینی استفاده کنید.")
            
            # نمایش آخرین مدل آموزش داده شده
            st.subheader("📊 آخرین مدل آموزش داده شده")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("الگوریتم", st.session_state.algorithm)
                st.metric("دقت", f"{st.session_state.metrics.get('accuracy', 0):.2%}")
            with col2:
                st.metric("زمان آموزش", f"{st.session_state.get('training_time', 0):.2f} ثانیه")
                if 'best_params' in st.session_state and st.session_state.best_params:
                    st.metric("پارامترها", str(st.session_state.best_params))

# ============================================
# ۱۱. پیش‌بینی تعاملی
# ============================================

with tab4:
    st.header("🔮 پیش‌بینی تعاملی گونه پنگوئن")
    
    if st.session_state.model is not None:
        
        st.markdown("""
        <div class="prediction-box">
            <h4>📝 وارد کردن ویژگی‌های پنگوئن</h4>
            <p>مقادیر را در محدوده مشخص شده وارد کنید تا سیستم گونه را پیش‌بینی کند.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📏 ویژگی‌های نوک**")
            bill_length = st.number_input(
                "طول نوک (میلی‌متر):",
                min_value=30.0, max_value=60.0, value=45.0, step=0.1,
                format="%.1f",
                help="محدوده: ۳۰ - ۶۰ میلی‌متر"
            )
            
            bill_depth = st.number_input(
                "عمق نوک (میلی‌متر):",
                min_value=13.0, max_value=22.0, value=17.0, step=0.1,
                format="%.1f",
                help="محدوده: ۱۳ - ۲۲ میلی‌متر"
            )
        
        with col2:
            st.markdown("**🦩 ویژگی‌های بدن**")
            flipper_length = st.number_input(
                "طول بالچه (میلی‌متر):",
                min_value=170.0, max_value=240.0, value=200.0, step=1.0,
                format="%.0f",
                help="محدوده: ۱۷۰ - ۲۴۰ میلی‌متر"
            )
            
            body_mass = st.number_input(
                "وزن (گرم):",
                min_value=2500.0, max_value=6500.0, value=4200.0, step=50.0,
                format="%.0f",
                help="محدوده: ۲۵۰۰ - ۶۵۰۰ گرم"
            )
        
        # اضافه کردن جنسیت
        sex = st.selectbox(
            "جنسیت:",
            options=["Male", "Female"],
            index=0,
            help="انتخاب جنسیت پنگوئن"
        )
        sex_code = 0 if sex == "Male" else 1
        
        # دکمه پیش‌بینی
        predict_button = st.button(
            "🎯 پیش‌بینی گونه",
            type="primary",
            use_container_width=True
        )
        
        if predict_button:
            # آماده‌سازی داده ورودی
            input_data = {}
            for i, feature in enumerate(st.session_state.selected_features):
                if feature == "bill_length_mm":
                    input_data[feature] = [bill_length]
                elif feature == "bill_depth_mm":
                    input_data[feature] = [bill_depth]
                elif feature == "flipper_length_mm":
                    input_data[feature] = [flipper_length]
                elif feature == "body_mass_g":
                    input_data[feature] = [body_mass]
            
            # اگر ویژگی جنسیت انتخاب شده بود
            if "sex_code" in st.session_state.selected_features:
                input_data["sex_code"] = [sex_code]
            
            input_df = pd.DataFrame(input_data)
            
            # اطمینان از ترتیب صحیح ستون‌ها
            input_df = input_df[st.session_state.selected_features]
            
            try:
                # پیش‌بینی
                prediction = st.session_state.model.predict(input_df)[0]
                
                # احتمال (اگر مدل از predict_proba پشتیبانی کند)
                if hasattr(st.session_state.model, 'predict_proba'):
                    probabilities = st.session_state.model.predict_proba(input_df)[0]
                else:
                    probabilities = None
                
                # نگاشت کد به نام گونه
                species_map = {0: 'Adelie', 1: 'Chinstrap', 2: 'Gentoo'}
                predicted_species = species_map[prediction]
                
                # نمایش نتیجه
                st.markdown("---")
                
                result_col1, result_col2 = st.columns([1, 1])
                
                with result_col1:
                    st.markdown(f"""
                    <div style='background-color: #4CAF50; padding: 30px; border-radius: 15px; text-align: center;'>
                        <h2 style='color: white; margin: 0;'>🐧 {predicted_species}</h2>
                        <p style='color: white; font-size: 20px; margin-top: 10px;'>گونه پیش‌بینی شده</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with result_col2:
                    if probabilities is not None:
                        st.subheader("📊 احتمال تعلق به هر گونه")
                        
                        prob_df = pd.DataFrame({
                            'گونه': ['Adelie', 'Chinstrap', 'Gentoo'],
                            'احتمال': probabilities
                        })
                        
                        fig = px.bar(
                            prob_df,
                            x='گونه',
                            y='احتمال',
                            color='گونه',
                            text_auto='.2%',
                            title="احتمال پیش‌بینی",
                            color_discrete_map={
                                'Adelie': '#1f77b4',
                                'Chinstrap': '#ff7f0e',
                                'Gentoo': '#2ca02c'
                            }
                        )
                        fig.update_layout(showlegend=False)
                        st.plotly_chart(fig, use_container_width=True)
                
                # اضافه کردن به تاریخچه پیش‌بینی
                st.session_state.predictions.append({
                    'timestamp': datetime.now().strftime("%H:%M:%S"),
                    'bill_length': bill_length,
                    'bill_depth': bill_depth,
                    'flipper_length': flipper_length,
                    'body_mass': body_mass,
                    'sex': sex,
                    'prediction': predicted_species,
                    'probabilities': probabilities.tolist() if probabilities is not None else None
                })
                
                st.balloons()
                
            except Exception as e:
                st.error(f"❌ خطا در پیش‌بینی: {str(e)}")
                st.info("💡 لطفا مطمئن شوید که مدل با همین ویژگی‌ها آموزش دیده است.")
    
    else:
        st.warning("⚠️ ابتدا باید یک مدل را آموزش دهید!")
        st.info("👈 به تب 'آموزش و ارزیابی' بروید و یک مدل را آموزش دهید.")
    
    # نمایش تاریخچه پیش‌بینی
    if len(st.session_state.predictions) > 0:
        st.markdown("---")
        st.subheader("📋 تاریخچه پیش‌بینی‌ها")
        
        history_df = pd.DataFrame(st.session_state.predictions[-10:])  # آخرین ۱۰ پیش‌بینی
        st.dataframe(history_df, use_container_width=True, hide_index=True)

# ============================================
# ۱۲. نمایش کد (اختیاری)
# ============================================

if st.session_state.show_code:
    st.markdown("---")
    st.header("📝 کد منبع اپلیکیشن")
    
    with st.expander("نمایش کد کامل", expanded=False):
        with open(__file__, 'r', encoding='utf-8') as f:
            code = f.read()
        st.code(code, language='python')

# ============================================
# ۱۳. فوتر
# ============================================

st.markdown("---")
st.markdown(f"""
<div style='text-align: center; color: gray; padding: 20px;'>
    <p>🐧 Palmer Penguins Classifier | توسعه داده شده با Streamlit و ❤️</p>
    <p>شناسه سشن: {st.session_state.session_id} | تاریخ: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
    <p style='font-size: 0.8em;'>© 2026 Antarctic Research Program - All Rights Reserved</p>
</div>
""", unsafe_allow_html=True)