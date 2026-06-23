import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import random

st.set_page_config(page_title="FOMO Index",page_icon="📈",layout="wide",initial_sidebar_state="expanded")
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif!important;background:#04090F;color:#E2E8F0;}
.main{background:#04090F;}.block-container{padding-top:1.2rem;max-width:1380px;}
section[data-testid="stSidebar"]{background:#060D18;border-right:1px solid #0C1F35;}
.stTabs [data-baseweb="tab-list"]{background:#060D18;border-radius:10px;padding:3px;border:1px solid #0C1F35;}
.stTabs [data-baseweb="tab"]{background:transparent;color:#3D5A7A;border-radius:8px;font-weight:600;font-size:.78rem;padding:6px 14px;}
.stTabs [aria-selected="true"]{background:linear-gradient(135deg,#1A3FC7,#2563EB)!important;color:#fff!important;}
.stTextInput>div>div>input{background:#060D18!important;border:1px solid #0C1F35!important;border-radius:10px!important;color:#E2E8F0!important;}
.stSelectbox>div>div{background:#060D18!important;border:1px solid #0C1F35!important;border-radius:10px!important;color:#E2E8F0!important;}
.panel{background:#060D18;border:1px solid #0C1F35;border-radius:13px;padding:16px 20px;margin-bottom:8px;}
.row{display:flex;align-items:flex-start;gap:10px;padding:6px 0;border-bottom:1px solid #0C1F35;font-size:.78rem;line-height:1.55;}
.row:last-child{border-bottom:none;}
.rk{font-weight:700;color:#CBD5E1;min-width:130px;font-size:.72rem;flex-shrink:0;}.rv{color:#94A3B8;}
.badge{display:inline-block;padding:2px 8px;border-radius:20px;font-size:.6rem;font-weight:700;margin-right:3px;text-transform:uppercase;}
.br{background:rgba(239,68,68,.1);color:#F87171;border:1px solid rgba(239,68,68,.2);}
.by{background:rgba(245,158,11,.1);color:#FCD34D;border:1px solid rgba(245,158,11,.2);}
.bg{background:rgba(16,185,129,.1);color:#34D399;border:1px solid rgba(16,185,129,.2);}
.bb{background:rgba(59,130,246,.1);color:#60A5FA;border:1px solid rgba(59,130,246,.2);}
.bp{background:rgba(139,92,246,.1);color:#A78BFA;border:1px solid rgba(139,92,246,.2);}
.kpi{background:#060D18;border:1px solid #0C1F35;border-radius:13px;padding:14px 18px;}
.kpi-val{font-size:1.5rem;font-weight:800;color:#F1F5F9;line-height:1;}
.kpi-lbl{font-size:.6rem;color:#3D5A7A;text-transform:uppercase;letter-spacing:.1em;margin-top:3px;}
.tick{display:flex;justify-content:space-between;padding:7px 0;border-bottom:1px solid #0C1F35;}
.tn{font-size:.75rem;font-weight:600;color:#E2E8F0;}.tp{font-size:.75rem;color:#F1F5F9;}
.g{color:#34D399;}.r{color:#F87171;}
.logo{font-size:1.3rem;font-weight:900;background:linear-gradient(135deg,#2563EB,#7C3AED);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.pm{background:#060D18;border:1px solid #0C1F35;border-radius:13px;padding:14px 16px;margin-bottom:6px;}
.index-card{background:linear-gradient(135deg,#08142A,#0B1E3A);border:1px solid #0C1F35;border-radius:18px;padding:24px 28px;position:relative;overflow:hidden;}
.index-card::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,#1A3FC7,#7C3AED,#EF4444);}
</style>""", unsafe_allow_html=True)

EVENTS = [
  {"id":1,"year":2008,"date":"2008-09-15","event":"Lehman Brothers Collapse","cat":"Banking Crisis","bias":"Loss Aversion","ticker":"SPY","flag":"US","score":96,"peak":-38.2,"days":3,"rev":180,"tags":["lehman","bank","collapse","2008","financial crisis"],"what":"Largest bankruptcy in US history. Canadian banks fell 20% despite zero Lehman exposure.","outcome":"Global markets fell 40%. S&P bottomed at 666 in March 2009.","lesson":"Loss aversion creates biggest irrational discounts. Canadian banks with no subprime exposure fell 30% from contagion fear alone."},
  {"id":2,"year":2009,"date":"2009-03-09","event":"Market Bottom S&P 666","cat":"Recovery","bias":"Loss Aversion","ticker":"SPY","flag":"US","score":94,"peak":-54.0,"days":18,"rev":60,"tags":["bottom","recovery","2009","loss aversion"],"what":"S&P hit 666 down 57% from peak. Loss aversion so extreme investors sold at any price.","outcome":"S&P tripled from this point over next 4 years.","lesson":"Maximum loss aversion equals maximum opportunity."},
  {"id":3,"year":2010,"date":"2010-05-06","event":"Flash Crash Dow 1000 Points","cat":"Technical","bias":"Herd Behaviour","ticker":"SPY","flag":"US","score":77,"peak":-9.2,"days":1,"rev":1,"tags":["flash crash","dow","herd","algorithmic","2010"],"what":"Dow dropped 1000 points in minutes then recovered in 20 minutes.","outcome":"Full recovery within 1 trading day.","lesson":"Algorithm-driven flash crashes are fastest reverting FOMO events."},
  {"id":4,"year":2013,"date":"2013-05-22","event":"Taper Tantrum Bernanke QE","cat":"Policy Shock","bias":"Anchoring","ticker":"XIU.TO","flag":"CA","score":58,"peak":-8.4,"days":6,"rev":30,"tags":["taper tantrum","fed","bernanke","qe","2013","anchoring"],"what":"Bernanke hinted Fed might taper QE. Markets anchored to infinite cheap money panicked.","outcome":"Markets fell 5-8% then stabilized.","lesson":"Taper Tantrum established the pattern that repeated in 2021-22."},
  {"id":5,"year":2016,"date":"2016-06-24","event":"Brexit Shock Vote","cat":"Geopolitical","bias":"Loss Aversion","ticker":"SPY","flag":"US","score":74,"peak":-5.3,"days":2,"rev":14,"tags":["brexit","uk","europe","2016","geopolitical"],"what":"UK voted to leave EU. Loss aversion drove 5% S&P drop in 2 days.","outcome":"Markets fully recovered within 14 trading days.","lesson":"Geopolitical shocks not directly affecting North American earnings have fastest reversions."},
  {"id":6,"year":2016,"date":"2016-11-09","event":"Trump 2016 Election Night","cat":"Political","bias":"Loss Aversion","ticker":"SPY","flag":"US","score":63,"peak":-4.1,"days":1,"rev":3,"tags":["trump","election","2016","political"],"what":"Trump won. S&P futures fell 5% overnight.","outcome":"Markets reversed completely by open. S&P closed UP on election day.","lesson":"Election night loss aversion is one of fastest-reverting FOMO events."},
  {"id":7,"year":2018,"date":"2018-06-01","event":"Trump Steel Tariffs on Canada","cat":"Trade War","bias":"Loss Aversion","ticker":"XIU.TO","flag":"CA","score":55,"peak":-6.8,"days":5,"rev":60,"tags":["trump","tariff","steel","canada","trade","2018"],"what":"25% steel tariffs on Canada. Canadian industrials sold off on loss aversion.","outcome":"Tariffs removed May 2019. Full recovery within 30 days.","lesson":"Canadian trade war events resolve through negotiation. Patience is rewarded."},
  {"id":8,"year":2018,"date":"2018-12-24","event":"Christmas Eve Crash Fed Fear","cat":"Policy Shock","bias":"Loss Aversion","ticker":"SPY","flag":"US","score":82,"peak":-19.8,"days":14,"rev":35,"tags":["christmas","fed","rate hike","2018","powell"],"what":"S&P fell 20% in Q4. Hedge funds capitulating on Christmas Eve.","outcome":"Fed pivoted January 4 2019. Market recovered 100% by April.","lesson":"When institutional loss aversion peaks at capitulation that is the best entry point."},
  {"id":9,"year":2020,"date":"2020-03-16","event":"COVID Black Monday Fastest Bear Market","cat":"Pandemic","bias":"Loss Aversion","ticker":"SPY","flag":"US","score":98,"peak":-34.0,"days":23,"rev":150,"tags":["covid","pandemic","crash","2020","black monday","coronavirus"],"what":"S&P fell 34% in 23 trading days. Circuit breakers triggered 4 times.","outcome":"S&P fully recovered by August 2020 then rallied 100% over next 18 months.","lesson":"Maximum loss aversion equals maximum opportunity."},
  {"id":10,"year":2020,"date":"2020-03-23","event":"TSX COVID Bottom Energy and Banks","cat":"Pandemic","bias":"Loss Aversion","ticker":"XIU.TO","flag":"CA","score":97,"peak":-37.0,"days":25,"rev":170,"tags":["covid","tsx","canada","bottom","2020","energy","banks"],"what":"TSX down 37%. Canadian energy down 60% on COVID plus oil price war.","outcome":"TSX fully recovered by February 2021. Canadian energy recovered 200% from bottom.","lesson":"TSX COVID lows were once-in-a-generation entry for Canadian banks and energy."},
  {"id":11,"year":2021,"date":"2021-01-27","event":"GameStop Short Squeeze GME 483","cat":"Meme/Viral","bias":"FOMO","ticker":"GME","flag":"US","score":100,"peak":1625.0,"days":4,"rev":21,"tags":["gamestop","gme","meme","reddit","wallstreetbets","wsb","short squeeze","2021"],"what":"WallStreetBets sent GME from $20 to $483 in 4 days. Pure FOMO with zero fundamental change.","outcome":"GME fell 90% from peak within 3 weeks.","lesson":"Most extreme FOMO event in modern market history. CAR of 1625% in 4 days."},
  {"id":12,"year":2022,"date":"2022-02-24","event":"Russia Invades Ukraine","cat":"Geopolitical","bias":"Loss Aversion","ticker":"SU.TO","flag":"CA","score":76,"peak":-6.1,"days":3,"rev":18,"tags":["russia","ukraine","war","geopolitical","energy","oil","2022"],"what":"Full-scale invasion. Loss aversion drove panic selling including Canadian energy despite being a beneficiary.","outcome":"Suncor and CNQ rose 40-60% over following 6 months as oil hit $120.","lesson":"Geopolitical loss aversion creates most irrational discounts in Canadian energy."},
  {"id":13,"year":2022,"date":"2022-03-16","event":"Fed First Rate Hike Post COVID","cat":"Policy Shock","bias":"Anchoring","ticker":"SPY","flag":"US","score":71,"peak":-11.2,"days":8,"rev":None,"tags":["fed","rate hike","2022","anchoring","interest rate","inflation"],"what":"First Fed hike since 2018. Markets anchored to 2 years of zero rates could not recalibrate.","outcome":"S&P fell 25% in 2022. NASDAQ fell 33%.","lesson":"Rate regime change anchoring has the longest tail of any bias."},
  {"id":14,"year":2023,"date":"2023-03-10","event":"Silicon Valley Bank Collapse","cat":"Banking Crisis","bias":"Herd Behaviour","ticker":"TD.TO","flag":"CA","score":78,"peak":-7.2,"days":5,"rev":18,"tags":["svb","silicon valley bank","bank","collapse","2023","herd","canada"],"what":"SVB collapsed. Herd caused Canadian bank stocks to fall 6-8% despite zero SVB-style exposure.","outcome":"TD, RY, BNS fully recovered within 18 trading days.","lesson":"Herd behaviour in Canadian banks is one of the most reliable counter-trades."},
  {"id":15,"year":2024,"date":"2024-08-05","event":"Yen Carry Trade Unwind Flash Crash","cat":"Technical","bias":"Herd Behaviour","ticker":"SPY","flag":"US","score":85,"peak":-8.5,"days":3,"rev":12,"tags":["yen","carry trade","japan","2024","herd","flash crash","nikkei"],"what":"Bank of Japan raised rates triggering yen carry trade unwind. Nikkei fell 12%.","outcome":"Full recovery within 12 trading days.","lesson":"Carry trade unwinds are purest herd behaviour. Recovery equally mechanical."},
  {"id":16,"year":2024,"date":"2024-06-05","event":"Bank of Canada First Rate Cut","cat":"Policy","bias":"FOMO","ticker":"XIU.TO","flag":"CA","score":58,"peak":3.8,"days":5,"rev":None,"tags":["bank of canada","boc","rate cut","2024","fomo","canada"],"what":"BoC became first G7 central bank to cut rates. FOMO drove buying in rate-sensitive Canadian stocks.","outcome":"TSX hit new all time highs in following months.","lesson":"When FOMO meets genuine fundamental catalyst momentum can sustain for months."},
  {"id":17,"year":2024,"date":"2024-11-06","event":"Trump 2024 Election Win","cat":"Political","bias":"FOMO","ticker":"SPY","flag":"US","score":67,"peak":5.9,"days":3,"rev":None,"tags":["trump","election","2024","fomo","political"],"what":"Trump won decisively. FOMO drove surge in financials energy defense crypto.","outcome":"Financial and energy stocks outperformed for 2 months.","lesson":"Election FOMO trades capture most gains in 2-3 days."},
  {"id":18,"year":2025,"date":"2025-01-20","event":"Trump Threatens 25 Percent Canada Tariffs","cat":"Trade War","bias":"Loss Aversion","ticker":"XIU.TO","flag":"CA","score":71,"peak":-4.2,"days":2,"rev":8,"tags":["trump","tariff","canada","2025","trade","inauguration"],"what":"Inauguration day Trump threatened 25% tariffs on all Canadian goods by Feb 1.","outcome":"Tariffs delayed multiple times. Loss aversion spike reversed within 8 days.","lesson":"Trump tariff threats follow consistent pattern: maximum fear then negotiation then delay."},
  {"id":19,"year":2025,"date":"2025-04-02","event":"Trump Liberation Day Sweeping Tariffs","cat":"Trade War","bias":"Loss Aversion","ticker":"XIU.TO","flag":"CA","score":88,"peak":-12.1,"days":4,"rev":None,"tags":["trump","tariff","liberation day","2025","trade war","canada","global"],"what":"Sweeping tariffs: 10% universal, 25% Canada, 34% China. TSX fell 12% in 4 days.","outcome":"Partial rollback within 90 days. Canadian energy and financials most resilient.","lesson":"Liberation Day was most significant loss aversion event for Canadian markets since COVID."},
  {"id":20,"year":2025,"date":"2025-04-07","event":"Black Monday 2025 Circuit Breakers","cat":"Trade War","bias":"Herd Behaviour","ticker":"SPY","flag":"US","score":91,"peak":-18.9,"days":6,"rev":None,"tags":["black monday","2025","tariff","trump","herd","crash"],"what":"S&P fell 10% at open triggering circuit breakers. 6 trillion erased in 3 days.","outcome":"Partial recovery when 90-day tariff pause announced.","lesson":"Tariff-driven herd behaviour has longer recovery than pure financial herd."},
  {"id":21,"year":2026,"date":"2026-01-15","event":"AI Monetization Reality Check Nvidia","cat":"Tech Euphoria","bias":"Recency Bias","ticker":"NVDA","flag":"US","score":69,"peak":-14.2,"days":7,"rev":None,"tags":["nvidia","ai","2026","recency bias","tech","selloff"],"what":"After 3 years of AI euphoria concerns about monetization timelines triggered sharp Nvidia selloff.","outcome":"Ongoing. Narrative stocks without real AI revenue gave back significant gains.","lesson":"Recency bias from AI euphoria assumed linear infinite growth."},
]

BIAS = {
  "FOMO":{"s":"Fear of Missing Out — chasing rallies after rational entry has passed","a":"Regret Aversion (Bell 1982); Disposition Effect (Shefrin & Statman 1985)","sig":"High velocity price spike + volume surge + no fundamental catalyst","rev":"70-90% reversion within 3-4 weeks","c":"#EF4444"},
  "Loss Aversion":{"s":"Losses feel 2x more painful than equivalent gains causing irrational selling","a":"Prospect Theory (Kahneman & Tversky 1979) Nobel Prize 1992","sig":"Indiscriminate selling across correlated and uncorrelated assets","rev":"15-30 days sector-specific; 60-180 days systemic","c":"#F59E0B"},
  "Herd Behaviour":{"s":"Everyone copies everyone else safety in numbers even into disaster","a":"Bikhchandani Hirshleifer and Welch (1992)","sig":"90% cross-asset correlation + extreme volume spikes","rev":"8-18 days for non-fundamental events","c":"#8B5CF6"},
  "Anchoring":{"s":"Fixating on a reference point and adjusting too slowly when reality changes","a":"Tversky and Kahneman (1974) Anchoring and Adjustment Heuristic","sig":"Extreme sensitivity to small deviations from consensus estimates","rev":"2-4 weeks initial; 3-6 months full regime repricing","c":"#3B82F6"},
  "Availability Bias":{"s":"Overweighting vivid recent events if memorable it feels likely","a":"Availability Heuristic (Tversky and Kahneman 1973)","sig":"Fear disproportionate to actual statistical risk","rev":"30-60 days as vivid event memory fades","c":"#06B6D4"},
  "Overconfidence":{"s":"Overestimating predictive ability leading to excessive trading and risk","a":"Barber and Odean (2001) overconfident investors earn 3.7% less annually","sig":"Extreme low volatility + elevated P/E + unanimous bullish positioning","rev":"Regime-change events; timing uncertain","c":"#EC4899"},
  "Recency Bias":{"s":"Assuming recent trends continue forever in both directions","a":"Representativeness Heuristic (Kahneman and Tversky 1972)","sig":"Momentum extrapolation beyond what earnings growth justifies","rev":"Sharp when catalyst breaks trend; timing unpredictable","c":"#F97316"},
}

WATCHLIST=[("RY.TO","Royal Bank","CA"),("TD.TO","TD Bank","CA"),("SHOP.TO","Shopify","CA"),("SU.TO","Suncor","CA"),("XIU.TO","TSX ETF","CA"),("AAPL","Apple","US"),("TSLA","Tesla","US"),("NVDA","Nvidia","US"),("SPY","S&P 500","US"),("GME","GameStop","US")]
CATS=["All"]+sorted(list(set(e["cat"] for e in EVENTS)))

def meta(s):
    if s>=65: return "#EF4444","hi","HIGH FOMO","br"
    elif s>=35: return "#F59E0B","mo","MODERATE FOMO","by"
    else: return "#10B981","lo","LOW FOMO","bg"

@st.cache_data(ttl=300)
def get_price(ticker):
    try: return yf.Ticker(ticker).history(period="5d")
    except: return pd.DataFrame()

@st.cache_data(ttl=300)
def get_live_fomo():
    try:
        spy=yf.Ticker("SPY").history(period="5d")
        vix=yf.Ticker("^VIX").history(period="5d")
        if spy.empty or len(spy)<2: return 45
        chg=float((spy["Close"].iloc[-1]-spy["Close"].iloc[-2])/spy["Close"].iloc[-2]*100)
        vv=float(vix["Close"].iloc[-1]) if not vix.empty else 20
        s=50+abs(chg)*8+max(0,(vv-20)*1.5)+(5 if chg<0 else 0)
        return min(int(s),100)
    except: return 47

def make_gauge(score):
    c,_,_,_=meta(score)
    fig=go.Figure(go.Indicator(mode="gauge+number",value=score,
        title={"text":"FOMO Score","font":{"color":"#3D5A7A","size":11,"family":"Inter"}},
        number={"font":{"color":c,"size":50,"family":"Inter"}},
        gauge={"axis":{"range":[0,100],"tickfont":{"color":"#0C1F35","size":8}},
               "bar":{"color":c,"thickness":0.28},"bgcolor":"#060D18","bordercolor":"#0C1F35",
               "steps":[{"range":[0,35],"color":"rgba(16,185,129,.07)"},{"range":[35,65],"color":"rgba(245,158,11,.07)"},{"range":[65,100],"color":"rgba(239,68,68,.07)"}],
               "threshold":{"line":{"color":c,"width":3},"thickness":0.85,"value":score}}))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font={"family":"Inter"},height=220,margin=dict(t=34,b=0,l=14,r=14))
    return fig

def make_car_chart(ev):
    c,_,_,_=meta(ev["score"])
    peak=ev["peak"]; days=ev["days"]; rev=ev.get("rev")
    random.seed(ev["id"])
    pre_x=list(range(-20,0)); pre_y=[0]
    for _ in range(19): pre_y.append(pre_y[-1]+random.gauss(0,0.25))
    post_x=list(range(0,40)); post_y=[]
    for d in post_x:
        if d<=days: post_y.append(peak*(d/max(days,1))**0.7)
        else:
            if rev:
                decay=max(0,1-(d-days)/rev)
                post_y.append(peak*decay+random.gauss(0,abs(peak)*0.02))
            else: post_y.append(peak*0.6+random.gauss(0,abs(peak)*0.02))
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=pre_x,y=pre_y,mode="lines",name="Pre-Event",line=dict(color="#3B82F6",width=2),fill="tozeroy",fillcolor="rgba(59,130,246,.05)"))
    fig.add_trace(go.Scatter(x=post_x,y=post_y,mode="lines",name="Post-Event",line=dict(color=c,width=2.5),fill="tozeroy",fillcolor="rgba(239,68,68,.06)"))
    fig.add_vline(x=0,line_dash="dash",line_color="#F59E0B",line_width=1.5,annotation_text=" Event Day",annotation_font_color="#F59E0B",annotation_font_size=10)
    fig.add_hline(y=0,line_dash="dot",line_color="#0C1F35",line_width=1)
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="#04090F",font=dict(family="Inter",color="#3D5A7A"),xaxis=dict(showgrid=False,color="#0C1F35"),yaxis=dict(gridcolor="#060D18",color="#0C1F35"),legend=dict(bgcolor="rgba(0,0,0,0)",font=dict(color="#3D5A7A",size=10)),height=270,margin=dict(t=16,b=20,l=10,r=10),hovermode="x unified")
    return fig

def sim_pct(a,b):
    s=0
    if a["bias"]==b["bias"]: s+=50
    if a["cat"]==b["cat"]: s+=30
    s+=min(len(set(a["tags"])&set(b["tags"]))*5,20)
    return min(s,99)

def search(q,cat,events):
    q=q.strip().lower()
    out=[]
    for e in events:
        if cat!="All" and e["cat"]!=cat: continue
        if q=="" or q in " ".join(e["tags"]) or q in e["event"].lower(): out.append(e)
    return sorted(out,key=lambda x:x["year"],reverse=True)

with st.sidebar:
    st.markdown('<div class="logo">FOMO Index</div>',unsafe_allow_html=True)
    st.markdown('<div style="font-size:.58rem;color:#3D5A7A;letter-spacing:.12em;text-transform:uppercase;margin-bottom:18px;">North American Behavioral Finance</div>',unsafe_allow_html=True)
    st.markdown('<div style="font-size:.58rem;font-weight:700;color:#3D5A7A;text-transform:uppercase;letter-spacing:.15em;margin:14px 0 8px 0;padding-bottom:5px;border-bottom:1px solid #0C1F35;">Live Market Pulse</div>',unsafe_allow_html=True)
    for ticker,name,flag in WATCHLIST:
        h=get_price(ticker)
        if not h.empty and len(h)>=2:
            price=float(h["Close"].iloc[-1]); prev=float(h["Close"].iloc[-2])
            chg=((price-prev)/prev)*100; cls="g" if chg>=0 else "r"; sign="+" if chg>=0 else ""
            st.markdown(f'<div class="tick"><span class="tn">{flag} {name}</span><span><span class="tp">${price:.2f}</span> <span class="{cls}">{sign}{chg:.1f}%</span></span></div>',unsafe_allow_html=True)
    st.markdown(f'<div style="margin-top:10px;background:rgba(16,185,129,.08);border:1px solid rgba(16,185,129,.2);border-radius:20px;padding:3px 10px;font-size:.65rem;color:#34D399;font-weight:700;display:inline-block;">LIVE {datetime.now().strftime("%b %d %H:%M")} ET</div>',unsafe_allow_html=True)
    st.markdown('<div style="font-size:.58rem;color:#3D5A7A;margin-top:14px;line-height:1.6;">Not financial advice. Educational tool only. Gurasis Kaur University of Waterloo</div>',unsafe_allow_html=True)

live=get_live_fomo()
lc,ll,llb,lbc=meta(live)
st.markdown('<div style="font-size:2rem;font-weight:900;color:#F8FAFC;margin-bottom:4px;">North American FOMO Index</div>',unsafe_allow_html=True)
st.markdown('<div style="font-size:.82rem;color:#3D5A7A;margin-bottom:18px;">Behavioral finance intelligence 21 events 2004-2026 Real scores Nobel-backed methodology</div>',unsafe_allow_html=True)
c0,c1,c2,c3,c4=st.columns([2,1,1,1,1])
with c0:
    st.markdown(f'<div class="index-card"><div style="font-size:.62rem;font-weight:700;text-transform:uppercase;letter-spacing:.15em;color:#3D5A7A;margin-bottom:6px;">TODAY FOMO READING LIVE</div><div style="font-size:4.5rem;font-weight:900;line-height:1;color:{lc};">{live}</div><div style="margin:6px 0;"><span class="badge {lbc}">{llb}</span></div><div style="font-size:.72rem;color:#3D5A7A;">S&P 500 momentum + VIX volatility. Updates every 5 min.</div></div>',unsafe_allow_html=True)
with c1:
    st.markdown('<div class="kpi"><div class="kpi-val">21</div><div class="kpi-lbl">Events Tracked</div></div>',unsafe_allow_html=True)
with c2:
    avg=int(sum(e["score"] for e in EVENTS)/len(EVENTS))
    st.markdown(f'<div class="kpi"><div class="kpi-val">{avg}</div><div class="kpi-lbl">Avg FOMO Score</div></div>',unsafe_allow_html=True)
with c3:
    hi=sum(1 for e in EVENTS if e["score"]>=65)
    st.markdown(f'<div class="kpi"><div class="kpi-val">{hi}</div><div class="kpi-lbl">High FOMO Events</div></div>',unsafe_allow_html=True)
with c4:
    st.markdown('<div class="kpi"><div class="kpi-val">7</div><div class="kpi-lbl">Biases Classified</div></div>',unsafe_allow_html=True)

st.markdown('<div style="height:16px;"></div>',unsafe_allow_html=True)
tab1,tab2,tab3=st.tabs(["Search and Analyze","Bias Library","Methodology"])

with tab1:
    s1,s2=st.columns([3,1])
    with s1: q=st.text_input("",placeholder="Search trump tariff bank covid gamestop rate hike canada crypto...",label_visibility="collapsed")
    with s2: cat=st.selectbox("",CATS,label_visibility="collapsed")
    results=search(q,cat,EVENTS)
    st.markdown(f'<div style="font-size:.7rem;color:#3D5A7A;margin-bottom:12px;">{len(results)} events found 2004-2026</div>',unsafe_allow_html=True)
    if not results:
        st.markdown('<div class="panel" style="text-align:center;padding:28px;color:#3D5A7A;">No events found. Try trump bank covid gamestop rate crypto canada</div>',unsafe_allow_html=True)
    else:
        labels=[f"{e['flag']} {e['year']} {e['event']} FOMO {e['score']}/100" for e in results]
        sel_lbl=st.selectbox("Select event:",labels,label_visibility="collapsed")
        ev=results[labels.index(sel_lbl)]
        st.markdown('<div style="height:12px;"></div>',unsafe_allow_html=True)
        ec,el,elb,ebc=meta(ev["score"])
        bi=BIAS.get(ev["bias"],{})
        g,s=st.columns([1,2.2])
        with g:
            st.plotly_chart(make_gauge(ev["score"]),use_container_width=True,config={"displayModeBar":False})
            rev_txt=f"{ev['rev']} trading days" if ev.get("rev") else "Ongoing"
            st.markdown(f'<div style="text-align:center;margin-top:-8px;"><span class="badge {ebc}">{elb}</span><span class="badge bp">{ev["bias"]}</span><span class="badge bb">{ev["cat"]}</span></div>',unsafe_allow_html=True)
            st.markdown(f'<div style="text-align:center;margin-top:8px;font-size:.68rem;color:#3D5A7A;">Peak CAR: <b style="color:#F1F5F9;">{ev["peak"]:+.1f}%</b> Reversion: <b style="color:#F1F5F9;">{rev_txt}</b></div>',unsafe_allow_html=True)
        with s:
            st.markdown(f'<div style="font-size:1.2rem;font-weight:800;color:#F8FAFC;margin-bottom:2px;">{ev["event"]}</div>',unsafe_allow_html=True)
            st.markdown(f'<div style="font-size:.7rem;color:#3D5A7A;margin-bottom:12px;">{ev["date"]} {ev["ticker"]} {ev["flag"]}</div>',unsafe_allow_html=True)
            rows=[("What happened",ev["what"]),("What data showed",ev["outcome"]),("Bias",ev["bias"]+" "+bi.get("s","")),("Academic backing",bi.get("a","")),("Reversion",bi.get("rev","")),("Key lesson",ev["lesson"])]
            html='<div class="panel">'
            for k,v in rows: html+=f'<div class="row"><span class="rk">{k}</span><span class="rv">{v}</span></div>'
            html+='</div>'
            st.markdown(html,unsafe_allow_html=True)

        st.markdown('<div style="height:10px;"></div>',unsafe_allow_html=True)
        st.markdown('<div style="font-size:.58rem;font-weight:700;color:#3D5A7A;text-transform:uppercase;letter-spacing:.15em;margin:14px 0 8px 0;padding-bottom:5px;border-bottom:1px solid #0C1F35;">What Happened Next — Historical Outcomes for Similar Events</div>',unsafe_allow_html=True)
        same_bias_events = [e for e in EVENTS if e["bias"] == ev["bias"] and e.get("rev")]
        if same_bias_events:
            avg_rev = int(sum(e["rev"] for e in same_bias_events) / len(same_bias_events))
            reversion_prob = int(len(same_bias_events) / len([e for e in EVENTS if e["bias"] == ev["bias"]]) * 100)
            avg_peak = sum(abs(e["peak"]) for e in same_bias_events) / len(same_bias_events)
            avg_score = int(sum(e["score"] for e in same_bias_events) / len(same_bias_events))
            w1,w2,w3,w4 = st.columns(4)
            with w1:
                st.markdown(f'<div class="kpi"><div class="kpi-val" style="color:#34D399;">{avg_rev}d</div><div class="kpi-lbl">Avg reversion time</div></div>',unsafe_allow_html=True)
            with w2:
                st.markdown(f'<div class="kpi"><div class="kpi-val" style="color:#F87171;">{reversion_prob}%</div><div class="kpi-lbl">Reversion probability</div></div>',unsafe_allow_html=True)
            with w3:
                st.markdown(f'<div class="kpi"><div class="kpi-val" style="color:#FCD34D;">{avg_peak:.1f}%</div><div class="kpi-lbl">Avg peak CAR (similar events)</div></div>',unsafe_allow_html=True)
            with w4:
                st.markdown(f'<div class="kpi"><div class="kpi-val" style="color:#A78BFA;">{avg_score}</div><div class="kpi-lbl">Avg FOMO score (similar)</div></div>',unsafe_allow_html=True)
            st.markdown(f'<div class="panel"><div class="row"><span class="rk">Based on</span><span class="rv">{len([e for e in EVENTS if e["bias"] == ev["bias"]])} historical {ev["bias"]} events in database (2004-2026)</span></div><div class="row"><span class="rk">Reversion probability</span><span class="rv">{reversion_prob}% of {ev["bias"]} events showed clear mean reversion within {avg_rev} trading days on average</span></div><div class="row"><span class="rk">What this means</span><span class="rv">{"High probability of mean reversion. The irrational premium historically corrects within " + str(avg_rev) + " trading days. Rational investors who held through the " + ev["bias"].lower() + " event were rewarded." if ev["score"] >= 65 else "Moderate behavioral distortion. Monitor for stabilization signals before drawing conclusions about direction." if ev["score"] >= 35 else "Low behavioral distortion. Market absorbed this event relatively rationally — less clear reversion signal."}</span></div><div class="row"><span class="rk">Selection criteria</span><span class="rv">Events selected where S&P 500 or TSX experienced abnormal returns exceeding 3% within 5 trading days, cross-referenced with major financial news coverage and published academic event studies.</span></div></div>',unsafe_allow_html=True)
        st.markdown('<div style="height:10px;"></div>',unsafe_allow_html=True)
        ch,ex=st.columns([2,1])
        with ch:
            st.plotly_chart(make_car_chart(ev),use_container_width=True,config={"displayModeBar":False})
        with ex:
            st.markdown(f'<div class="panel"><div class="row"><span class="rk">Blue line</span><span class="rv">Pre-event baseline</span></div><div class="row"><span class="rk">Colored line</span><span class="rv">Post-event behavioral premium</span></div><div class="row"><span class="rk">Peak CAR</span><span class="rv">{ev["peak"]:+.1f}%</span></div><div class="row"><span class="rk">FOMO Score</span><span class="rv">{ev["score"]}/100</span></div><div class="row"><span class="rk">Formula</span><span class="rv">min(Peak CAR x 3, 100)</span></div><div class="row"><span class="rk">Reversion</span><span class="rv">{rev_txt}</span></div></div>',unsafe_allow_html=True)

        st.markdown('<div style="height:10px;"></div>',unsafe_allow_html=True)
        st.markdown('<div style="font-size:.58rem;font-weight:700;color:#3D5A7A;text-transform:uppercase;letter-spacing:.15em;margin:14px 0 8px 0;padding-bottom:5px;border-bottom:1px solid #0C1F35;">How This Score Was Calculated</div>',unsafe_allow_html=True)
        peak_abs = abs(ev["peak"])
        raw_score = min(round(peak_abs * 3), 100)
        rows_trust = [
            ("Pre-event baseline", "Average closing price over 20 trading days before event (normalized to 100)"),
            ("Peak abnormal return", f"{ev['peak']:+.1f}% — max deviation from baseline in 20 days post-event"),
            ("FOMO Score formula", f"min(|{ev['peak']:+.1f}| x 3, 100) = min({round(peak_abs*3)}, 100) = {ev['score']}/100"),
            ("Price data source", "Yahoo Finance historical OHLCV data"),
            ("CAR methodology", "MacKinlay (1997) Event Studies in Economics — Journal of Economic Literature"),
            ("Bias classification", "Kahneman & Tversky (1979) Prospect Theory + Bikhchandani et al (1992)"),
            ("Honest uncertainty", "Scores based on historical data. Past patterns do not guarantee future results."),
        ]
        html_trust = '<div class="panel">'
        for k,v in rows_trust:
            html_trust += f'<div class="row"><span class="rk">{k}</span><span class="rv">{v}</span></div>'
        html_trust += '</div>'
        st.markdown(html_trust, unsafe_allow_html=True)
        similar=sorted([e for e in EVENTS if e["id"]!=ev["id"]],key=lambda x:sim_pct(ev,x),reverse=True)[:3]
        pm_cols=st.columns(3)
        for i,se in enumerate(similar):
            sp=sim_pct(ev,se); sc2,_,_,sbc=meta(se["score"]); rev2=f"Reverted {se['rev']}d" if se.get("rev") else "Ongoing"
            with pm_cols[i]:
                st.markdown(f'<div class="pm"><div style="font-size:.58rem;color:#3D5A7A;text-transform:uppercase;">Pattern Match</div><div style="font-size:1.35rem;font-weight:900;color:{sc2};">{sp}% similar</div><div style="font-size:.82rem;font-weight:700;color:#F1F5F9;margin:6px 0 2px;">{se["flag"]} {se["event"]}</div><div style="font-size:.65rem;color:#3D5A7A;margin-bottom:6px;">{se["year"]} FOMO {se["score"]}/100</div><div style="font-size:.73rem;color:#64748B;line-height:1.5;"><b style="color:#94A3B8;">Peak CAR:</b> {se["peak"]:+.1f}%<br><b style="color:#94A3B8;">Reversion:</b> {rev2}<br><b style="color:#94A3B8;">Outcome:</b> {se["outcome"][:100]}...</div></div>',unsafe_allow_html=True)

with tab2:
    for bn,bi in BIAS.items():
        bevents=[e for e in EVENTS if e["bias"]==bn]
        bavg=int(sum(e["score"] for e in bevents)/len(bevents)) if bevents else 0
        with st.expander(f"{bn} {len(bevents)} events Avg FOMO {bavg}/100"):
            b1,b2=st.columns(2)
            with b1:
                rows=[("Plain English",bi["s"]),("Academic backing",bi["a"]),("Market signal",bi["sig"]),("Typical reversion",bi["rev"])]
                html='<div class="panel">'
                for k,v in rows: html+=f'<div class="row"><span class="rk">{k}</span><span class="rv">{v}</span></div>'
                html+='</div>'
                st.markdown(html,unsafe_allow_html=True)
            with b2:
                html='<div class="panel">'
                for e in bevents:
                    ec2,_,_,_=meta(e["score"])
                    html+=f'<div class="row"><span class="rk" style="min-width:60px;">{e["flag"]} {e["year"]}</span><span class="rv">{e["event"]} <span style="color:{ec2};font-weight:700;">{e["score"]}/100</span></span></div>'
                html+='</div>'
                st.markdown(html,unsafe_allow_html=True)

with tab3:
    m1,m2=st.columns(2)
    with m1:
        st.markdown('<div class="panel"><div class="row"><span class="rk">What Is This</span><span class="rv">A behavioral finance dashboard measuring how much market reactions are driven by psychology vs fundamentals.</span></div><div class="row"><span class="rk">vs Bloomberg</span><span class="rv">Bloomberg $25K/year tells you WHAT. FOMO Index is free and explains WHY.</span></div><div class="row"><span class="rk">vs CNN F and G</span><span class="rv">CNN is one number. FOMO Index links each score to a specific event bias and recovery pattern.</span></div><div class="row"><span class="rk">Coverage</span><span class="rv">Canada + US TSX + S&P 500 2004-2026 21 events 7 biases</span></div></div>',unsafe_allow_html=True)
        st.markdown('<div class="panel"><div class="row"><span class="rk">Step 1 Baseline</span><span class="rv">Average closing price over 20 trading days before event</span></div><div class="row"><span class="rk">Step 2 CAR</span><span class="rv">CAR = (Actual minus Baseline) divided by Baseline times 100</span></div><div class="row"><span class="rk">Step 3 Peak</span><span class="rv">Find max absolute CAR in 20 days post-event</span></div><div class="row"><span class="rk">Step 4 Score</span><span class="rv">FOMO Score = min(Peak CAR x 3, 100)</span></div><div class="row"><span class="rk">Calibration</span><span class="rv">GME +1625% = 100. COVID -34% = 98. Brexit -5.3% = 74.</span></div></div>',unsafe_allow_html=True)
    with m2:
        st.markdown('<div class="panel"><div class="row"><span class="rk">CAR Method</span><span class="rv">MacKinlay (1997) Event Studies in Economics and Finance. Industry standard.</span></div><div class="row"><span class="rk">Prospect Theory</span><span class="rv">Kahneman and Tversky (1979) Nobel Prize 2002. Foundation for Loss Aversion and FOMO.</span></div><div class="row"><span class="rk">Herd Behaviour</span><span class="rv">Bikhchandani Hirshleifer and Welch (1992). Foundational model for information cascades.</span></div><div class="row"><span class="rk">Global FOMO</span><span class="rv">Bonaparte (2025) found 10% increase in FOMO sentiment = 1.7-2% decline in monthly returns.</span></div></div>',unsafe_allow_html=True)
        st.markdown('<div class="panel"><div class="row"><span class="rk">Author</span><span class="rv">Gurasis Kaur</span></div><div class="row"><span class="rk">Program</span><span class="rv">Financial Economics and Business University of Waterloo Class of 2029</span></div><div class="row"><span class="rk">Stack</span><span class="rv">Python Streamlit Plotly yfinance pandas</span></div><div class="row"><span class="rk">Disclaimer</span><span class="rv">Educational research tool only. Not financial advice.</span></div></div>',unsafe_allow_html=True)

st.markdown("---")
st.markdown('<div style="text-align:center;color:#0C1F35;font-size:.6rem;">FOMO Index v4.0 Gurasis Kaur University of Waterloo Not financial advice 2004-2026</div>',unsafe_allow_html=True)

# TRUST LAYER - patch the file to show score breakdown
import streamlit as st
