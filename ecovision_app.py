"""
EcoVision 2026 — Экологическое веб-приложение на Streamlit
Запуск: streamlit run ecovision_app.py
Зависимости: pip install streamlit pandas numpy requests streamlit-lottie
"""

import streamlit as st
import pandas as pd
import numpy as np
import requests
from streamlit_lottie import st_lottie  # pip install streamlit-lottie

# ─────────────────────────────────────────────
# КОНФИГУРАЦИЯ СТРАНИЦЫ
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="EcoVision 2026",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# КАСТОМНЫЕ CSS-СТИЛИ — тёмная тема + Eco Green
# ─────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Импорт шрифта ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    /* ── Глобальные переменные ── */
    :root {
        --eco-dark:      #0D1B0F;
        --eco-card:      #1A2E1C;
        --eco-border:    #2E7D32;
        --eco-green:     #2E7D32;
        --eco-light:     #81C784;
        --eco-text:      #E8F5E9;
        --eco-muted:     #A5D6A7;
        --eco-accent:    #66BB6A;
    }

    /* ── Фон приложения ── */
    .stApp {
        background: linear-gradient(135deg, #0D1B0F 0%, #102014 50%, #0A1A0C 100%);
        font-family: 'Inter', sans-serif;
        color: var(--eco-text);
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0F2211 0%, #1A2E1C 100%);
        border-right: 1px solid #2E7D32;
    }
    [data-testid="stSidebar"] * { color: var(--eco-text) !important; }

    /* ── Карточки ── */
    .eco-card {
        background: var(--eco-card);
        border: 1px solid var(--eco-border);
        border-radius: 15px;
        padding: 24px 28px;
        margin-bottom: 20px;
        box-shadow: 0 4px 24px rgba(46,125,50,0.15);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .eco-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 32px rgba(46,125,50,0.3);
    }

    /* ── Hero-заголовок ── */
    .hero-title {
        font-size: 3.2rem;
        font-weight: 700;
        background: linear-gradient(90deg, #81C784, #2E7D32, #66BB6A);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 6px;
        letter-spacing: -1px;
    }
    .hero-subtitle {
        text-align: center;
        color: var(--eco-muted);
        font-size: 1.1rem;
        font-weight: 300;
        margin-bottom: 32px;
    }

    /* ── Метрики ── */
    .metric-card {
        background: linear-gradient(135deg, #1A2E1C, #0F2211);
        border: 1px solid var(--eco-border);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
    }
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: var(--eco-light);
    }
    .metric-label {
        font-size: 0.85rem;
        color: var(--eco-muted);
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* ── Секция-разделитель ── */
    .section-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: var(--eco-light);
        border-left: 4px solid var(--eco-green);
        padding-left: 12px;
        margin: 32px 0 16px;
    }

    /* ── Слайдеры ── */
    .stSlider > div > div > div > div { background: var(--eco-green) !important; }

    /* ── Кнопки ── */
    .stButton > button {
        background: linear-gradient(90deg, #2E7D32, #43A047);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 28px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #43A047, #66BB6A);
        transform: scale(1.03);
        box-shadow: 0 4px 16px rgba(46,125,50,0.4);
    }

    /* ── Info/Success блоки ── */
    .stAlert {
        background: #1A2E1C !important;
        border-radius: 12px !important;
        border-left-color: var(--eco-green) !important;
        color: var(--eco-text) !important;
    }

    /* ── Таблицы / DataFrame ── */
    .dataframe { border-radius: 10px; overflow: hidden; }

    /* ── Прячем дефолтный footer Streamlit ── */
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ─────────────────────────────────────────────

def load_lottie_url(url: str):
    """Загружает Lottie-анимацию по URL; возвращает None при ошибке."""
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return None


def calculate_carbon_footprint(km_car: float, meat_kg: float, flights: int) -> dict:
    """
    Упрощённый расчёт углеродного следа (тонны CO₂/год).
    Коэффициенты усреднены по открытым источникам.
    """
    car_co2    = km_car * 0.21 / 1000      # 210 г CO₂/км → тонны
    meat_co2   = meat_kg * 27 / 1000       # ~27 кг CO₂ / кг говядины
    flight_co2 = flights * 0.9             # ~0.9 т CO₂ / перелёт
    total      = car_co2 + meat_co2 + flight_co2
    return {
        "🚗 Автомобиль": round(car_co2, 2),
        "🥩 Питание":    round(meat_co2, 2),
        "✈️ Авиа":       round(flight_co2, 2),
        "total":         round(total, 2),
    }


def generate_co2_data() -> pd.DataFrame:
    """Генерирует фейковые данные снижения выбросов CO₂ (2015–2025)."""
    years = list(range(2015, 2026))
    np.random.seed(42)
    base = 52.0  # Гт CO₂ в 2015
    reductions = np.cumsum(np.random.uniform(0.3, 1.1, len(years)))
    noise      = np.random.normal(0, 0.2, len(years))
    co2        = np.clip(base - reductions + noise, 40, 55)
    target     = np.linspace(52, 26, len(years))  # линия цели
    return pd.DataFrame({"Год": years, "Факт (Гт CO₂)": co2.round(2), "Цель (Гт CO₂)": target.round(2)})


ECO_TIPS = [
    ("🌱", "Замените один мясной приём пищи в день растительным — это экономит ~2 кг CO₂ ежедневно."),
    ("💧", "Закрывайте кран во время чистки зубов: так вы сохраняете до 12 литров воды в минуту."),
    ("🚲", "Велосипед вместо авто на короткие поездки — 0 г CO₂ и польза для здоровья."),
    ("♻️", "Раздельный сбор мусора сокращает объём свалок и снижает выбросы метана."),
    ("🌳", "Посадите хотя бы одно дерево в год — за 40 лет оно поглотит ~1 т CO₂."),
    ("💡", "Светодиодные лампы потребляют на 75% меньше энергии, чем лампы накаливания."),
]


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌿 EcoVision 2026")
    st.markdown("---")

    page = st.radio(
        "Навигация",
        ["🏠 Главная", "📊 CO₂ Тренды", "🧮 Калькулятор", "💚 Eco Tips"],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("### 🤝 Поддержи планету")
    st.markdown("""
    <div class="eco-card" style="padding:16px;">
        <p style="color:#A5D6A7; font-size:0.9rem; margin:0;">
        Стань волонтёром или помоги финансово — каждое действие важно.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.link_button("💸 Задонатить", "https://www.wwf.org", use_container_width=True)
    st.link_button("🙋 Стать волонтёром", "https://www.greenpeace.org", use_container_width=True)

    st.markdown("---")
    st.caption("© 2026 EcoVision · Made with 💚")


# ─────────────────────────────────────────────
# HERO-СЕКЦИЯ
# ─────────────────────────────────────────────
st.markdown('<h1 class="hero-title">🌿 EcoVision 2026</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="hero-subtitle">Отслеживай. Считай. Действуй. Спасай планету вместе с нами.</p>',
    unsafe_allow_html=True,
)

# Lottie-анимация (дерево/экология)
lottie_tree = load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_tpa7u0bo.json")
if lottie_tree:
    col_l, col_anim, col_r = st.columns([2, 1, 2])
    with col_anim:
        st_lottie(lottie_tree, height=180, key="tree_hero")
else:
    st.markdown("<p style='text-align:center;font-size:5rem;'>🌳</p>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# KPI-МЕТРИКИ (всегда видны)
# ─────────────────────────────────────────────
st.markdown('<p class="section-title">Глобальный прогресс</p>', unsafe_allow_html=True)
m1, m2, m3, m4 = st.columns(4)
kpis = [
    ("−18%", "Выбросы CO₂ vs 2015"),
    ("4.1 Гт", "Поглощено лесами (2025)"),
    ("42%", "Доля ВИЭ в электроэнергии"),
    ("1.2M+", "Активных эко-волонтёров"),
]
for col, (val, label) in zip([m1, m2, m3, m4], kpis):
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{val}</div>
            <div class="metric-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# СТРАНИЦА: CO₂ ТРЕНДЫ
# ─────────────────────────────────────────────
if "📊 CO₂ Тренды" in page or "🏠 Главная" in page:
    st.markdown('<p class="section-title">📊 Тренды выбросов CO₂ (2015–2025)</p>', unsafe_allow_html=True)

    df_co2 = generate_co2_data()

    st.markdown('<div class="eco-card">', unsafe_allow_html=True)
    st.area_chart(
        df_co2.set_index("Год"),
        color=["#81C784", "#2E7D32"],
        height=320,
        use_container_width=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

    with st.expander("📋 Посмотреть таблицу данных"):
        st.dataframe(df_co2, use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────
# СТРАНИЦА: КАЛЬКУЛЯТОР УГЛЕРОДНОГО СЛЕДА
# ─────────────────────────────────────────────
if "🧮 Калькулятор" in page or "🏠 Главная" in page:
    st.markdown('<p class="section-title">🧮 Калькулятор углеродного следа</p>', unsafe_allow_html=True)

    st.markdown('<div class="eco-card">', unsafe_allow_html=True)

    col_sliders, col_result = st.columns([3, 2], gap="large")

    with col_sliders:
        st.markdown("**Введи свои данные за год:**")
        km_car = st.slider(
            "🚗 Километров на автомобиле", 0, 50_000, 12_000, step=500,
            help="Средний пробег по России ~15 000 км/год",
        )
        meat_kg = st.slider(
            "🥩 Потребление мяса (кг)", 0, 200, 60, step=5,
            help="Средний россиянин ест ~75 кг мяса/год",
        )
        flights = st.slider(
            "✈️ Авиаперелётов (туда-обратно)", 0, 20, 2,
            help="Один перелёт Москва–Сочи ≈ 0.3 т CO₂",
        )

    with col_result:
        result = calculate_carbon_footprint(km_car, meat_kg, flights)
        total  = result.pop("total")

        st.markdown(f"""
        <div style="text-align:center; padding: 16px 0;">
            <div style="font-size:0.9rem; color:#A5D6A7; text-transform:uppercase; letter-spacing:1px;">
                Твой след
            </div>
            <div style="font-size:3.5rem; font-weight:700; color:#81C784; line-height:1.1;">
                {total}
            </div>
            <div style="font-size:1rem; color:#A5D6A7;">тонн CO₂ / год</div>
        </div>
        """, unsafe_allow_html=True)

        # Сравнение со средним
        avg_world = 4.7
        delta_pct = round((total - avg_world) / avg_world * 100, 1)
        sign      = "+" if delta_pct > 0 else ""
        color     = "#ef5350" if delta_pct > 0 else "#66BB6A"
        st.markdown(f"""
        <p style="text-align:center; color:{color}; font-size:0.95rem;">
            {sign}{delta_pct}% к среднемировому показателю ({avg_world} т)
        </p>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Breakdown-диаграмма
    st.markdown('<p class="section-title" style="font-size:1.1rem;">Разбивка по источникам</p>',
                unsafe_allow_html=True)
    df_breakdown = pd.DataFrame({"Источник": list(result.keys()), "CO₂ (т)": list(result.values())})
    st.bar_chart(df_breakdown.set_index("Источник"), color="#81C784", height=240)


# ─────────────────────────────────────────────
# СТРАНИЦА: ECO TIPS
# ─────────────────────────────────────────────
if "💚 Eco Tips" in page or "🏠 Главная" in page:
    st.markdown('<p class="section-title">💚 Daily Eco Tips</p>', unsafe_allow_html=True)

    # Lottie для секции советов
    lottie_eco = load_lottie_url("https://assets3.lottiefiles.com/packages/lf20_ystsffqy.json")

    tip_col, anim_col = st.columns([3, 1])

    with tip_col:
        for i, (icon, tip) in enumerate(ECO_TIPS):
            if i % 2 == 0:
                st.success(f"{icon} {tip}")
            else:
                st.info(f"{icon} {tip}")

    with anim_col:
        if lottie_eco:
            st_lottie(lottie_eco, height=300, key="eco_tips_anim")
        else:
            st.markdown("<p style='font-size:4rem; text-align:center;'>♻️</p>", unsafe_allow_html=True)

    # Прогресс-бар "Personal Eco Score"
    st.markdown('<p class="section-title" style="font-size:1.1rem;">🌡️ Personal Eco Score</p>',
                unsafe_allow_html=True)
    score = st.slider("Оцени свою экологичность за эту неделю", 0, 100, 65, format="%d%%")
    color_score = "#66BB6A" if score >= 60 else "#FFA726" if score >= 30 else "#ef5350"
    label_score = "Отлично! Ты настоящий эко-герой 🌟" if score >= 75 \
        else "Хороший прогресс! Продолжай в том же духе 💪" if score >= 50 \
        else "Есть куда расти — маленькие шаги меняют мир 🌱"
    st.markdown(f"""
    <div class="eco-card" style="text-align:center;">
        <div style="font-size:2.5rem; font-weight:700; color:{color_score};">{score}%</div>
        <div style="color:#A5D6A7; margin-top:8px;">{label_score}</div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<p style="text-align:center; color:#4CAF50; font-size:0.85rem; padding:8px 0;">
    🌿 EcoVision 2026 · Каждое действие важно · Сделано с любовью к планете
</p>
""", unsafe_allow_html=True)
