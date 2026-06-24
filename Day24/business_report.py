from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.graphics.shapes import Drawing, Rect, String, Circle, Line, Wedge, Arrow
import math

# ── Palette ──────────────────────────────────────────────────────────────────
NAVY   = colors.HexColor("#0D1B2A")
INDIGO = colors.HexColor("#1B3A6B")
BLUE   = colors.HexColor("#2563EB")
TEAL   = colors.HexColor("#0EA5E9")
GREEN  = colors.HexColor("#10B981")
AMBER  = colors.HexColor("#F59E0B")
RED    = colors.HexColor("#EF4444")
PURPLE = colors.HexColor("#7C3AED")
LGBG   = colors.HexColor("#F0F4FF")
LGRAY  = colors.HexColor("#F8FAFC")
MGRAY  = colors.HexColor("#E2E8F0")
DGRAY  = colors.HexColor("#64748B")
WHITE  = colors.white
BLACK  = colors.HexColor("#0F172A")

PAGE_W, PAGE_H = A4
M  = 1.6 * cm
CW = PAGE_W - 2 * M

def S(name, **kw): return ParagraphStyle(name, **kw)

sTitle = S("T",  fontSize=26, textColor=WHITE,  fontName="Helvetica-Bold",  leading=32, alignment=TA_CENTER)
sSub   = S("Su", fontSize=10, textColor=colors.HexColor("#93C5FD"), fontName="Helvetica", leading=14, alignment=TA_CENTER)
sTag   = S("Tg", fontSize=8,  textColor=colors.HexColor("#CBD5E1"), fontName="Helvetica-Oblique", leading=12, alignment=TA_CENTER)
sH1    = S("H1", fontSize=11, textColor=WHITE,  fontName="Helvetica-Bold",  leading=15)
sH2    = S("H2", fontSize=10, textColor=INDIGO, fontName="Helvetica-Bold",  leading=13)
sH3    = S("H3", fontSize=9,  textColor=BLUE,   fontName="Helvetica-Bold",  leading=12)
sBody  = S("B",  fontSize=8.5,textColor=BLACK,  fontName="Helvetica",       leading=13, alignment=TA_JUSTIFY)
sBul   = S("Bu", fontSize=8.5,textColor=BLACK,  fontName="Helvetica",       leading=13, leftIndent=12, firstLineIndent=-12)
sTH    = S("TH", fontSize=8,  textColor=WHITE,  fontName="Helvetica-Bold",  leading=11, alignment=TA_CENTER)
sTC    = S("TC", fontSize=8,  textColor=BLACK,  fontName="Helvetica",       leading=12, alignment=TA_LEFT)
sTCC   = S("TCC",fontSize=8,  textColor=BLACK,  fontName="Helvetica",       leading=12, alignment=TA_CENTER)
sSmall = S("Sm", fontSize=7,  textColor=DGRAY,  fontName="Helvetica",       leading=10)
sWht   = S("Wh", fontSize=9,  textColor=WHITE,  fontName="Helvetica",       leading=13)
sWhtB  = S("WhB",fontSize=9,  textColor=WHITE,  fontName="Helvetica-Bold",  leading=13)

def sp(h=6): return Spacer(1, h)
def hr(): return HRFlowable(width="100%", thickness=0.4, color=MGRAY, spaceAfter=4, spaceBefore=4)

def banner(title, sub=""):
    d = Drawing(CW, 34)
    d.add(Rect(0, 0, CW, 34, fillColor=INDIGO, strokeColor=None))
    d.add(Rect(0, 0, 4, 34, fillColor=BLUE,   strokeColor=None))
    d.add(String(12, 13, title, fontName="Helvetica-Bold", fontSize=11, fillColor=WHITE))
    if sub:
        d.add(String(12, 4, sub, fontName="Helvetica-Oblique", fontSize=7,
                     fillColor=colors.HexColor("#93C5FD")))
    return d

def callout(text, bg=LGBG, border=BLUE):
    t = Table([[Paragraph(text, sBody)]], colWidths=[CW - 2])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), bg),
        ("BOX",(0,0),(-1,-1), 0.5, border),
        ("LEFTPADDING",(0,0),(-1,-1),10), ("RIGHTPADDING",(0,0),(-1,-1),10),
        ("TOPPADDING",(0,0),(-1,-1),8),   ("BOTTOMPADDING",(0,0),(-1,-1),8),
        ("LINEBEFORETABLE",(0,0),(0,-1), 3, border),
    ]))
    return t

def tbl(headers, rows, cw=None, stripe=True, hdr_color=INDIGO):
    data = [[Paragraph(h, sTH) for h in headers]]
    for row in rows:
        data.append([Paragraph(str(c), sTCC if i > 0 else sTC)
                     for i, c in enumerate(row)])
    if not cw:
        cw = [CW / len(headers)] * len(headers)
    t = Table(data, colWidths=cw, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0), hdr_color),
        ("GRID",(0,0),(-1,-1), 0.35, MGRAY),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [WHITE, LGBG] if stripe else [WHITE]),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("LEFTPADDING",(0,0),(-1,-1),7), ("RIGHTPADDING",(0,0),(-1,-1),7),
        ("TOPPADDING",(0,0),(-1,-1),6),  ("BOTTOMPADDING",(0,0),(-1,-1),6),
    ]))
    return t

