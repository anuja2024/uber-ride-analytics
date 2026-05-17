def load_css():
    return """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0a0a0f;
    color: #e0e4f0;
}
.stApp { background-color: #0a0a0f; }
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 2rem 2rem 2rem 2rem;
    max-width: 1400px;
}
[data-testid="stSidebar"] {
    background: #0d0d14 !important;
    border-right: 1px solid #1a1a2e;
}
.kpi-card {
    background: linear-gradient(135deg, #12131f, #0e0f1a);
    border: 1px solid #1e2040;
    border-radius: 16px;
    padding: 1.4rem 1rem;
    text-align: center;
    transition: all 0.3s ease;
    cursor: default;
    height: 100%;
}
.kpi-card:hover {
    transform: translateY(-5px);
    border-color: #2a3060;
    box-shadow: 0 8px 30px rgba(0,212,170,0.12);
}
.kpi-label {
    font-size: 10px;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #6b7399;
    margin-bottom: 8px;
    font-weight: 500;
}
.kpi-value {
    font-size: 20px;
    font-weight: 700;
    color: #ffffff;
    font-family: 'Space Mono', monospace;
    line-height: 1.3;
}
.kpi-sub {
    font-size: 11px;
    color: #00d4aa;
    margin-top: 6px;
    font-weight: 500;
}
.section-header {
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #6b7399;
    border-bottom: 1px solid #1a1a2e;
    padding-bottom: 8px;
    margin-bottom: 1rem;
    margin-top: 1.5rem;
}
.page-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 4px;
}
.page-subtitle {
    font-size: 0.85rem;
    color: #6b7399;
    margin-bottom: 1.5rem;
}
.insight-box {
    background: linear-gradient(135deg, #0f1a14, #0d1612);
    border: 1px solid #1a3028;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.8rem;
    transition: all 0.2s;
}
.insight-box:hover {
    border-color: rgba(0,212,170,0.3);
    transform: translateX(3px);
}
.insight-title {
    font-size: 10px;
    font-weight: 600;
    color: #00d4aa;
    margin-bottom: 5px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
.insight-text {
    font-size: 13px;
    color: #a0aec0;
    line-height: 1.6;
}
.live-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(0,212,170,0.1);
    border: 1px solid rgba(0,212,170,0.3);
    border-radius: 50px;
    padding: 4px 12px;
    font-size: 11px;
    color: #00d4aa;
    font-weight: 600;
    margin-bottom: 1rem;
}
.live-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #00d4aa;
    animation: pulse 1.5s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.2; }
}
</style>
"""