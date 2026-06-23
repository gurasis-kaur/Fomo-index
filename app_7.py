import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(
    page_title="FOMO Index | North American Markets",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background-color: #060B18;
    color: #E2E8F0;
}
.main { background-color: #060B18; }
.block-container { padding-top: 2rem; padding-bottom: 2rem; }

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0A1628 0%, #0D1F3C 100%);
    border-right: 1px solid #1E3A5F;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: #0A1628;
    border-radius: 12px;
    padding: 4px;
    border: 1px solid #1E3A5F;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #64748B;
    border-radius: 8px;
    font-weight: 500;
    font-size: 0.82rem;
    padding: 8px 16px;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #1E40AF, #3B82F6) !important;
    color: white !important;
}

/* Cards */
.card {
    background: linear-gradient(135deg, #0D1F3C 0%, #0A1628 100%);
    border: 1px solid #1E3A5F;
    border-radius: 16px;
    padding: 20px 24px;
    margin-bottom: 14px;
    transition: all 0.2s;
}
.card:hover { border-color: #3B82F6; transform: translateY(-1px); }
.card.high { border-left: 4px solid #EF4444; }
.card.moderate { border-left: 4px solid #F59E0B; }
.card.low { border-left: 4px solid #10B981; }

.card-title { font-size: 1rem; font-weight: 700; color: #F1F5F9; margin-bottom: 4px; }
.card-meta { font-size: 0.72rem; color: #64748B; margin-bottom: 12px; }

/* Badges */
.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.68rem;
    font-weight: 700;
    margin-right: 5px;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}
.b-red { background: rgba(239,68,68,0.12); color: #F87171; border: 1px solid rgba(239,68,68,0.25); }
.b-yellow { background: rgba(245,158,11,0.12); color: #FCD34D; border: 1px solid rgba(245,158,11,0.25); }
.b-green { background: rgba(16,185,129,0.12); color: #34D399; border: 1px solid rgba(16,185,129,0.25); }
.b-blue { background: rgba(59,130,246,0.12); color: #60A5FA; border: 1px solid rgba(59,130,246,0.25); }
.b-purple { background: rgba(139,92,246,0.12); color: #A78BFA; border: 1px solid rgba(139,92,246,0.25); }
.b-orange { background: rgba(249,115,22,0.12); color: #FB923C; border: 1px solid rgba(249,115,22,0.25); }

/* Info boxes */
.infobox {
    background: linear-gradient(135deg, #0D1F3C 0%, #0A1628 100%);
    border: 1px solid #1E3A5F;
    border-radius: 12px;
    padding: 18px 22px;
    font-size: 0.85rem;
    line-height: 1.7;
    color: #CBD5E1;
    margin-bottom: 12px;
}

/* Ticker rows */
.tick {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 9px 0;
    border-bottom: 1px solid #1E3A5F;
}
.tick-name { font-size: 0.82rem; font-weight: 600; color: #E2E8F0; }
.tick-price { font-size: 0.82rem; color: #F1F5F9; font-weight: 500; }
.up { color: #34D399; font-size: 0.75rem; }
.dn { color: #F87171; font-size: 0.75rem; }

/* Section headers */
.sec-head {
    font-size: 0.65rem;
    font-weight: 700;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    margin: 20px 0 10px 0;
    padding-bottom: 8px;
    border-bottom: 1px solid #1E3A5F;
}

/* Score display */
.big-score { font-size: 3.5rem; font-weight: 800; line-height: 1; }
.score-red { color: #EF4444; }
.score-yellow { color: #F59E0B; }
.score-green { color: #10B981; }

/* Search */
.stTextInput > div > div > input {
    background: #0D1F3C !important;
    border: 1px solid #1E3A5F !important;
    border-radius: 10px !important;
    color: #E2E8F0 !important;
    font-size: 0.9rem !important;
}
.stSelectbox > div > div {
    background: #0D1F3C !important;
    border: 1px solid #1E3A5F !important;
    border-radius: 10px !important;
    color: #E2E8F0 !important;
}

/* Logo */
.logo {
    font-size: 1.5rem;
    font-weight: 800;
    background: linear-gradient(135deg, #3B82F6, #8B5CF6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.logo-sub { font-size: 0.68rem; color: #334155; margin-bottom: 24px; letter-spacing: 0.05em; }

.live-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(16,185,129,0.1);
    border: 1px solid rgba(16,185,129,0.2);
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.7rem;
    color: #34D399;
    font-weight: 600;
}

.hero-title { font-size: 2rem; font-weight: 800; color: #F1F5F9; line-height: 1.2; margin-bottom: 6px; }
.hero-sub { font-size: 0.88rem; color: #64748B; margin-bottom: 24px; }

.stat-card {
    background: linear-gradient(135deg, #0D1F3C, #0A1628);
    border: 1px solid #1E3A5F;
    border-radius: 14px;
    padding: 18px;
    text-align: center;
}
.stat-val { font-size: 1.8rem; font-weight: 800; color: #F1F5F9; }
.stat-label { font-size: 0.68rem; color: #64748B; text-transform: uppercase; letter-spacing: 0.1em; margin-top: 4px; }

.disclaimer { font-size: 0.65rem; color: #1E3A5F; margin-top: 16px; line-height: 1.6; }

.search-result-count { font-size: 0.75rem; color: #64748B; margin-bottom: 16px; }

div[data-testid="stMetricValue"] { color: #F1F5F9 !important; }
</style>
""", unsafe_allow_html=True)

# ── DATA ──────────────────────────────────────────────────────────────────────

WATCHLIST = [
    ("RY.TO",   "Royal Bank",  "🇨🇦"),
    ("TD.TO",   "TD Bank",     "🇨🇦"),
    ("SHOP.TO", "Shopify",     "🇨🇦"),
    ("SU.TO",   "Suncor",      "🇨🇦"),
    ("XIU.TO",  "TSX ETF",     "🇨🇦"),
    ("AAPL",    "Apple",       "🇺🇸"),
    ("TSLA",    "Tesla",       "🇺🇸"),
    ("NVDA",    "Nvidia",      "🇺🇸"),
    ("SPY",     "S&P 500",     "🇺🇸"),
    ("GME",     "GameStop",    "🇺🇸"),
]

BIAS_INFO = {
    "Herd Behaviour": {
        "short": "Everyone copies everyone else — not because it makes sense, but because it feels safe.",
        "long": "Herd behaviour occurs when investors abandon independent analysis and follow the crowd. It is rooted in social proof — a cognitive shortcut where we assume that if everyone else is doing something, it must be correct. In markets, this creates self-fulfilling crashes and bubbles. When SVB collapsed, Canadian bank stocks fell sharply despite having fundamentally stronger balance sheets. Investors did not analyze — they saw others selling and sold too.",
        "academic": "Documented extensively by Kahneman (2011) and Bikhchandani et al. (1992). The key signal is abnormal volume combined with price moves that exceed what fundamentals justify.",
        "reversion": "High herd events typically revert within 8–18 trading days once fundamentals reassert."
    },
    "Loss Aversion": {
        "short": "Fear of losing feels twice as painful as the joy of gaining the same amount.",
        "long": "Kahneman and Tversky's Prospect Theory (1979) showed that losses feel roughly 2x more painful than equivalent gains feel pleasurable. In practice, this means investors sell fundamentally strong stocks during geopolitical events or market panics — not because the companies changed, but because the feeling of watching losses accumulate is psychologically unbearable. This creates the best buying opportunities for rational investors.",
        "academic": "Prospect Theory (Kahneman & Tversky, 1979) — Nobel Prize winning research. Loss aversion coefficient estimated at 1.5x to 2.5x across studies.",
        "reversion": "Loss aversion events in strong sectors (Canadian energy, Canadian banks) historically revert within 15–30 trading days."
    },
    "FOMO": {
        "short": "Fear of Missing Out — chasing a rally long after the rational entry point has passed.",
        "long": "FOMO in markets is the irrational compulsion to buy into a rising asset simply because others are profiting. The key psychological driver is regret aversion — investors fear the regret of watching something moon without them more than they fear the regret of buying at the top. GameStop is the textbook case: retail investors bought at $400+ not because they believed in the fundamentals, but because they could not stand watching others make money.",
        "academic": "Related to regret aversion (Bell, 1982) and the disposition effect (Shefrin & Statman, 1985). FOMO events show the highest initial velocity but also the fastest and most complete reversions.",
        "reversion": "Pure FOMO events revert 70–90% within 3–4 weeks. The faster the initial spike, the faster the reversion."
    },
    "Anchoring": {
        "short": "Investors fixate on a reference number and adjust too slowly when reality changes.",
        "long": "Anchoring bias occurs when investors use an initial piece of information — a past interest rate, a stock's 52-week high, a previous valuation — as the reference point for all future judgments. When the Bank of Canada signaled a rate pause, markets over-reacted because investors were anchored to the idea that rates were done rising. When the Fed raised rates in 2022, tech investors were anchored to the zero-rate era and could not adjust valuations fast enough.",
        "academic": "Tversky & Kahneman (1974). Anchoring is particularly powerful in policy contexts where central bank communication creates strong reference points.",
        "reversion": "Anchoring events have longer tails than FOMO — partial reversion in 2–4 weeks, full adjustment over 3–6 months."
    },
    "Availability Bias": {
        "short": "We overweight recent vivid events — if it is easy to remember, it feels more likely to happen again.",
        "long": "The availability heuristic causes investors to judge the probability of an event by how easily an example comes to mind. After SVB collapsed, investors saw banking risk everywhere — even in Canadian banks with completely different balance sheets. After COVID crashed markets, investors sold at the first sign of any negative news for months. The vividness of the recent event overwhelms rational probability assessment.",
        "academic": "Tversky & Kahneman (1973). The availability heuristic is one of the most documented cognitive biases in financial decision-making.",
        "reversion": "Availability bias effects diminish gradually as the vivid event fades from memory — typically 30–60 trading days."
    },
    "Overconfidence": {
        "short": "Investors overestimate their ability to predict the market — and trade too much as a result.",
        "long": "Overconfidence bias causes investors to believe their information and judgment is more accurate than it actually is. During bull markets, rising prices feel like confirmation of skill rather than market-wide tailwinds. This leads to excessive trading, concentrated positions, and underestimation of downside risk. The 2021 crypto and meme stock mania was heavily driven by overconfidence — retail investors who made money in rising markets attributed it to skill and bet bigger.",
        "academic": "Barber & Odean (2001) showed overconfident investors trade 45% more and earn 3.7% less annually than less active investors.",
        "reversion": "Overconfidence-driven rallies typically correct when a catalyst forces reality check — earnings misses, macro surprises, or simply running out of new buyers."
    },
    "Recency Bias": {
        "short": "Whatever happened recently feels like it will keep happening forever.",
        "long": "Recency bias causes investors to extrapolate recent trends indefinitely. After a long bull market, investors pile in expecting it to continue. After a crash, they stay out expecting more losses. In Canadian markets, recency bias is particularly visible around commodity cycles — investors pile into energy stocks after oil rallies and dump them after every correction, extrapolating short-term price moves into permanent trends.",
        "academic": "Related to the representativeness heuristic (Kahneman & Tversky, 1972). Recency bias is amplified by media coverage which reinforces recent narratives.",
        "reversion": "Recency bias effects are harder to time — they can persist for months in trending markets before mean-reverting sharply."
    },
}

EVENTS = [
    # TRUMP / TRADE WAR
    {"id": 1, "date": "2025-04-02", "event": "Trump Liberation Day Tariffs", "tags": ["trump", "tariff", "trade", "canada", "tsx"], "category": "Trade War", "bias": "Loss Aversion", "ticker": "XIU.TO", "ticker_label": "TSX ETF", "flag": "🇨🇦", "description": "Trump announced sweeping tariffs on virtually all imports including a 25% tariff on Canadian goods. TSX dropped sharply as loss aversion drove panic selling across manufacturing, auto, and energy sectors.", "outcome": "TSX fell 4.2% on announcement day. Partial recovery followed as markets priced in negotiation probability. Canadian energy stocks recovered faster than exporters.", "lesson": "Trade war tariff announcements create the sharpest initial loss aversion spikes in Canadian markets. Sectors with domestic revenue and negotiation leverage recover first."},
    {"id": 2, "date": "2025-01-20", "event": "Trump Threatens 25% Canada Tariffs (Inauguration)", "tags": ["trump", "tariff", "canada", "trade"], "category": "Trade War", "bias": "Loss Aversion", "ticker": "RY.TO", "ticker_label": "Royal Bank (TSX)", "flag": "🇨🇦", "description": "On his first day back in office, Trump threatened 25% tariffs on all Canadian and Mexican goods. CAD dropped and TSX financials sold off on loss aversion panic.", "outcome": "Initial panic reversed partially within 5 trading days as analysts noted the threat was a negotiating tactic.", "lesson": "Trump tariff threats vs actual implementation produce different FOMO profiles. Threats produce sharp short-lived spikes. Actual implementation produces sustained pressure."},
    {"id": 3, "date": "2018-06-01", "event": "Trump Steel and Aluminum Tariffs on Canada", "tags": ["trump", "tariff", "steel", "canada", "trade"], "category": "Trade War", "bias": "Loss Aversion", "ticker": "SU.TO", "ticker_label": "Suncor (TSX)", "flag": "🇨🇦", "description": "Trump invoked national security to impose 25% steel and 10% aluminum tariffs on Canada. Canadian retaliation followed. Markets experienced loss aversion selling across industrials.", "outcome": "Tariffs removed in May 2019 as part of CUSMA negotiations. Stocks fully recovered within 60 days of removal.", "lesson": "Trade wars with Canada historically resolve through negotiation. Patient investors who bought into loss aversion panic were rewarded within 6-12 months."},
    # BANKING CRISIS
    {"id": 4, "date": "2023-03-10", "event": "Silicon Valley Bank Collapse", "tags": ["svb", "bank", "collapse", "crisis", "silicon valley"], "category": "Banking Crisis", "bias": "Herd Behaviour", "ticker": "TD.TO", "ticker_label": "TD Bank (TSX)", "flag": "🇨🇦", "description": "SVB collapsed after a bank run triggered by a failed capital raise. Herd behaviour caused panic selling in Canadian bank stocks despite Canada's Big 6 having fundamentally stronger balance sheets and stricter capital requirements.", "outcome": "TD and Royal Bank fell 6-8% in the week following SVB. Fully recovered within 18 trading days as rational analysis replaced panic.", "lesson": "Canadian banks have never failed in the modern era due to OSFI capital requirements. SVB-style herd behaviour in Canadian banks is historically the strongest buy signal in this sector."},
    {"id": 5, "date": "2023-03-19", "event": "Credit Suisse Emergency Rescue by UBS", "tags": ["credit suisse", "ubs", "bank", "crisis", "europe"], "category": "Banking Crisis", "bias": "Herd Behaviour", "ticker": "XIU.TO", "ticker_label": "TSX ETF", "flag": "🇨🇦", "description": "Credit Suisse was acquired by UBS in a government-brokered emergency deal over a weekend. Global bank stocks fell on renewed herd behaviour panic.", "outcome": "TSX financials dropped 3-4% then stabilized within 10 trading days as European bank contagion fears did not materialize in Canada.", "lesson": "International banking crises trigger herd behaviour in Canadian bank stocks that is almost always irrational given OSFI oversight and Canadian bank capital strength."},
    # FEDERAL RESERVE / BANK OF CANADA
    {"id": 6, "date": "2022-03-16", "event": "US Fed First Rate Hike Post-COVID", "tags": ["fed", "rate", "hike", "federal reserve", "interest rate", "policy"], "category": "Policy Shock", "bias": "Anchoring", "ticker": "XIU.TO", "ticker_label": "TSX ETF", "flag": "🇺🇸", "description": "The Federal Reserve raised rates for the first time since 2018, ending the zero-rate era. Markets were anchored to cheap money valuations built over 2 years of near-zero rates and could not recalibrate fast enough.", "outcome": "TSX fell 12% and S&P 500 fell 18% over the following 6 months as anchored valuations unwound. Growth and tech hit hardest.", "lesson": "Rate anchoring unwinds slowly and painfully over months. The initial reaction undershoot is followed by continued pressure as DCF models are repriced across the entire market."},
    {"id": 7, "date": "2023-01-25", "event": "Bank of Canada Rate Pause Signal", "tags": ["bank of canada", "boc", "rate", "pause", "interest rate", "canada", "policy"], "category": "Policy", "bias": "Anchoring", "ticker": "RY.TO", "ticker_label": "Royal Bank (TSX)", "flag": "🇨🇦", "description": "Bank of Canada signaled a conditional pause in rate hikes. Markets immediately anchored to rates are done and overbought rate-sensitive Canadian bank and real estate stocks.", "outcome": "Initial rally reversed partially within 30 days as BoC clarified the pause was data-dependent and raised once more in June 2023.", "lesson": "BoC communication anchoring is one of the most consistent FOMO patterns in Canadian markets. Never anchor to a pause signal — always wait for the actual data."},
    {"id": 8, "date": "2024-06-05", "event": "Bank of Canada First Rate Cut", "tags": ["bank of canada", "boc", "rate cut", "interest rate", "canada"], "category": "Policy", "bias": "FOMO", "ticker": "XIU.TO", "ticker_label": "TSX ETF", "flag": "🇨🇦", "description": "BoC became the first G7 central bank to cut rates, reducing by 25bps to 4.75%. FOMO drove a surge in rate-sensitive Canadian real estate and financial stocks.", "outcome": "TSX hit new all-time highs in following months. Real estate stocks outperformed significantly. The FOMO was partially justified by fundamentals.", "lesson": "Not all FOMO is irrational. When FOMO aligns with a genuine fundamental catalyst like an actual rate cut, the initial surge can sustain longer than typical FOMO events."},
    {"id": 9, "date": "2022-06-15", "event": "Fed 75bps Jumbo Rate Hike", "tags": ["fed", "rate", "hike", "federal reserve", "75bps", "inflation"], "category": "Policy Shock", "bias": "Anchoring", "ticker": "SPY", "ticker_label": "S&P 500 ETF", "flag": "🇺🇸", "description": "The Fed raised rates by 75bps — the largest single hike since 1994 — shocking markets anchored to 25-50bps increments. The word transitory had been abandoned months earlier but many investors were still anchored to it.", "outcome": "S&P 500 fell 23% in 2022. The 75bps shock accelerated a repricing that lasted the entire year.", "lesson": "When the Fed breaks its own communication anchors, the repricing is violent and prolonged. This is the most dangerous form of anchoring bias."},
    # GAMESTOP / MEME
    {"id": 10, "date": "2021-01-27", "event": "GameStop Short Squeeze Peak", "tags": ["gamestop", "gme", "meme", "short squeeze", "reddit", "wallstreetbets", "wsb"], "category": "Meme/Viral", "bias": "FOMO", "ticker": "GME", "ticker_label": "GameStop (NYSE)", "flag": "🇺🇸", "description": "Reddit WallStreetBets coordinated a historic short squeeze sending GME from $20 to $483 in days. Pure FOMO drove retail investors to buy at any price because others were making life-changing money.", "outcome": "GME fell 90% from peak within 3 weeks. Retail investors who bought above $100 lost catastrophically. The company itself was fundamentally unchanged.", "lesson": "When the only investment thesis is other people are making money, you are the exit liquidity. Pure FOMO events with no fundamental basis revert the fastest and most completely."},
    {"id": 11, "date": "2021-02-24", "event": "AMC and Meme Stock Second Wave", "tags": ["amc", "meme", "short squeeze", "reddit", "wallstreetbets"], "category": "Meme/Viral", "bias": "FOMO", "ticker": "GME", "ticker_label": "GameStop (NYSE)", "flag": "🇺🇸", "description": "A second wave of meme stock mania hit AMC, BB (BlackBerry — a Canadian company), and GME again. FOMO drove retail investors back in hoping to replicate January gains.", "outcome": "Most positions lost value within 30 days. BlackBerry fell 50% from meme peak within 60 days.", "lesson": "Second wave FOMO events are even more dangerous than originals — the crowd hopes to repeat what worked before in a completely different environment."},
    # COVID
    {"id": 12, "date": "2020-03-16", "event": "COVID Market Crash — Black Monday", "tags": ["covid", "pandemic", "crash", "2020", "coronavirus"], "category": "Pandemic Shock", "bias": "Loss Aversion", "ticker": "SPY", "ticker_label": "S&P 500 ETF", "flag": "🇺🇸", "description": "The S&P 500 fell 12% in a single day — worst since 1987 — as COVID lockdowns began. Loss aversion caused mass selling of fundamentally strong companies at historic discounts. Circuit breakers triggered multiple times.", "outcome": "S&P 500 fully recovered within 5 months and hit new all-time highs by August 2020 — the fastest recovery from a 30%+ bear market in history.", "lesson": "Pandemic-scale loss aversion created the biggest buying opportunity of a generation. The investors who bought into the panic were rewarded within months. Loss aversion was the enemy."},
    {"id": 13, "date": "2020-03-23", "event": "TSX Hits COVID Low", "tags": ["covid", "tsx", "canada", "crash", "pandemic"], "category": "Pandemic Shock", "bias": "Loss Aversion", "ticker": "XIU.TO", "ticker_label": "TSX ETF", "flag": "🇨🇦", "description": "TSX hit its COVID bottom, down 37% from February highs. Canadian energy and financial stocks were among the hardest hit as oil prices also collapsed simultaneously.", "outcome": "TSX recovered fully by February 2021. Energy stocks took longer due to oil price dynamics but recovered 100%+ from lows.", "lesson": "TSX COVID lows were a once-in-a-decade buying opportunity. The double shock of COVID plus oil price war created maximum loss aversion — and maximum opportunity for rational investors."},
    # CRYPTO CONTAGION
    {"id": 14, "date": "2022-05-11", "event": "Terra Luna Collapse", "tags": ["luna", "terra", "crypto", "collapse", "stablecoin"], "category": "Crypto Contagion", "bias": "Availability Bias", "ticker": "TSLA", "ticker_label": "Tesla (NASDAQ)", "flag": "🇺🇸", "description": "Terra LUNA lost 99.9% of its value in days as its algorithmic stablecoin UST lost its peg. Availability bias caused crypto contagion fears to spill into tech stocks and even traditional markets.", "outcome": "Triggered a broader crypto winter. Tech stocks with crypto exposure fell 20-40% in following months. Traditional equities experienced moderate contagion.", "lesson": "Crypto collapse availability bias hits tech stocks harder than fundamentals justify. The visual of a $40B asset going to zero creates vivid mental availability that distorts risk perception."},
    {"id": 15, "date": "2022-11-11", "event": "FTX Bankruptcy and Sam Bankman-Fried", "tags": ["ftx", "sbf", "crypto", "bankruptcy", "fraud"], "category": "Crypto Contagion", "bias": "Availability Bias", "ticker": "TSLA", "ticker_label": "Tesla (NASDAQ)", "flag": "🇺🇸", "description": "FTX crypto exchange collapsed in 72 hours revealing massive fraud. Availability bias created contagion fears across all crypto and tech assets.", "outcome": "Bitcoin fell 20% in a week. Tech stocks with crypto exposure sold off. Traditional financial stocks saw minimal impact despite availability bias fears.", "lesson": "Fraud-driven collapses create the strongest availability bias signals. The narrative of fraud is so vivid it distorts risk assessment for unrelated assets for weeks."},
    # GEOPOLITICAL
    {"id": 16, "date": "2022-02-24", "event": "Russia Invades Ukraine", "tags": ["russia", "ukraine", "war", "geopolitical", "energy", "oil"], "category": "Geopolitical", "bias": "Loss Aversion", "ticker": "SU.TO", "ticker_label": "Suncor (TSX)", "flag": "🇨🇦", "description": "Russia launched full-scale invasion of Ukraine. Loss aversion drove panic selling globally despite many Canadian energy stocks actually benefiting from oil price spikes above $120/barrel.", "outcome": "Suncor and Canadian energy stocks surged 40-60% in following months as oil hit $120+. Investors who panic sold lost extraordinary gains.", "lesson": "Geopolitical events create the biggest disconnect between emotional reaction and fundamental reality for Canadian energy. Canada is a direct beneficiary of European energy supply disruption."},
    {"id": 17, "date": "2023-10-07", "event": "Hamas Attack on Israel", "tags": ["israel", "hamas", "war", "geopolitical", "middle east"], "category": "Geopolitical", "bias": "Loss Aversion", "ticker": "SPY", "ticker_label": "S&P 500 ETF", "flag": "🇺🇸", "description": "Hamas launched unprecedented attack on Israel triggering conflict. Loss aversion caused oil price spike and defensive selling across equities globally.", "outcome": "S&P 500 initially fell 3% then recovered fully within 2 weeks. Oil spiked briefly then normalized. Canadian defense-adjacent stocks benefited.", "lesson": "Middle East conflicts trigger strong but short-lived loss aversion in Western equities. Unless oil supply is actually disrupted, the fundamental impact on North American stocks is limited."},
    # INFLATION
    {"id": 18, "date": "2022-06-10", "event": "US CPI Hits 9.1% — 40 Year High", "tags": ["inflation", "cpi", "us", "federal reserve", "rate"], "category": "Macro Shock", "bias": "Recency Bias", "ticker": "SPY", "ticker_label": "S&P 500 ETF", "flag": "🇺🇸", "description": "US inflation hit 9.1% — highest since 1981. Investors anchored to the low-inflation 2010s environment could not adjust their mental models fast enough. Recency bias made them believe low inflation was permanent.", "outcome": "Triggered the most aggressive Fed tightening cycle in 40 years. S&P 500 fell 25% in 2022. Bonds lost more than stocks — an extremely rare event.", "lesson": "Regime changes — from low inflation to high inflation — are the hardest for recency bias investors to accept. The investors who adapted fastest (rotating to energy, commodities, value) significantly outperformed."},
    {"id": 19, "date": "2022-07-13", "event": "Canada CPI Hits 8.1% — Generational High", "tags": ["canada", "inflation", "cpi", "bank of canada", "boc"], "category": "Macro Shock", "bias": "Recency Bias", "ticker": "XIU.TO", "ticker_label": "TSX ETF", "flag": "🇨🇦", "description": "Canadian inflation hit 8.1% — highest since 1983. Bank of Canada had been behind the curve and was forced into aggressive tightening. Recency bias had led markets to underestimate inflation persistence.", "outcome": "BoC raised rates 10 consecutive times. Canadian real estate fell 20-25%. Rate-sensitive stocks underperformed for 18 months.", "lesson": "Recency bias in Canadian markets made the inflation regime change especially painful. Canadian real estate — which had never fallen significantly in living memory — became the ultimate recency bias trap."},
    # TECH
    {"id": 20, "date": "2023-11-30", "event": "OpenAI ChatGPT One Year — AI Euphoria Peak", "tags": ["ai", "chatgpt", "openai", "nvidia", "tech", "artificial intelligence"], "category": "Tech Euphoria", "bias": "FOMO", "ticker": "NVDA", "ticker_label": "Nvidia (NASDAQ)", "flag": "🇺🇸", "description": "One year after ChatGPT launch, AI FOMO reached peak levels. Nvidia had risen 240% in 2023. Every company adding AI to its press release saw its stock surge regardless of actual AI revenue.", "outcome": "Nvidia continued rising through 2024. However many AI-adjacent stocks with no real AI revenue gave back gains within 6 months.", "lesson": "Not all FOMO is irrational — Nvidia had real earnings growth justifying its rise. But distinguishing between fundamental FOMO (Nvidia) and narrative FOMO (random AI stock) is the key analytical skill."},
    {"id": 21, "date": "2024-07-17", "event": "CrowdStrike Global IT Outage", "tags": ["crowdstrike", "outage", "tech", "it", "microsoft"], "category": "Tech Crisis", "bias": "Availability Bias", "ticker": "NVDA", "ticker_label": "Nvidia (NASDAQ)", "flag": "🇺🇸", "description": "A faulty CrowdStrike update caused 8.5 million Windows devices worldwide to crash — the largest IT outage in history. Availability bias created cybersecurity sector panic beyond CrowdStrike itself.", "outcome": "CrowdStrike fell 40% initially. Cybersecurity sector broadly sold off despite other companies having no involvement. CrowdStrike recovered 60% of losses within 3 months.", "lesson": "Single-company tech failures create availability bias in entire sectors. The irrational spillover to unrelated cybersecurity stocks was a buying opportunity."},
    # CANADIAN SPECIFIC
    {"id": 22, "date": "2021-09-20", "event": "Evergrande Crisis — China Property Panic", "tags": ["evergrande", "china", "property", "crisis", "contagion"], "category": "Contagion Risk", "bias": "Availability Bias", "ticker": "XIU.TO", "ticker_label": "TSX ETF", "flag": "🇨🇦", "description": "Chinese property giant Evergrande missed bond payments raising fears of a Lehman-style contagion. Availability bias caused Canadian mining and commodity stocks to sell off on China demand fears.", "outcome": "TSX mining and materials fell 5-8%. Recovered fully within 3 weeks as China contagion fears did not materialize in Western markets.", "lesson": "China crisis availability bias hits Canadian commodity stocks hard due to China's importance as a commodity buyer. But Western financial contagion from Chinese property debt has historically not materialized."},
    {"id": 23, "date": "2024-04-15", "event": "Canada Federal Budget 2024 — Capital Gains Tax Hike", "tags": ["canada", "budget", "capital gains", "tax", "trudeau"], "category": "Policy", "bias": "Loss Aversion", "ticker": "SHOP.TO", "ticker_label": "Shopify (TSX)", "flag": "🇨🇦", "description": "Trudeau government increased capital gains inclusion rate from 50% to 67% for gains over $250K. Loss aversion drove immediate selling of high-gain Canadian tech and investment stocks to lock in lower tax rates.", "outcome": "Shopify and other high-appreciation Canadian tech stocks saw unusual volume as investors crystallized gains. Temporary selling pressure resolved within 30 days.", "lesson": "Tax policy changes trigger rational-seeming but often poorly timed loss aversion selling. Investors who sold to avoid the tax often triggered the very taxable event they were trying to minimize."},
]

CATEGORIES = sorted(list(set(e["category"] for e in EVENTS)))

# ── HELPERS ──────────────────────────────────────────────────────────────────

@st.cache_data(ttl=300)
def fetch_ticker(ticker, period="5d"):
    try:
        h = yf.Ticker(ticker).history(period=period)
        return h
    except Exception:
        return pd.DataFrame()

@st.cache_data(ttl=600)
def fetch_event_data(ticker, period="6mo"):
    try:
        h = yf.Ticker(ticker).history(period=period)
        return h
    except Exception:
        return pd.DataFrame()

def calc_car(df, event_date):
    try:
        ets = pd.Timestamp(event_date)
        df = df.copy()
        df.index = pd.to_datetime(df.index).tz_localize(None)
        pre = df[df.index < ets].tail(20)
        if len(pre) < 3:
            return df, 0
        baseline = float(pre["Close"].mean())
        if baseline == 0:
            return df, 0
        df["CAR"] = ((df["Close"] - baseline) / baseline) * 100
        post = df[df.index >= ets].head(20)
        if len(post) == 0:
            return df, 0
        swing = float(post["CAR"].abs().max())
        score = min(round(swing * 3), 100)
        return df, score
    except Exception:
        return df, 0

def fomo_meta(score):
    if score >= 65:
        return "#EF4444", "high", "HIGH FOMO", "b-red", "score-red"
    elif score >= 35:
        return "#F59E0B", "moderate", "MODERATE FOMO", "b-yellow", "score-yellow"
    else:
        return "#10B981", "low", "LOW FOMO", "b-green", "score-green"

def gauge(score):
    col, _, _, _, sc = fomo_meta(score)
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={"text": "FOMO Score", "font": {"color": "#64748B", "size": 12, "family": "Inter"}},
        number={"font": {"color": col, "size": 52, "family": "Inter"}, "suffix": ""},
        gauge={
            "axis": {"range": [0, 100], "tickfont": {"color": "#334155", "size": 9}},
            "bar": {"color": col, "thickness": 0.3},
            "bgcolor": "#0D1F3C",
            "bordercolor": "#1E3A5F",
            "steps": [
                {"range": [0, 35], "color": "rgba(16,185,129,0.08)"},
                {"range": [35, 65], "color": "rgba(245,158,11,0.08)"},
                {"range": [65, 100], "color": "rgba(239,68,68,0.08)"},
            ],
            "threshold": {"line": {"color": col, "width": 3}, "thickness": 0.85, "value": score}
        }
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Inter"},
        height=240,
        margin=dict(t=40, b=0, l=20, r=20)
    )
    return fig

def car_chart(df, event_date, ticker):
    ets = pd.Timestamp(event_date)
    if "CAR" not in df.columns:
        return None
    pre = df[df.index < ets]
    post = df[df.index >= ets]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=pre.index, y=pre["CAR"], mode="lines", name="Pre-Event",
        line=dict(color="#3B82F6", width=2),
        fill="tozeroy", fillcolor="rgba(59,130,246,0.06)"
    ))
    fig.add_trace(go.Scatter(
        x=post.index, y=post["CAR"], mode="lines", name="Post-Event",
        line=dict(color="#EF4444", width=2.5),
        fill="tozeroy", fillcolor="rgba(239,68,68,0.07)"
    ))
    fig.add_vline(x=ets, line_dash="dash", line_color="#F59E0B",
                  line_width=1.5, annotation_text="  Event",
                  annotation_font_color="#F59E0B", annotation_font_size=11)
    fig.add_hline(y=0, line_dash="dot", line_color="#1E3A5F", line_width=1)
    fig.update_layout(
        title=dict(text=f"Cumulative Abnormal Return — {ticker}",
                   font=dict(color="#94A3B8", size=12, family="Inter")),
        xaxis=dict(showgrid=False, color="#334155"),
        yaxis=dict(gridcolor="#0D1F3C", color="#334155",
                   title="CAR %", titlefont=dict(size=11)),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#060B18",
        font=dict(family="Inter", color="#64748B"),
        legend=dict(bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#64748B", size=11)),
        height=300,
        margin=dict(t=40, b=20, l=10, r=10),
        hovermode="x unified"
    )
    return fig

def search_events(query, category, events):
    q = query.strip().lower()
    results = []
    for e in events:
        cat_match = (category == "All Categories" or e["category"] == category)
        if not cat_match:
            continue
        if q == "":
            results.append(e)
        else:
            searchable = " ".join(e["tags"]) + " " + e["event"].lower() + " " + e["category"].lower()
            if q in searchable:
                results.append(e)
    return results

# ── SIDEBAR ──────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown('<div class="logo">FOMO Index</div>', unsafe_allow_html=True)
    st.markdown('<div class="logo-sub">NORTH AMERICAN BEHAVIORAL FINANCE</div>', unsafe_allow_html=True)

    st.markdown('<div class="sec-head">Live Market Pulse</div>', unsafe_allow_html=True)

    for ticker, name, flag in WATCHLIST:
        h = fetch_ticker(ticker, "5d")
        if not h.empty and len(h) >= 2:
            price = float(h["Close"].iloc[-1])
            prev  = float(h["Close"].iloc[-2])
            chg   = ((price - prev) / prev) * 100
            cls   = "up" if chg >= 0 else "dn"
            sign  = "▲" if chg >= 0 else "▼"
            st.markdown(
                f'<div class="tick">'
                f'<span class="tick-name">{flag} {name}</span>'
                f'<span><span class="tick-price">${price:.2f}</span> '
                f'<span class="{cls}">{sign}{abs(chg):.1f}%</span></span>'
                f'</div>',
                unsafe_allow_html=True
            )

    st.markdown(
        f'<div style="margin-top:12px;" class="live-pill">● LIVE &nbsp;·&nbsp; {datetime.now().strftime("%b %d %H:%M")} ET</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="disclaimer">Not financial advice. Educational research tool only.<br>Built by Gurasis Kaur · University of Waterloo · Financial Economics & Business</div>',
        unsafe_allow_html=True
    )

# ── MAIN ─────────────────────────────────────────────────────────────────────

st.markdown('<div class="hero-title">📈 North American FOMO Index</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Measure the irrational. Understand the psychology. Make better decisions.</div>', unsafe_allow_html=True)

# Stats row
total_events = len(EVENTS)
high_fomo_count = 8
categories_count = len(CATEGORIES)
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f'<div class="stat-card"><div class="stat-val">{total_events}</div><div class="stat-label">Events Tracked</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="stat-card"><div class="stat-val">{categories_count}</div><div class="stat-label">Event Categories</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="stat-card"><div class="stat-val">7</div><div class="stat-label">Biases Classified</div></div>', unsafe_allow_html=True)
with c4:
    st.markdown(f'<div class="stat-card"><div class="stat-val">2018–2025</div><div class="stat-label">Date Range</div></div>', unsafe_allow_html=True)

st.markdown('<div style="height:24px;"></div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🔍  Event Search & Analysis", "🧠  Bias Library", "📖  Methodology"])

# ══ TAB 1 ════════════════════════════════════════════════════════════════════
with tab1:
    sc1, sc2 = st.columns([3, 1])
    with sc1:
        query = st.text_input("", placeholder="🔍  Search events — try 'Trump', 'tariff', 'bank', 'covid', 'rate hike', 'GameStop'...", label_visibility="collapsed")
    with sc2:
        cat_filter = st.selectbox("", ["All Categories"] + CATEGORIES, label_visibility="collapsed")

    results = search_events(query, cat_filter, EVENTS)
    st.markdown(f'<div class="search-result-count">{len(results)} event{"s" if len(results) != 1 else ""} found</div>', unsafe_allow_html=True)

    if not results:
        st.markdown('<div class="infobox" style="text-align:center;padding:32px;">No events matched your search. Try broader terms like "bank", "trade", "inflation", or "tech".</div>', unsafe_allow_html=True)
    else:
        # Event selector
        event_names = [f"{e['flag']} {e['date'][:7]}  ·  {e['event']}" for e in results]
        selected_label = st.selectbox("Select event to analyze:", event_names, label_visibility="collapsed")
        selected = results[event_names.index(selected_label)]

        st.markdown('<div style="height:16px;"></div>', unsafe_allow_html=True)

        # Fetch data
        df = fetch_event_data(selected["ticker"], "6mo")
        fomo_score = 0
        if not df.empty:
            df, fomo_score = calc_car(df, selected["date"])
        col, level, label, badge_cls, score_cls = fomo_meta(fomo_score)

        # ── Row 1: Gauge + Summary ────────────────────────────────────
        g_col, s_col = st.columns([1, 2])

        with g_col:
            st.plotly_chart(gauge(fomo_score), use_container_width=True, config={"displayModeBar": False})
            st.markdown(
                f'<div style="text-align:center;margin-top:-8px;">'
                f'<span class="badge {badge_cls}">{label}</span>'
                f'<span class="badge b-purple">{selected["bias"]}</span>'
                f'<span class="badge b-blue">{selected["category"]}</span>'
                f'</div>',
                unsafe_allow_html=True
            )

        with s_col:
            st.markdown(f'<div style="font-size:1.3rem;font-weight:800;color:#F1F5F9;margin-bottom:4px;">{selected["event"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div style="font-size:0.75rem;color:#64748B;margin-bottom:16px;">{selected["date"]} &nbsp;·&nbsp; {selected["ticker_label"]} &nbsp;·&nbsp; {selected["flag"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="infobox"><b style="color:#A78BFA;">What happened:</b><br>{selected["description"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="infobox"><b style="color:#FCD34D;">What the data showed:</b><br>{selected["outcome"]}</div>', unsafe_allow_html=True)

        # ── Row 2: Psychology ─────────────────────────────────────────
        st.markdown('<div style="height:16px;"></div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-head">🧠 The Psychology — Plain English Explanation</div>', unsafe_allow_html=True)

        bias = BIAS_INFO.get(selected["bias"], {})
        p1, p2 = st.columns(2)
        with p1:
            st.markdown(
                f'<div class="infobox">'
                f'<b style="color:#F87171;font-size:0.95rem;">{selected["bias"]}</b>'
                f'<br><br>'
                f'<b style="color:#94A3B8;">In plain English:</b><br>{bias.get("short","")}'
                f'<br><br>'
                f'<b style="color:#94A3B8;">The full picture:</b><br>{bias.get("long","")}'
                f'</div>',
                unsafe_allow_html=True
            )
        with p2:
            if fomo_score >= 65:
                signal = f"Strong {selected['bias']} detected. The price move was significantly larger than fundamentals justify. Historical patterns suggest high probability of mean reversion."
            elif fomo_score >= 35:
                signal = f"Moderate {selected['bias']} detected. The reaction contained both rational and emotional components. Watch for stabilization before drawing conclusions."
            else:
                signal = f"Markets absorbed this event relatively rationally. The price move appears closer to fundamentally justified levels."
            st.markdown(
                f'<div class="infobox">'
                f'<b style="color:#34D399;font-size:0.95rem;">Signal Reading — FOMO Score {fomo_score}/100</b>'
                f'<br><br>{signal}'
                f'<br><br><b style="color:#94A3B8;">Academic backing:</b><br>{bias.get("academic","")}'
                f'<br><br><b style="color:#60A5FA;">Historical reversion pattern:</b><br>{bias.get("reversion","")}'
                f'<br><br><b style="color:#FCD34D;">Key lesson:</b><br>{selected["lesson"]}'
                f'</div>',
                unsafe_allow_html=True
            )

        # ── Row 3: CAR Chart ──────────────────────────────────────────
        st.markdown('<div style="height:16px;"></div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-head">📈 Cumulative Abnormal Return (CAR) Chart</div>', unsafe_allow_html=True)
        st.markdown('<div style="font-size:0.75rem;color:#334155;margin-bottom:12px;">CAR measures the gap between what the stock actually returned vs what it should have returned based on its pre-event average. The gap = the irrational premium. This is the exact methodology used by RBC Capital Markets and Goldman Sachs in M&A event studies.</div>', unsafe_allow_html=True)

        if not df.empty and "CAR" in df.columns:
            fig = car_chart(df, selected["date"], selected["ticker"])
            if fig:
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.markdown('<div class="infobox">Chart data unavailable for this event period.</div>', unsafe_allow_html=True)

        # ── Row 4: Similar Events ─────────────────────────────────────
        st.markdown('<div style="height:16px;"></div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-head">🔄 Similar Events — Same Bias, Different Context</div>', unsafe_allow_html=True)

        similar = [e for e in EVENTS if e["bias"] == selected["bias"] and e["id"] != selected["id"]][:3]
        if similar:
            cols = st.columns(len(similar))
            for i, ev in enumerate(similar):
                df2 = fetch_event_data(ev["ticker"], "6mo")
                sc2_val = 0
                if not df2.empty:
                    df2, sc2_val = calc_car(df2, ev["date"])
                _, lv2, _, bc2, _ = fomo_meta(sc2_val)
                with cols[i]:
                    st.markdown(
                        f'<div class="card {lv2}">'
                        f'<div class="card-title">{ev["flag"]} {ev["event"]}</div>'
                        f'<div class="card-meta">{ev["date"]} · {ev["ticker_label"]}</div>'
                        f'<span class="badge {bc2}">FOMO {sc2_val}/100</span>'
                        f'<span class="badge b-purple">{ev["bias"]}</span>'
                        f'<div style="margin-top:10px;font-size:0.78rem;color:#64748B;line-height:1.5;">{ev["outcome"]}</div>'
                        f'</div>',
                        unsafe_allow_html=True
                    )

# ══ TAB 2 ════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div style="color:#64748B;font-size:0.82rem;margin-bottom:20px;">Every behavioral bias explained in plain English — with academic backing, real market examples, and what to do when you spot one.</div>', unsafe_allow_html=True)
    for bias_name, info in BIAS_INFO.items():
        events_with_bias = [e for e in EVENTS if e["bias"] == bias_name]
        count = len(events_with_bias)
        with st.expander(f"  {bias_name}  ·  {count} events in database"):
            b1, b2 = st.columns(2)
            with b1:
                st.markdown(f'<div class="infobox"><b style="color:#F87171;">Plain English:</b><br>{info["short"]}<br><br><b style="color:#94A3B8;">Full explanation:</b><br>{info["long"]}</div>', unsafe_allow_html=True)
            with b2:
                st.markdown(f'<div class="infobox"><b style="color:#34D399;">Academic backing:</b><br>{info["academic"]}<br><br><b style="color:#60A5FA;">Typical reversion:</b><br>{info["reversion"]}<br><br><b style="color:#FCD34D;">Events in database:</b><br>' + "<br>".join([f"· {e['flag']} {e['event']} ({e['date'][:7]})" for e in events_with_bias]) + '</div>', unsafe_allow_html=True)

# ══ TAB 3 ════════════════════════════════════════════════════════════════════
with tab3:
    m1, m2 = st.columns(2)
    with m1:
        st.markdown('<div class="infobox"><b style="color:#A78BFA;font-size:1rem;">What Is FOMO Index?</b><br><br>A behavioral finance dashboard that measures how much of a stock market reaction to a major event is driven by human psychology rather than fundamentals.<br><br>When Trump announces tariffs, when a bank collapses, when a meme stock goes viral — markets react. But how much is rational? How much is panic, herd behavior, or pure FOMO?<br><br>This tool answers that with real data, real methodology, and plain English explanations.</div>', unsafe_allow_html=True)
        st.markdown('<div class="infobox" style="margin-top:0;"><b style="color:#FCD34D;font-size:1rem;">The CAR Methodology</b><br><br><b>Cumulative Abnormal Return (CAR)</b> is the gold standard event study framework used by Goldman Sachs, RBC Capital Markets, TD Securities, and academic researchers worldwide.<br><br>Formula: CAR = Actual Return − Expected Return<br><br>Expected return is calculated as the average pre-event return over 20 trading days. The deviation from this baseline is the behavioral premium — the part of the price move that cannot be explained by fundamentals alone.<br><br>The FOMO Score = min(|max CAR post-event| × 3, 100)</div>', unsafe_allow_html=True)
    with m2:
        st.markdown('<div class="infobox"><b style="color:#34D399;font-size:1rem;">Why This Exists</b><br><br>Bloomberg Terminal: $25,000/year. Tells you what happened. Not why.<br><br>CNN Fear & Greed: A single number. No event linkage. US only. No explanation.<br><br>Academic papers: The math is there. Nobody reads them.<br><br>FOMO Index: Free. Live. Searchable. Canada + US. Plain English psychology. Real methodology. Built for anyone who wants to understand markets, not just watch them.</div>', unsafe_allow_html=True)
        st.markdown('<div class="infobox" style="margin-top:0;"><b style="color:#60A5FA;font-size:1rem;">Bias Classification Logic</b><br><br>Each event is manually classified based on three factors:<br><br>1. <b>Price velocity</b> — how fast did the move happen vs historical volatility<br>2. <b>Volume anomaly</b> — did volume spike beyond normal ranges<br>3. <b>Fundamental justification</b> — did the event actually change earnings/cash flows<br><br>When price moves fast, volume spikes, and fundamentals did not change — that is behavioral bias at work.<br><br><b style="color:#94A3B8;">Disclaimer:</b> Not financial advice. Educational research tool. Always consult a licensed advisor before investing.</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown('<div style="text-align:center;color:#1E3A5F;font-size:0.65rem;">FOMO Index v2.0 · Built by Gurasis Kaur · Financial Economics & Business, University of Waterloo · Not financial advice</div>', unsafe_allow_html=True)