def score_bar(label, val, mx, clr):
    bw = CW - 175
    pct = val / mx
    d = Drawing(bw, 14)
    d.add(Rect(0, 3, bw, 8, fillColor=MGRAY, strokeColor=None))
    d.add(Rect(0, 3, bw * pct, 8, fillColor=clr, strokeColor=None))
    xpos = min(bw * pct + 3, bw - 30)
    d.add(String(xpos, 4, f"{val}/100", fontName="Helvetica-Bold", fontSize=7, fillColor=BLACK))
    row = Table([[Paragraph(label, sBody), d]], colWidths=[170, bw])
    row.setStyle(TableStyle([
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("TOPPADDING",(0,0),(-1,-1),4), ("BOTTOMPADDING",(0,0),(-1,-1),4),
        ("LEFTPADDING",(0,0),(-1,-1),4), ("RIGHTPADDING",(0,0),(-1,-1),4),
        ("ROWBACKGROUNDS",(0,0),(-1,-1),[WHITE]),
    ]))
    return row

def metric_strip(items):
    cw = CW / len(items)
    cells = []
    for label, val, clr in items:
        d = Drawing(cw - 8, 52)
        d.add(Rect(0, 0, cw-8, 52, fillColor=LGBG, strokeColor=MGRAY, strokeWidth=0.5))
        d.add(Rect(0, 48, cw-8, 4,  fillColor=clr, strokeColor=None))
        d.add(String((cw-8)/2, 24, val, fontName="Helvetica-Bold", fontSize=14,
                     fillColor=clr, textAnchor="middle"))
        d.add(String((cw-8)/2, 8, label, fontName="Helvetica", fontSize=6.5,
                     fillColor=DGRAY, textAnchor="middle"))
        cells.append(d)
    t = Table([cells], colWidths=[cw]*len(items))
    t.setStyle(TableStyle([("LEFTPADDING",(0,0),(-1,-1),3),("RIGHTPADDING",(0,0),(-1,-1),3),
                            ("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3)]))
    return t

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — COVER
# ═══════════════════════════════════════════════════════════════════════════════
def cover():
    el = []
    hero = Drawing(CW, 200)
    hero.add(Rect(0, 0, CW, 200, fillColor=NAVY, strokeColor=None))
    hero.add(Rect(0, 0, CW, 4,   fillColor=BLUE, strokeColor=None))
    hero.add(Rect(0, 196, CW, 4, fillColor=TEAL, strokeColor=None))
    hero.add(Circle(CW-50, 165, 65, fillColor=colors.HexColor("#1E3A8A"), strokeColor=None))
    hero.add(Circle(CW-50, 165, 38, fillColor=INDIGO, strokeColor=None))
    # Dollar signs decorative
    for i, (x, y, sz) in enumerate([(40,170,20),(80,140,14),(20,130,10)]):
        hero.add(String(x, y, "$", fontName="Helvetica-Bold", fontSize=sz,
                        fillColor=colors.HexColor("#1E40AF")))
    el.append(hero)
    cover_t = Table([
        [Paragraph("AI CO-FOUNDER BUSINESS STRATEGY REPORT", sTitle)],
        [Paragraph("AI Career Mentor for Students — India Market", sSub)],
        [sp(4)],
        [Paragraph("Source: Customer &amp; MVP Blueprint (Day 23) &nbsp;|&nbsp; June 2025", sTag)],
        [Paragraph("Prepared by AI Co-Founder &amp; Growth Strategy Engine", sTag)],
    ], colWidths=[CW])
    cover_t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), NAVY),
        ("TOPPADDING",(0,0),(-1,-1),8), ("BOTTOMPADDING",(0,0),(-1,-1),8),
        ("LEFTPADDING",(0,0),(-1,-1),16), ("RIGHTPADDING",(0,0),(-1,-1),16),
    ]))
    el.append(cover_t)
    el.append(sp(14))
    el.append(metric_strip([
        ("Business Viability",  "68/100", BLUE),
        ("Revenue Potential",   "72/100", GREEN),
        ("GTM Strength",        "55/100", AMBER),
        ("Competitive Strength","58/100", TEAL),
        ("Investor Readiness",  "38/100", RED),
        ("OVERALL",             "58/100", PURPLE),
    ]))
    el.append(sp(12))
    el.append(callout(
        "<b>Co-Founder Verdict: 🟡 VALIDATE BEFORE SCALING</b> — The AI Career Mentor has genuine "
        "business potential in a large underserved market. The problem is real, the timing is excellent, "
        "and the white space is clear. However, the business cannot be called investable today: "
        "zero revenue validation, unproven willingness-to-pay, and no distribution engine. "
        "Execute the 30-day sprint, hit the 5 gates, then return to investors.",
        bg=colors.HexColor("#FFF7ED"), border=AMBER))
    el.append(PageBreak())
    return el

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — TABLE OF CONTENTS
# ═══════════════════════════════════════════════════════════════════════════════
def toc():
    el = []
    el.append(banner("TABLE OF CONTENTS"))
    el.append(sp(10))
    items = [
        ("1", "Startup Summary (10 Bullets)", "3"),
        ("2", "Business Reality Check", "3"),
        ("3", "Executive Summary", "4"),
        ("4", "Business Model Canvas", "5"),
        ("5", "Revenue & Pricing Strategy", "5"),
        ("6", "Go-To-Market Strategy", "6"),
        ("7", "Customer Acquisition Strategy", "6"),
        ("8", "First 100 Users Plan", "7"),
        ("9", "Competitive Position & Moat", "7"),
        ("10","Reverse SWOT Analysis", "8"),
        ("11","Investor One-Liner & 30-Second Pitch", "8"),
        ("12","Investment Scorecard (0–100)", "9"),
        ("13","Visual Dashboard", "9"),
        ("14","Founder Action Sheet (Top 10)", "10"),
        ("15","Sustainability Verdict", "10"),
    ]
    rows = [[Paragraph(f"<b>{n}.</b> {title}", sBody),
             Paragraph(pg, S("pg", fontSize=9, alignment=TA_RIGHT, textColor=BLUE,
                              fontName="Helvetica-Bold"))]
            for n, title, pg in items]
    t = Table(rows, colWidths=[CW-30, 30])
    t.setStyle(TableStyle([
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7),
        ("LINEBELOW",(0,0),(-1,-1),0.3,MGRAY),
        ("ROWBACKGROUNDS",(0,0),(-1,-1),[WHITE, LGBG]),
    ]))
    el.append(t)
    el.append(PageBreak())
    return el

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — STARTUP SUMMARY + REALITY CHECK
# ═══════════════════════════════════════════════════════════════════════════════
def summary_reality():
    el = []

    # ── 10 Bullet Summary ──
    el.append(banner("1. STARTUP SUMMARY", "Extracted from Customer & MVP Blueprint"))
    el.append(sp(8))
    bullets = [
        ("<b>Idea:</b>", "AI-powered personalised career mentorship platform for Indian college students — delivering roadmaps, skill-gap analysis, and internship readiness."),
        ("<b>Problem:</b>", "43M+ Indian students have no affordable, personalised career guidance. College placement cells are generic; human mentors cost Rs.2,000+/session."),
        ("<b>Target Customer:</b>", "19–23 yr B2C students (primary) at Tier-1/2 Indian cities + college placement departments as B2B secondary buyers."),
        ("<b>Core Value Prop:</b>", "The only AI that gives you a personalised 12-week career roadmap — skills, projects, and certifications — matched to your degree, goal, and timeline."),
        ("<b>MVP:</b>", "Single flow: 5-question onboarding quiz → AI-generated 12-week roadmap → weekly progress tracker → freemium gate at week 3."),
        ("<b>Competitors:</b>", "LinkedIn Learning, Internshala, Unstop, ChatGPT/Gemini. No one owns the end-to-end 'career OS for students' position in India."),
        ("<b>Revenue Model:</b>", "Freemium B2C (Rs.0/99/299/mo) + B2B institutional licensing (Rs.2L/yr per college)."),
        ("<b>Pricing Hypothesis:</b>", "Rs.99/mo Pro tier is primary revenue driver. B2B college licensing is the path to meaningful revenue scale."),
        ("<b>Validation Status:</b>", "Observational only — zero interviews, no MVP, no waitlist. MVP Readiness score: 30/100."),
        ("<b>Stage &amp; Next Step:</b>", "Pre-product. Run 30-day validation sprint (50 interviews + landing page + 100 waitlist signups) before writing any code."),
    ]
    for bold, text in bullets:
        el.append(Paragraph(f"• {bold} {text}", sBul))
        el.append(sp(3))
    el.append(sp(10))

    # ── Business Reality Check ──
    el.append(banner("2. BUSINESS REALITY CHECK", "Revenue over vanity. Evidence over assumptions."))
    el.append(sp(8))

    reality = [
        ["Question", "Honest Answer", "Risk Level"],
        ["Who pays?",
         "Students (Rs.99–299/mo) IF they see clear ROI.\nColleges (Rs.2L/yr) IF placement rates improve.",
         "🟠 High — both are price-sensitive or slow-moving"],
        ["Why do they pay?",
         "Students: career anxiety + no affordable alternative.\nColleges: placement rate KPI pressure.",
         "🟡 Medium — motivation exists but unvalidated"],
        ["How will they discover it?",
         "No distribution engine defined yet.\nAssuming organic social + WhatsApp groups — unproven.",
         "🔴 Critical — biggest unvalidated assumption"],
        ["Biggest growth risk?",
         "ChatGPT adds career UX. Students choose free general AI over paid vertical tool.",
         "🔴 Critical — no current moat against this"],
        ["Biggest monetisation risk?",
         "Students won't pay Rs.99/mo consistently.\nB2B college sales cycle is 3–9 months.",
         "🔴 Critical — both revenue streams slow to validate"],
        ["Weakest assumptions?",
         "1. Students will pay for career AI\n2. Word-of-mouth replaces paid CAC\n3. Colleges will pilot within 30 days\n4. AI roadmap quality is good enough to retain",
         "🔴 Critical — all 4 must be tested immediately"],
    ]
    el.append(tbl(reality[0], reality[1:], cw=[110, 230, CW-340]))
    el.append(PageBreak())
    return el

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — EXECUTIVE SUMMARY
# ═══════════════════════════════════════════════════════════════════════════════
def exec_summary():
    el = []
    el.append(banner("3. EXECUTIVE SUMMARY", "The honest case for this business"))
    el.append(sp(8))
    el.append(Paragraph("The Opportunity", sH2))
    el.append(sp(4))
    el.append(Paragraph(
        "India has 43M+ college students, the majority of whom receive no meaningful career guidance. "
        "Human mentors are unaffordable (Rs.2,000+/session). Job platforms are reactive, not proactive. "
        "AI tools like ChatGPT are capable but lack structured career UX and India-specific data. "
        "The window is open for a vertically focused, AI-first career platform to own this space — "
        "but only if it moves fast and validates before competitors close the gap.", sBody))
    el.append(sp(8))
    el.append(Paragraph("The Business Case", sH2))
    el.append(sp(4))
    biz_rows = [
        ["Dimension", "Assessment", "Confidence"],
        ["Problem Reality",    "Real, large, daily pain for students",              "High"],
        ["Market Size",        "SAM $380M India; TAM $4.5B global",                "Medium"],
        ["Revenue Path",       "Freemium → Pro conversion + B2B licensing",        "Low — unvalidated"],
        ["Distribution",       "Organic social, WA groups, college partnerships",  "Low — untested"],
        ["Competition",        "Gap exists but ChatGPT is fast-moving threat",     "Medium"],
        ["Team Readiness",     "Observational insight; no technical co-founder yet","Low"],
        ["Capital Efficiency", "Can validate with <$500 (landing page + interviews)","High"],
        ["Timing",             "AI adoption peak + India digital boom = good timing","High"],
    ]
    el.append(tbl(biz_rows[0], biz_rows[1:], cw=[130, 210, CW-340]))
    el.append(sp(8))
    el.append(Paragraph("Why This Can Work", sH2))
    el.append(sp(4))
    for pt in [
        "The problem is <b>emotional</b> (career anxiety) + <b>economic</b> (job outcomes) — dual motivation to pay.",
        "The B2B college channel provides a <b>distribution shortcut</b> — one contract = 500–5,000 users.",
        "India's engineering student market is <b>highly networked</b> — viral growth via WhatsApp is plausible.",
        "A <b>no-code MVP</b> can be built for &lt;Rs.50,000, keeping burn near zero during validation.",
        "Institutional B2B (placement cells) provides <b>predictable, recurring revenue</b> vs. high-churn B2C.",
    ]:
        el.append(Paragraph(f"• {pt}", sBul))
        el.append(sp(3))
    el.append(sp(8))
    el.append(Paragraph("Why This Can Fail", sH2))
    el.append(sp(4))
    for pt in [
        "<b>ChatGPT adds career UX</b> — free tool with 100M users is a permanent threat.",
        "<b>Students don't pay</b> — Rs.99/mo is affordable but habit formation for a 'career tool' is weak.",
        "<b>No co-founder / team</b> — single founder building AI product is high execution risk.",
        "<b>B2B sales are slow</b> — college bureaucracy makes 30-day pilot targets unrealistic.",
        "<b>AI quality</b> — if roadmap advice is generic or wrong, retention collapses in week 2.",
    ]:
        el.append(Paragraph(f"• {pt}", sBul))
        el.append(sp(3))
    el.append(PageBreak())
    return el

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 5 — BMC + REVENUE
# ═══════════════════════════════════════════════════════════════════════════════
def bmc_revenue():
    el = []

    # ── BMC ──
    el.append(banner("4. BUSINESS MODEL CANVAS", "9-block strategic overview"))
    el.append(sp(8))
    bmc = [
        ["Block", "Content"],
        ["Key Partners",        "• OpenAI / Anthropic API\n• College placement depts (B2B)\n• LinkedIn for data signals\n• NSDC / Skill India (distribution)"],
        ["Key Activities",      "• AI roadmap generation & tuning\n• Student onboarding & activation\n• College partnership sales\n• Content & outcome data curation"],
        ["Key Resources",       "• AI/LLM API access\n• India career market dataset\n• Founder + tech co-founder\n• College relationships"],
        ["Value Proposition",   "• Personalised 12-week career roadmap\n• Skill-gap diagnosis vs. target role\n• Affordable (free tier always exists)\n• India-specific, not US-centric"],
        ["Customer Segments",   "• B2C: 19–23 yr college students\n• B2B: College placement offices\n• Expansion: Recent grads (0–2 yr)"],
        ["Channels",            "• Instagram / YouTube content\n• WhatsApp group seeding\n• College campus ambassador\n• Direct B2B email outreach"],
        ["Customer Relations",  "• Self-serve freemium onboarding\n• Weekly AI nudges / check-ins\n• Milestone badges + streaks\n• WhatsApp support bot"],
        ["Revenue Streams",     "• B2C: Rs.99/299/mo subscriptions\n• B2B: Rs.2L/yr per institution\n• Future: Recruiter data access fee"],
        ["Cost Structure",      "• LLM API costs (per query)\n• Cloud hosting (AWS/GCP)\n• Content creation\n• B2B sales effort (founder time)"],
    ]
    el.append(tbl(bmc[0], bmc[1:], cw=[130, CW-130]))
    el.append(sp(10))

    # ── Revenue ──
    el.append(banner("5. REVENUE & PRICING STRATEGY", "How money flows in — and when"))
    el.append(sp(8))
    rev_rows = [
        ["Stream", "Model", "Price", "Target Users", "Year 1 Goal", "Confidence"],
        ["Free Tier",    "Freemium",   "Rs. 0",     "All students (acquisition)",  "5,000 users",   "High"],
        ["Pro B2C",      "Subscription","Rs. 99/mo", "Motivated students",          "500 paying",    "Low"],
        ["Elite B2C",    "Subscription","Rs. 299/mo","Placement-focused students",  "100 paying",    "Very Low"],
        ["College B2B",  "Annual SaaS", "Rs. 2L/yr", "Placement cells",             "3 colleges",    "Low"],
        ["Data/API",     "Future",      "TBD",       "Recruiters / HR platforms",   "Phase 2",       "Speculative"],
    ]
    el.append(tbl(rev_rows[0], rev_rows[1:], cw=[72, 72, 72, 115, 80, CW-411]))
    el.append(sp(8))

    unit_rows = [
        ["Metric", "B2C Estimate", "B2B Estimate"],
        ["Avg. Contract Value",       "Rs. 1,188/yr (Pro)",        "Rs. 2,00,000/yr"],
        ["CAC (Customer Acq. Cost)",  "Rs. 300–800 (unvalidated)", "Rs. 15,000–40,000"],
        ["LTV (Lifetime Value)",      "Rs. 1,500–3,000",           "Rs. 4,00,000 (3-yr contract)"],
        ["LTV:CAC Ratio",             "~3–5x (target)",            "~10x (if retained)"],
        ["Payback Period",            "3–6 months",                "6–12 months"],
        ["Gross Margin",              "~75% (post API costs)",     "~80%"],
        ["Churn Risk",                "High (student lifecycle)",  "Low (annual contract)"],
    ]
    el.append(tbl(unit_rows[0], unit_rows[1:], cw=[160, 140, CW-300]))
    el.append(sp(6))
    el.append(callout(
        "<b>Revenue Thesis:</b> B2C creates reach and proof. B2B creates revenue. "
        "Target: 3 college contracts (Rs.6L ARR) + 500 Pro users (Rs.6L ARR) = Rs.12L ARR by Month 12. "
        "This is the minimum viable revenue signal for a pre-seed raise.",
        bg=colors.HexColor("#F0FDF4"), border=GREEN))
    el.append(PageBreak())
    return el

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 6 — GTM + ACQUISITION
# ═══════════════════════════════════════════════════════════════════════════════
def gtm_acquisition():
    el = []

    el.append(banner("6. GO-TO-MARKET STRATEGY", "Distribution is the business"))
    el.append(sp(8))
    el.append(Paragraph("GTM Motion: Community-Led → Content-Led → Partnership-Led", sH2))
    el.append(sp(6))
    gtm = [
        ["Phase", "Timeline", "Channel", "Target", "Action"],
        ["Phase 1\nSeed",     "Day 1–30",  "WhatsApp + College",    "50 students",
         "Manual interviews; 5-question survey in WhatsApp groups; build trust before product"],
        ["Phase 2\nLaunch",   "Day 31–60", "Landing page + Content","200 signups",
         "Carrd/Framer landing page; Instagram reels on 'career roadmap for CSE students'"],
        ["Phase 3\nGrow",     "Month 3–6", "SEO + Campus Amb.",     "1,000 users",
         "Campus ambassador program (1 per college, free Pro account); SEO for 'career roadmap for B.Tech'"],
        ["Phase 4\nScale",    "Month 6–12","B2B Outreach + PR",     "5,000 users",
         "Pitch 10 colleges/month; placement officer LinkedIn DMs; EdTech media coverage"],
    ]
    el.append(tbl(gtm[0], gtm[1:], cw=[58, 58, 90, 72, CW-278]))
    el.append(sp(10))

    el.append(banner("7. CUSTOMER ACQUISITION STRATEGY", "How to get the first 1,000 users cheaply"))
    el.append(sp(8))
    acq = [
        ["Channel", "Cost", "Scalability", "Speed", "Priority"],
        ["WhatsApp college groups (seed)",    "Free",       "Low",    "Fast",   "🔴 Now"],
        ["Instagram reels (organic)",         "Time only",  "Medium", "Medium", "🔴 Now"],
        ["Campus ambassador program",         "Free Pro acc","High",  "Slow",   "🟠 Month 2"],
        ["SEO — 'career roadmap India'",      "Content only","High",  "Slow",   "🟠 Month 2"],
        ["College placement cell outreach",   "Founder time","High",  "Slow",   "🟠 Month 2"],
        ["LinkedIn content by founder",       "Time only",  "Medium", "Medium", "🟡 Month 3"],
        ["Paid Instagram/Google ads",         "Rs.10K+/mo", "High",   "Fast",   "🟡 Month 4+"],
        ["EdTech newsletter / podcast",       "Rs.5K–20K",  "Medium", "Medium", "🟡 Month 4+"],
    ]
    el.append(tbl(acq[0], acq[1:], cw=[160, 70, 76, 60, CW-366]))
    el.append(sp(6))
    el.append(callout(
        "<b>Acquisition Insight:</b> The highest-leverage move is a <b>campus ambassador program</b>. "
        "Give 1 student per college a free Pro account in exchange for hosting a 'Career Roadmap Workshop'. "
        "One event = 50–200 signups. 10 colleges = 500–2,000 users at near-zero cost.",
        bg=LGBG, border=BLUE))
    el.append(PageBreak())
    return el

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 7 — FIRST 100 USERS + MOAT
# ═══════════════════════════════════════════════════════════════════════════════
def users_moat():
    el = []

    el.append(banner("8. FIRST 100 USERS PLAN", "Who they are, where to find them, how to convert"))
    el.append(sp(8))
    users_plan = [
        ["Batch", "Users", "Source", "Method", "Timeline"],
        ["Batch 1", "10",  "Founder's own network",
         "DM 20 college friends; share manual roadmap; collect feedback",
         "Day 1–3"],
        ["Batch 2", "20",  "College WhatsApp groups",
         "Post: 'I'm building an AI career mentor — want a free roadmap review?'",
         "Day 4–7"],
        ["Batch 3", "30",  "Landing page sign-ups",
         "Build Carrd page; share in 5 communities; run IG story poll",
         "Day 8–14"],
        ["Batch 4", "20",  "LinkedIn outreach",
         "Founder posts: 'I made 5 students a personalised roadmap — results inside'",
         "Day 15–21"],
        ["Batch 5", "20",  "Referrals from batches 1–4",
         "Ask satisfied users to share; offer 'refer 1, get 1 month free'",
         "Day 22–30"],
    ]
    el.append(tbl(users_plan[0], users_plan[1:], cw=[52, 38, 100, 185, CW-375]))
    el.append(sp(6))
    el.append(callout(
        "<b>Key Rule for First 100:</b> Do not automate anything. Talk to every single user personally. "
        "The insights from conversations 1–100 will define the product for users 101–10,000.",
        bg=colors.HexColor("#FFF7ED"), border=AMBER))
    el.append(sp(10))

    el.append(banner("9. COMPETITIVE POSITION & MOAT", "How to stay ahead"))
    el.append(sp(8))
    moat_rows = [
        ["Moat Type", "Description", "Build Time", "Strength"],
        ["India Career Data", "Proprietary dataset of skills vs. hiring company expectations in India",
         "6–12 months", "🟢 Strong if built"],
        ["Outcome Data",  "Track user outcomes (internships won, jobs got) — creates proof loop",
         "12–18 months", "🟢 Strong if built"],
        ["College Integrations","Signed agreements with placement cells — creates switching cost",
         "3–6 months",  "🟡 Medium"],
        ["Brand / Community","'The go-to career OS for Indian students' — community trust",
         "12+ months",  "🟡 Medium"],
        ["Product UX",   "Structured career UX ChatGPT can't match (roadmap + tracker + nudges)",
         "1–3 months",  "🔴 Temporary only"],
        ["Referral Loop","Students who get hired refer the platform — viral proof",
         "6–9 months",  "🟡 Medium"],
    ]
    el.append(tbl(moat_rows[0], moat_rows[1:], cw=[110, 190, 80, CW-380]))
    el.append(sp(6))
    el.append(callout(
        "<b>Moat Strategy:</b> Product UX is not a moat — ChatGPT will copy features. "
        "Your real moat is <b>India career outcome data + college integrations</b>. "
        "Start collecting outcome data from day 1. Every student who gets hired is a data point and a testimonial.",
        bg=colors.HexColor("#F0FDF4"), border=GREEN))
    el.append(PageBreak())
    return el

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 8 — REVERSE SWOT + PITCH
# ═══════════════════════════════════════════════════════════════════════════════
def swot_pitch():
    el = []

    el.append(banner("10. REVERSE SWOT ANALYSIS", "Focus on what could go wrong — and how to prevent it"))
    el.append(sp(8))

    sw_left = Table([
        [Paragraph("<b>STRENGTHS TO PROTECT</b>", S("sh", fontSize=9, fontName="Helvetica-Bold",
                    textColor=GREEN, leading=12))],
        [Paragraph("• First-mover on 'career OS' positioning in India", sBul)],
        [Paragraph("• Low-cost validation possible (&lt;Rs.50K)", sBul)],
        [Paragraph("• Dual revenue: B2C reach + B2B revenue", sBul)],
        [Paragraph("• AI timing — students already expect AI tools", sBul)],
        [Paragraph("• Clear aha moment: personalised roadmap in &lt;3 min", sBul)],
    ], colWidths=[CW/2 - 5])

    sw_right = Table([
        [Paragraph("<b>WEAKNESSES TO FIX IMMEDIATELY</b>", S("wh", fontSize=9, fontName="Helvetica-Bold",
                    textColor=RED, leading=12))],
        [Paragraph("• No technical co-founder or dev partner", sBul)],
        [Paragraph("• Zero primary validation (0 interviews done)", sBul)],
        [Paragraph("• No distribution channel confirmed", sBul)],
        [Paragraph("• AI quality untested — roadmaps may be generic", sBul)],
        [Paragraph("• No revenue evidence — WTP completely assumed", sBul)],
    ], colWidths=[CW/2 - 5])

    opp_left = Table([
        [Paragraph("<b>OPPORTUNITIES TO CAPTURE FIRST</b>", S("oh", fontSize=9, fontName="Helvetica-Bold",
                    textColor=BLUE, leading=12))],
        [Paragraph("• Campus ambassador program = free distribution", sBul)],
        [Paragraph("• B2B college licensing = fast revenue path", sBul)],
        [Paragraph("• India's 21.7% EdTech CAGR = rising tide", sBul)],
        [Paragraph("• Outcome data flywheel: proof → more users → more data", sBul)],
        [Paragraph("• YC / Surge accelerators actively funding EdTech AI", sBul)],
    ], colWidths=[CW/2 - 5])

    thr_right = Table([
        [Paragraph("<b>THREATS TO NEUTRALISE NOW</b>", S("th", fontSize=9, fontName="Helvetica-Bold",
                    textColor=AMBER, leading=12))],
        [Paragraph("• ChatGPT / Gemini adding career UX features", sBul)],
        [Paragraph("• Internshala / Unstop launch AI roadmap feature", sBul)],
        [Paragraph("• College B2B sales cycle: 3–9 months (too slow)", sBul)],
        [Paragraph("• Student churn: graduation lifecycle limits LTV", sBul)],
        [Paragraph("• India DPDPA 2023 compliance for student data", sBul)],
    ], colWidths=[CW/2 - 5])

    sw_table = Table([[sw_left, sw_right], [opp_left, thr_right]],
                     colWidths=[CW/2, CW/2])
    sw_table.setStyle(TableStyle([
        ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),0),
        ("TOPPADDING",(0,0),(-1,-1),0),("BOTTOMPADDING",(0,0),(-1,-1),6),
        ("LINEBEFORE",(1,0),(1,-1),0.5,MGRAY),
        ("LINEBELOW",(0,0),(-1,0),0.5,MGRAY),
    ]))
    el.append(sw_table)
    el.append(sp(10))

    el.append(banner("11. INVESTOR ONE-LINER & 30-SECOND PITCH"))
    el.append(sp(8))

    oneliner = Table([[
        Paragraph(
            "<b>Investor One-Liner:</b><br/>"
            "\"We are the AI career mentor for India's 43 million college students — giving every "
            "student a personalised roadmap from classroom to career, at the price of a coffee per month.\"",
            S("ol", fontSize=10, textColor=WHITE, fontName="Helvetica", leading=16))
    ]], colWidths=[CW])
    oneliner.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), INDIGO),
        ("BOX",(0,0),(-1,-1), 1.5, BLUE),
        ("LEFTPADDING",(0,0),(-1,-1),16),("RIGHTPADDING",(0,0),(-1,-1),16),
        ("TOPPADDING",(0,0),(-1,-1),14),("BOTTOMPADDING",(0,0),(-1,-1),14),
    ]))
    el.append(oneliner)
    el.append(sp(8))

    pitch = Table([[
        Paragraph(
            "<b>30-Second Founder Pitch:</b><br/><br/>"
            "\"India has 43 million college students. Most of them have no idea what to learn next, "
            "which projects to build, or how to prepare for their first job. Human mentors cost "
            "Rs.2,000 a session — that's a week's food budget for most students. "
            "We're building an AI career mentor that gives every student a personalised, "
            "12-week roadmap — skills, projects, and certifications — matched to their specific goal, "
            "for less than Rs.100 a month. We're starting in India where the problem is most acute "
            "and the market is 43 million strong. We've identified clear white space that no competitor "
            "owns today. We're raising a pre-seed to run customer discovery, build our MVP, and sign "
            "our first 3 college partnerships. If you've ever wished you'd had a smarter guide at "
            "the start of your career — that's what we're building, for every student.\"",
            S("pitch", fontSize=9, textColor=BLACK, fontName="Helvetica", leading=15))
    ]], colWidths=[CW])
    pitch.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), LGBG),
        ("BOX",(0,0),(-1,-1), 0.5, BLUE),
        ("LEFTPADDING",(0,0),(-1,-1),14),("RIGHTPADDING",(0,0),(-1,-1),14),
        ("TOPPADDING",(0,0),(-1,-1),12),("BOTTOMPADDING",(0,0),(-1,-1),12),
    ]))
    el.append(pitch)
    el.append(PageBreak())
    return el

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 9 — INVESTMENT SCORECARD + ACTION SHEET
# ═══════════════════════════════════════════════════════════════════════════════
def scorecard_actions():
    el = []

    el.append(banner("12. INVESTMENT SCORECARD", "Honest 0–100 scores with reasoning"))
    el.append(sp(8))
    scores = [
        ("Business Viability — Can this become a real, self-sustaining business?",       68, GREEN),
        ("Revenue Potential — How large and predictable is the revenue ceiling?",         72, BLUE),
        ("GTM Strength — Is there a clear, executable path to first 1,000 users?",       55, AMBER),
        ("Competitive Strength — How defensible is the position vs. incumbents?",        58, TEAL),
        ("Investor Readiness — Is this ready for a pre-seed pitch right now?",            38, RED),
    ]
    for label, val, clr in scores:
        el.append(score_bar(label, val, 100, clr))
    el.append(sp(8))

    reasoning = [
        ["Dimension", "Score", "Key Reasoning"],
        ["Business Viability", "68",
         "Real problem, large market, dual revenue model. Penalised for zero validation and no team."],
        ["Revenue Potential",  "72",
         "B2B college licensing creates scalable ARR. B2C is high-churn but high-volume potential."],
        ["GTM Strength",       "55",
         "No distribution engine proven. Campus ambassador + content is plausible but untested."],
        ["Competitive Strength","58",
         "Clear white space today, but temporary. ChatGPT is a permanent and fast-moving threat."],
        ["Investor Readiness", "38",
         "Not ready. No MVP, no interviews, no metrics, no co-founder. Returns to 65+ after 30-day sprint."],
        ["<b>OVERALL</b>",     "<b>58</b>",
         "<b>Validate. Hit the 5 gates. Then pitch. Do not pitch investors before the sprint.</b>"],
    ]
    el.append(tbl(reasoning[0], reasoning[1:], cw=[130, 45, CW-175]))
    el.append(sp(10))

    el.append(banner("14. FOUNDER ACTION SHEET", "Top 10 actions — ranked by business impact"))
    el.append(sp(8))
    actions = [
        ["#", "Action", "Business Impact", "When"],
        ["1","Conduct 20 student interviews using JTBD — focus on WTP signal",
         "Validates or kills the revenue assumption","Day 1–5"],
        ["2","Build a 1-page landing page with pricing page (3 tiers shown)",
         "Tests discovery + conversion assumptions","Day 6–7"],
        ["3","Run manual 'wizard of oz' roadmap for 10 students — no AI yet",
         "Tests if the product idea creates value before building","Day 8–12"],
        ["4","Ask 5 students: 'Would you pay Rs.99/mo for this?' — record answers",
         "First real WTP data point","Day 9–12"],
        ["5","Email 10 college placement officers — offer free pilot",
         "Opens B2B pipeline which is your real revenue path","Day 10–18"],
        ["6","Interview 5 HR managers: 'What skills make interns stand out?'",
         "Builds proprietary data asset + credibility","Day 15–20"],
        ["7","Post on LinkedIn: 'I built 5 students a career roadmap — here are the results'",
         "Tests content distribution + founder brand","Day 14"],
        ["8","Find a technical co-founder or no-code developer",
         "Without this, MVP takes 6 months instead of 6 weeks","Day 20–30"],
        ["9","Define MVP scope: ONE feature only (personalised roadmap generator)",
         "Prevents scope creep from killing the launch","Day 21"],
        ["10","Apply to Surge (Sequoia India), Y Combinator, or Antler India",
         "Unlocks capital, network, credibility in one move","Day 25–30"],
    ]
    el.append(tbl(actions[0], actions[1:], cw=[18, 200, 140, CW-358]))
    el.append(PageBreak())
    return el

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 10 — SUSTAINABILITY VERDICT
# ═══════════════════════════════════════════════════════════════════════════════
def verdict_page():
    el = []

    el.append(banner("15. SUSTAINABILITY VERDICT", "The final word from your AI Co-Founder"))
    el.append(sp(10))

    # Big verdict box
    verdict = Table([[
        Paragraph(
            "🟡 &nbsp;<b>VERDICT: PROMISING — VALIDATE IMMEDIATELY</b><br/><br/>"
            "The AI Career Mentor for Students is a genuinely promising business idea with a large, "
            "underserved market, clear problem urgency, and an open competitive white space in India. "
            "The dual B2C + B2B revenue model creates multiple paths to sustainability, and the "
            "capital efficiency of a no-code MVP means the founder can reach meaningful validation "
            "milestones for under Rs.50,000. However, this is not yet a business — it is an "
            "educated hypothesis. Every critical assumption (willingness to pay, distribution, "
            "AI quality, college sales speed) remains unvalidated.<br/><br/>"
            "The next 30 days are the most important 30 days in this startup's life. Complete "
            "50 interviews, get 100 waitlist signups, pitch 5 colleges, and collect pricing data. "
            "If all 5 gates are hit, this becomes investable at a pre-seed level "
            "(Rs.50L–1Cr / $60K–120K). If fewer than 3 gates are hit, the hypothesis needs "
            "significant revision before any capital is raised or product is built.<br/><br/>"
            "The question is not whether Indian students need career guidance — they clearly do. "
            "The question is whether <i>this founder</i>, with <i>this approach</i>, can build the "
            "distribution engine fast enough before general-purpose AI tools close the window. "
            "Speed of validation, not quality of the product idea, is the critical variable.",
            S("vt", fontSize=9.5, textColor=WHITE, fontName="Helvetica", leading=16))
    ]], colWidths=[CW])
    verdict.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), NAVY),
        ("BOX",(0,0),(-1,-1), 2, AMBER),
        ("LEFTPADDING",(0,0),(-1,-1),18),("RIGHTPADDING",(0,0),(-1,-1),18),
        ("TOPPADDING",(0,0),(-1,-1),16),("BOTTOMPADDING",(0,0),(-1,-1),16),
    ]))
    el.append(verdict)
    el.append(sp(12))

    # 5 gates
    el.append(Paragraph("The 5 Gates to Investability", sH2))
    el.append(sp(6))
    gates = [
        ["Gate", "Target", "Status", "If Met → Next Step"],
        ["1. Student Interviews",  "50 completed",       "⬜ Not started", "Confirms problem severity"],
        ["2. Waitlist Signups",    "100+ emails",        "⬜ Not started", "Confirms discovery channel"],
        ["3. WTP Signal",          "20% say Yes to Rs.99","⬜ Not started","Confirms revenue model"],
        ["4. College Pilot Lead",  "1 confirmed interest","⬜ Not started","Confirms B2B path"],
        ["5. MVP Scope Defined",   "1-feature spec done","⬜ Not started", "Ready to build"],
    ]
    el.append(tbl(gates[0], gates[1:], cw=[130, 110, 90, CW-330]))
    el.append(sp(10))

    # 3-sentence sustainability statement
    sustain = Table([[
        Paragraph(
            "<b>Sustainability Statement:</b> The AI Career Mentor can become a sustainable, "
            "profitable business if — and only if — the B2B institutional revenue stream is "
            "developed in parallel with B2C, since student subscription churn will prevent "
            "unit economics from closing on B2C alone. The moat must be built on proprietary "
            "India career outcome data and college integrations, not product features, which "
            "any well-funded competitor can replicate within 6–12 months. Execute the 30-day "
            "validation sprint before spending a single rupee on product development — the "
            "answers you collect in the next 30 days are worth more than any AI feature "
            "you could build.",
            S("ss", fontSize=9, textColor=BLACK, fontName="Helvetica-Oblique", leading=14))
    ]], colWidths=[CW])
    sustain.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), colors.HexColor("#F0FDF4")),
        ("BOX",(0,0),(-1,-1), 0.5, GREEN),
        ("LEFTPADDING",(0,0),(-1,-1),14),("RIGHTPADDING",(0,0),(-1,-1),14),
        ("TOPPADDING",(0,0),(-1,-1),12),("BOTTOMPADDING",(0,0),(-1,-1),12),
        ("LINEBEFORETABLE",(0,0),(0,-1), 3, GREEN),
    ]))
    el.append(sustain)
    el.append(sp(14))

    footer = Table([[
        Paragraph("AI Career Mentor — Business Strategy Report", sSmall),
        Paragraph("Confidential | AI Co-Founder Engine | June 2025",
                  S("fr", fontSize=7, textColor=DGRAY, alignment=TA_RIGHT, fontName="Helvetica")),
    ]], colWidths=[CW/2, CW/2])
    footer.setStyle(TableStyle([
        ("LINEABOVE",(0,0),(-1,-1),0.5,MGRAY),
        ("TOPPADDING",(0,0),(-1,-1),6),
        ("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),0),
    ]))
    el.append(footer)
    return el

def build(path):
    doc = SimpleDocTemplate(
        path, pagesize=A4,
        leftMargin=M, rightMargin=M, topMargin=M, bottomMargin=M,
        title="AI Co-Founder Business Strategy Report — AI Career Mentor",
        author="AI Co-Founder & Growth Strategy Engine",
    )
    story = []
    story += cover()
    story += toc()
    story += summary_reality()
    story += exec_summary()
    story += bmc_revenue()
    story += gtm_acquisition()
    story += users_moat()
    story += swot_pitch()
    story += scorecard_actions()
    story += verdict_page()
    doc.build(story)
    print(f"Saved: {path}")

build("/mnt/user-data/outputs/Business_Strategy_Report_AI_Career_Mentor.pdf")
