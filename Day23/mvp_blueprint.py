from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Circle, Polygon
from reportlab.graphics.shapes import PolyLine

# ── Palette ──────────────────────────────────────────────────────────────────
NAVY    = colors.HexColor("#0D1B2A")
INDIGO  = colors.HexColor("#1B3A6B")
ACCENT  = colors.HexColor("#2563EB")
TEAL    = colors.HexColor("#0EA5E9")
GREEN   = colors.HexColor("#10B981")
AMBER   = colors.HexColor("#F59E0B")
RED     = colors.HexColor("#EF4444")
PURPLE  = colors.HexColor("#7C3AED")
LGBG    = colors.HexColor("#F0F4FF")
LGRAY   = colors.HexColor("#F8FAFC")
MGRAY   = colors.HexColor("#E2E8F0")
DGRAY   = colors.HexColor("#64748B")
WHITE   = colors.white
BLACK   = colors.HexColor("#0F172A")

PAGE_W, PAGE_H = A4
M = 1.6 * cm
CW = PAGE_W - 2 * M   # content width

# ── Styles ────────────────────────────────────────────────────────────────────
def S(name, **kw): return ParagraphStyle(name, **kw)

sTitle  = S("T",  fontSize=24, textColor=WHITE,  fontName="Helvetica-Bold",  leading=30, alignment=TA_CENTER)
sSub    = S("Su", fontSize=10, textColor=colors.HexColor("#93C5FD"), fontName="Helvetica", leading=14, alignment=TA_CENTER)
sH1     = S("H1", fontSize=11, textColor=WHITE,  fontName="Helvetica-Bold",  leading=14)
sH2     = S("H2", fontSize=10, textColor=INDIGO, fontName="Helvetica-Bold",  leading=13)
sBody   = S("B",  fontSize=8.5,textColor=BLACK,  fontName="Helvetica",       leading=13, alignment=TA_JUSTIFY)
sBul    = S("Bu", fontSize=8.5,textColor=BLACK,  fontName="Helvetica",       leading=13, leftIndent=10, firstLineIndent=-10)
sTHdr   = S("TH", fontSize=8,  textColor=WHITE,  fontName="Helvetica-Bold",  leading=11, alignment=TA_CENTER)
sTCell  = S("TC", fontSize=8,  textColor=BLACK,  fontName="Helvetica",       leading=11, alignment=TA_LEFT)
sTCellC = S("TCC",fontSize=8,  textColor=BLACK,  fontName="Helvetica",       leading=11, alignment=TA_CENTER)
sSmall  = S("Sm", fontSize=7,  textColor=DGRAY,  fontName="Helvetica",       leading=10)
sScore  = S("Sc", fontSize=18, textColor=ACCENT, fontName="Helvetica-Bold",  leading=22, alignment=TA_CENTER)
sLabel  = S("La", fontSize=7,  textColor=DGRAY,  fontName="Helvetica",       leading=10, alignment=TA_CENTER)
sVerdict= S("V",  fontSize=10, textColor=WHITE,  fontName="Helvetica-Bold",  leading=14, alignment=TA_CENTER)

def sp(h=6): return Spacer(1, h)
def hr(): return HRFlowable(width="100%", thickness=0.4, color=MGRAY, spaceAfter=4, spaceBefore=4)

# ── Section banner ────────────────────────────────────────────────────────────
def banner(title, subtitle=""):
    d = Drawing(CW, 34)
    d.add(Rect(0, 0, CW, 34, fillColor=INDIGO, strokeColor=None))
    d.add(Rect(0, 0, 4, 34, fillColor=ACCENT,  strokeColor=None))
    d.add(String(12, 13, title, fontName="Helvetica-Bold", fontSize=11, fillColor=WHITE))
    if subtitle:
        d.add(String(12, 4, subtitle, fontName="Helvetica-Oblique", fontSize=7,
                     fillColor=colors.HexColor("#93C5FD")))
    return d

# ── Callout ───────────────────────────────────────────────────────────────────
def callout(text, bg=LGBG, border=ACCENT):
    t = Table([[Paragraph(text, sBody)]], colWidths=[CW - 2])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), bg),
        ("BOX",(0,0),(-1,-1), 0.5, border),
        ("LEFTPADDING",(0,0),(-1,-1),10), ("RIGHTPADDING",(0,0),(-1,-1),10),
        ("TOPPADDING",(0,0),(-1,-1),8),   ("BOTTOMPADDING",(0,0),(-1,-1),8),
        ("LINEBEFORETABLE",(0,0),(0,-1), 3, border),
    ]))
    return t

# ── Std table ─────────────────────────────────────────────────────────────────
def tbl(headers, rows, cw=None, stripe=True):
    data = [[Paragraph(h, sTHdr) for h in headers]]
    for row in rows:
        data.append([Paragraph(str(c), sTCellC if i > 0 else sTCell)
                     for i, c in enumerate(row)])
    if not cw:
        cw = [CW / len(headers)] * len(headers)
    t = Table(data, colWidths=cw, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0), INDIGO),
        ("GRID",(0,0),(-1,-1), 0.35, MGRAY),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [WHITE, LGBG] if stripe else [WHITE]),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("LEFTPADDING",(0,0),(-1,-1),7), ("RIGHTPADDING",(0,0),(-1,-1),7),
        ("TOPPADDING",(0,0),(-1,-1),6),  ("BOTTOMPADDING",(0,0),(-1,-1),6),
    ]))
    return t

# ── Score bar ─────────────────────────────────────────────────────────────────
def score_bar(label, val, mx, clr):
    bw = CW - 170
    pct = val / mx
    d = Drawing(bw, 14)
    d.add(Rect(0, 3, bw, 8, fillColor=MGRAY, strokeColor=None))
    d.add(Rect(0, 3, bw * pct, 8, fillColor=clr, strokeColor=None))
    d.add(String(bw * pct + 3, 4, f"{val}/{mx}", fontName="Helvetica-Bold",
                 fontSize=7, fillColor=BLACK))
    row = Table([[Paragraph(label, sBody), d]], colWidths=[165, bw])
    row.setStyle(TableStyle([
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("TOPPADDING",(0,0),(-1,-1),4), ("BOTTOMPADDING",(0,0),(-1,-1),4),
        ("LEFTPADDING",(0,0),(-1,-1),4), ("RIGHTPADDING",(0,0),(-1,-1),4),
        ("ROWBACKGROUNDS",(0,0),(-1,-1),[WHITE]),
    ]))
    return row

# ── Metric strip ─────────────────────────────────────────────────────────────
def metric_strip(items):
    cw = CW / len(items)
    cells = []
    for label, val, clr in items:
        d = Drawing(cw - 8, 52)
        d.add(Rect(0, 0, cw - 8, 52, fillColor=LGBG, strokeColor=MGRAY, strokeWidth=0.5))
        d.add(Rect(0, 48, cw - 8, 4, fillColor=clr, strokeColor=None))
        d.add(String((cw-8)/2, 24, val, fontName="Helvetica-Bold", fontSize=15,
                     fillColor=clr, textAnchor="middle"))
        d.add(String((cw-8)/2, 8, label, fontName="Helvetica", fontSize=7,
                     fillColor=DGRAY, textAnchor="middle"))
        cells.append(d)
    t = Table([cells], colWidths=[cw] * len(items))
    t.setStyle(TableStyle([("LEFTPADDING",(0,0),(-1,-1),3),("RIGHTPADDING",(0,0),(-1,-1),3),
                            ("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3)]))
    return t

# ── MoSCoW coloured block ─────────────────────────────────────────────────────
def moscow_block(label, color, items):
    header = Drawing(CW, 22)
    header.add(Rect(0, 0, CW, 22, fillColor=color, strokeColor=None))
    header.add(String(10, 6, label, fontName="Helvetica-Bold", fontSize=10, fillColor=WHITE))
    rows = [[Paragraph(f"• {it}", sBul)] for it in items]
    body = Table(rows, colWidths=[CW])
    body.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), colors.HexColor("#F8FAFC")),
        ("LEFTPADDING",(0,0),(-1,-1),10),("RIGHTPADDING",(0,0),(-1,-1),10),
        ("TOPPADDING",(0,0),(-1,-1),5), ("BOTTOMPADDING",(0,0),(-1,-1),5),
        ("LINEBELOW",(0,0),(-1,-1),0.3,MGRAY),
    ]))
    return [header, body]

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — COVER
# ═══════════════════════════════════════════════════════════════════════════════
def cover():
    el = []
    # Hero block
    d = Drawing(CW, 190)
    d.add(Rect(0, 0, CW, 190, fillColor=NAVY, strokeColor=None))
    d.add(Rect(0, 0, CW, 4, fillColor=ACCENT, strokeColor=None))
    d.add(Rect(0, 186, CW, 4, fillColor=TEAL, strokeColor=None))
    d.add(Circle(CW - 40, 160, 55, fillColor=colors.HexColor("#1E3A8A"), strokeColor=None))
    d.add(Circle(CW - 40, 160, 32, fillColor=INDIGO, strokeColor=None))
    el.append(d)
    hero = Table([
        [Paragraph("CUSTOMER &amp; MVP BLUEPRINT", sTitle)],
        [Paragraph("AI Career Mentor for Students", sSub)],
        [sp(4)],
        [Paragraph("Derived from Startup Validation Report &nbsp;|&nbsp; India Market &nbsp;|&nbsp; June 2025", sSub)],
        [Paragraph("Prepared by AI Product Strategy Engine", S("tag", fontSize=8,
            textColor=colors.HexColor("#CBD5E1"), fontName="Helvetica-Oblique", alignment=TA_CENTER))],
    ], colWidths=[CW])
    hero.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), NAVY),
        ("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7),
        ("LEFTPADDING",(0,0),(-1,-1),16),("RIGHTPADDING",(0,0),(-1,-1),16),
    ]))
    el.append(hero)
    el.append(sp(12))
    el.append(metric_strip([
        ("Customer Clarity", "72/100", ACCENT),
        ("Problem Severity", "80/100", GREEN),
        ("PMF Potential",    "65/100", TEAL),
        ("MVP Readiness",    "30/100", AMBER),
    ]))
    el.append(sp(12))
    el.append(callout(
        "<b>Verdict: 🟡 Promising but Unvalidated</b> — Strong problem signal in a large market, "
        "but zero primary research completed. This blueprint defines exactly what to build, "
        "who to build it for, and what to do in the next 30 days.",
        bg=colors.HexColor("#FFF7ED"), border=AMBER))
    el.append(PageBreak())
    return el

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — EXEC SUMMARY + ICP + PERSONA
# ═══════════════════════════════════════════════════════════════════════════════
def exec_icp_persona():
    el = []

    # ── Executive Summary ──
    el.append(banner("1. EXECUTIVE SUMMARY", "What this blueprint is based on"))
    el.append(sp(8))
    summary = [
        ["Field", "Detail"],
        ["Product",       "AI-powered personalised career mentor for college students"],
        ["Core Problem",  "Students lack guidance on what to learn, build, and do to get hired"],
        ["Target Users",  "19–23 yr college students, India, Tier-1 & Tier-2 cities"],
        ["Market Size",   "SAM $380M | 43M+ students in India"],
        ["Validation",    "Observational only — no interviews, MVP, or waitlist"],
        ["Stage",         "Pre-idea → needs 30-day discovery sprint before building"],
        ["Revenue Model", "Freemium B2C (Rs.0–299/mo) + B2B institutional licensing"],
        ["Key Insight",   "No competitor owns the end-to-end 'career OS for students' position"],
    ]
    el.append(tbl(summary[0], summary[1:], cw=[140, CW-140]))
    el.append(sp(10))

    # ── ICP ──
    el.append(banner("2. IDEAL CUSTOMER PROFILE (ICP)", "Your best early adopter"))
    el.append(sp(8))
    icp_rows = [
        ["Dimension",     "B2C Student (Primary)",              "B2B Institution (Secondary)"],
        ["Who",           "2nd–4th year college student",       "Placement / Training Dept."],
        ["Location",      "Tier-1 & Tier-2 Indian cities",      "Any college 1,000+ students"],
        ["Pain Level",    "High — confused, anxious, behind",   "High — low placement rates"],
        ["Budget",        "Rs. 0–299/month",                    "Rs. 50K–5L/year"],
        ["Channel",       "Instagram, WhatsApp, LinkedIn",      "LinkedIn, EdTech expos, MoUs"],
        ["Job-to-be-Done","'Tell me what to learn and do next'","'Improve our placement %'"],
        ["Decision Time", "Minutes (self-serve)",               "Weeks–months (committee)"],
    ]
    el.append(tbl(icp_rows[0], icp_rows[1:], cw=[110, 155, CW-265]))
    el.append(sp(10))

    # ── Persona ──
    el.append(banner("3. BUYER PERSONA", "Arjun — The Confused Engineer"))
    el.append(sp(8))
    persona = Table([[
        Table([
            [Paragraph("<b>Arjun, 21 — B.Tech CSE, Year 3, Pune</b>", sH2)],
            [Paragraph("CGPA: 7.2 &nbsp;|&nbsp; Mid-tier private college &nbsp;|&nbsp; Smartphone-native", sSmall)],
            [sp(4)],
            [Paragraph("<b>Goals:</b> Land a product-company internship; know which skills matter; "
                       "build 2 impressive projects; get placed before graduation.", sBul)],
            [Paragraph("<b>Frustrations:</b> Done 10 courses with no direction; placement cell gives "
                       "only a resume template; can't afford Rs.2,000/session mentors; "
                       "peer comparison anxiety from LinkedIn.", sBul)],
            [Paragraph("<b>Discovery:</b> Instagram reels, YouTube, college WhatsApp groups.", sBul)],
            [Paragraph("<b>Converts when:</b> Sees a personalised roadmap in under 3 minutes.", sBul)],
        ], colWidths=[CW - 4]),
    ]], colWidths=[CW])
    persona.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), LGBG),
        ("BOX",(0,0),(-1,-1), 0.5, ACCENT),
        ("LEFTPADDING",(0,0),(-1,-1),12),("RIGHTPADDING",(0,0),(-1,-1),12),
        ("TOPPADDING",(0,0),(-1,-1),8), ("BOTTOMPADDING",(0,0),(-1,-1),8),
    ]))
    el.append(persona)
    el.append(PageBreak())
    return el

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — PAIN POINTS + JOURNEY
# ═══════════════════════════════════════════════════════════════════════════════
def pain_journey():
    el = []

    # ── Pain Points ──
    el.append(banner("4. TOP 10 CUSTOMER PAIN POINTS", "Ranked by severity × frequency"))
    el.append(sp(8))
    pains = [
        ["#", "Pain Point", "Severity", "Freq.", "MVP Priority"],
        ["1", "No structured 'what to learn next' roadmap",    "Critical", "Daily",  "✅ Core"],
        ["2", "Can't map skills to specific job roles/companies","Critical","Daily",  "✅ Core"],
        ["3", "Fails internship screening rounds — doesn't know why","High","Monthly","✅ Core"],
        ["4", "Human mentors too expensive (Rs.2K+/session)",  "High",    "Always", "✅ Core"],
        ["5", "Doesn't know which projects impress recruiters","High",    "Weekly", "🔜 Phase 2"],
        ["6", "Certification overload — AWS vs GCP vs Azure",  "High",    "Weekly", "🔜 Phase 2"],
        ["7", "Resume doesn't reflect real skills",            "Medium",  "Once",   "🔜 Phase 2"],
        ["8", "Peer comparison anxiety on LinkedIn",           "Medium",  "Daily",  "🚫 Won't Fix"],
        ["9", "College placement support is generic/reactive", "Medium",  "Semester","🔜 Phase 2"],
        ["10","No visibility into hiring trends by company",   "Medium",  "Monthly","🔜 Phase 2"],
    ]
    el.append(tbl(pains[0], pains[1:], cw=[18, 195, 58, 45, CW-316]))
    el.append(sp(10))

    # ── Journey ──
    el.append(banner("5. CUSTOMER JOURNEY", "Awareness → Consideration → Purchase → Retention"))
    el.append(sp(8))
    journey = [
        ["Stage", "Touchpoint", "Student Thought", "Your Move", "Metric"],
        ["🔍 Aware",
         "IG reel / YouTube / friend referral",
         "'This looks like what I need'",
         "Relatable career-anxiety content",
         "CTR, Views"],
        ["🤔 Consider",
         "Landing page + free skill quiz",
         "'Will this actually work for me?'",
         "Show sample roadmap — no sign-up",
         "Quiz completions"],
        ["⚡ Activate",
         "Personalised roadmap reveal (<3 min)",
         "'Wow — this is exactly my gap!'",
         "Aha moment = instant roadmap",
         "Time-to-roadmap"],
        ["💳 Purchase",
         "Hit free plan limit",
         "'I want the full 12-week plan'",
         "Contextual upgrade prompt",
         "Conversion %"],
        ["🔄 Retain",
         "Weekly nudges + milestone badges",
         "'I'm making progress every week'",
         "Streaks, check-ins, wins",
         "WAU, D30 retention"],
        ["📣 Advocate",
         "Internship win → posts on LinkedIn",
         "'This got me my internship!'",
         "Referral: 1 month free/referral",
         "Referral rate"],
    ]
    el.append(tbl(journey[0], journey[1:], cw=[62, 105, 110, 105, CW-382]))
    el.append(PageBreak())
    return el

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — OBJECTIONS + TRIGGERS + MVP
# ═══════════════════════════════════════════════════════════════════════════════
def obj_trig_mvp():
    el = []

    # ── Two columns: objections + triggers ──
    el.append(banner("6–7. OBJECTIONS & BUYING TRIGGERS"))
    el.append(sp(8))

    obj_rows = [
        [Paragraph("<b>Key Objections</b>", sH2), Paragraph("<b>Buying Triggers</b>", sH2)],
    ]
    objections = [
        "❌ 'ChatGPT is free and does this'",
        "❌ 'I can't afford a subscription'",
        "❌ 'Another app I'll forget to use'",
        "❌ 'Will this actually get me a job?'",
        "❌ 'My college already helps with placement'",
    ]
    counters = [
        "✅ Structured career UX + India data = ChatGPT can't match",
        "✅ Core free forever; Rs.99/mo = 1 cup of café coffee",
        "✅ Weekly AI nudges + progress streaks keep engagement",
        "✅ Show outcomes data + 30-day roadmap guarantee",
        "✅ College support is generic & reactive — we're personalised",
    ]
    triggers = [
        "🔔 Semester 3–5 starts (placement anxiety kicks in)",
        "🔔 Friend posts an internship offer on LinkedIn",
        "🔔 Campus placement drive announced",
        "🔔 Failed a coding test / first-round rejection",
        "🔔 Sees a LinkedIn post: '3rd year, 3 PPOs, no regrets'",
    ]

    inner = []
    for i in range(5):
        inner.append([
            Paragraph(f"{objections[i]}<br/><i>{counters[i]}</i>", S("ob", fontSize=7.5,
                textColor=BLACK, fontName="Helvetica", leading=12)),
            Paragraph(triggers[i], S("tr", fontSize=7.5, textColor=BLACK,
                fontName="Helvetica", leading=12)),
        ])
    two_col = Table(inner, colWidths=[CW/2 - 4, CW/2 - 4])
    two_col.setStyle(TableStyle([
        ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("ROWBACKGROUNDS",(0,0),(-1,-1),[WHITE, LGBG]),
        ("LINEBELOW",(0,0),(-1,-1),0.3,MGRAY),
        ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6),
        ("LEFTPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),8),
        ("LINEBEFORE",(1,0),(1,-1),0.5,MGRAY),
    ]))
    header_row = Table([[Paragraph("<b>Objection → Counter</b>", sH2),
                         Paragraph("<b>Buying Triggers</b>", sH2)]],
                       colWidths=[CW/2 - 4, CW/2 - 4])
    header_row.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), colors.HexColor("#E0E8FF")),
        ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6),
        ("LEFTPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),8),
    ]))
    el.append(header_row)
    el.append(two_col)
    el.append(sp(10))

    # ── MVP Recommendation ──
    el.append(banner("8. MVP RECOMMENDATION", "Build this — and only this — first"))
    el.append(sp(8))

    mvp_build = Table([[
        Table([
            [Paragraph("✅ WHAT TO BUILD FIRST", S("wbh", fontSize=9, fontName="Helvetica-Bold",
                        textColor=GREEN, leading=12))],
            [Paragraph("Single core flow — the Personalised Career Roadmap Generator:", sBul)],
            [Paragraph("• Onboarding quiz (degree, goal, skills, timeline) — 5 questions max", sBul)],
            [Paragraph("• AI-generated 12-week learning roadmap (skills + resources)", sBul)],
            [Paragraph("• Weekly progress tracker with completion nudges", sBul)],
            [Paragraph("• 3 free roadmap weeks; upgrade for full access", sBul)],
        ], colWidths=[CW/2 - 8]),
        Table([
            [Paragraph("🚫 WHAT NOT TO BUILD YET", S("wnh", fontSize=9, fontName="Helvetica-Bold",
                        textColor=RED, leading=12))],
            [Paragraph("Avoid scope creep — skip these in v1:", sBul)],
            [Paragraph("• Live human mentorship matching", sBul)],
            [Paragraph("• Internship / job board integration", sBul)],
            [Paragraph("• Resume builder", sBul)],
            [Paragraph("• Community / peer features", sBul)],
            [Paragraph("• Mobile app (web-first, then app)", sBul)],
        ], colWidths=[CW/2 - 8]),
    ]], colWidths=[CW/2, CW/2])
    mvp_build.setStyle(TableStyle([
        ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),0),
        ("TOPPADDING",(0,0),(-1,-1),0), ("BOTTOMPADDING",(0,0),(-1,-1),0),
    ]))
    el.append(mvp_build)
    el.append(sp(8))

    metrics = [
        ["Success Metric", "Target (Day 90)", "Why It Matters"],
        ["Activated Users (saw roadmap)", "500+", "Proves product delivers value"],
        ["D7 Retention",                  ">40%", "Proves habit loop works"],
        ["Free → Paid Conversion",        ">5%",  "Proves willingness to pay"],
        ["NPS Score",                      ">45",  "Proves genuine delight"],
        ["College Pilot Signups",          "3+",   "Unlocks B2B revenue path"],
    ]
    el.append(tbl(metrics[0], metrics[1:], cw=[180, 100, CW-280]))
    el.append(PageBreak())
    return el

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 5 — MoSCoW + PRICING + RISKS
# ═══════════════════════════════════════════════════════════════════════════════
def moscow_pricing_risks():
    el = []

    # ── MoSCoW ──
    el.append(banner("9. MoSCoW PRIORITIZATION", "For your v1 MVP build"))
    el.append(sp(8))

    must = [
        "Onboarding quiz (degree, goal, current skills)",
        "AI-generated personalised career roadmap (12 weeks)",
        "Skill gap identification vs. target role",
        "Weekly progress tracker + completion nudges",
        "Freemium gate (3 free weeks, upgrade for full)",
    ]
    should = [
        "Resource recommendations (courses, YouTube, docs) per roadmap step",
        "Project suggestions matched to career goal",
        "Email/WhatsApp weekly digest with next action",
        "Dashboard with completion streak and % progress",
    ]
    could = [
        "Certification recommendation engine (AWS vs GCP vs Azure)",
        "Peer comparison anonymised benchmarks ('Top 20% of CSE students')",
        "Resume score against target JD",
        "LinkedIn profile optimisation tips",
    ]
    wont = [
        "Live mentor matching (v2+)",
        "Internship / job board (v2+)",
        "Mobile app (web-first, then app in v2)",
        "Community forums / peer chat (v3)",
        "AI mock interviews (v3)",
    ]

    for label, clr, items in [
        ("MUST HAVE — Core MVP (Non-Negotiable)", GREEN,  must),
        ("SHOULD HAVE — Strong v1 Additions",    ACCENT, should),
        ("COULD HAVE — Nice to Have",            AMBER,  could),
        ("WON'T HAVE — Out of Scope for v1",     RED,    wont),
    ]:
        blocks = moscow_block(label, clr, items)
        for b in blocks:
            el.append(b)
        el.append(sp(4))

    el.append(sp(8))

    # ── Pricing ──
    el.append(banner("10. PRICING HYPOTHESIS", "Test these tiers before committing"))
    el.append(sp(8))
    pricing = [
        ["Tier", "Price", "Includes", "Target Segment", "Goal"],
        ["Free",    "Rs. 0/mo",   "3-week roadmap, basic skills gap",   "All students (acquisition)", "Reach & virality"],
        ["Pro",     "Rs. 99/mo",  "Full roadmap, resources, tracker",   "Motivated students",          "Primary revenue"],
        ["Elite",   "Rs. 299/mo", "Pro + project plans + cert guide",   "Placement-focused students",  "ARPU growth"],
        ["College", "Rs. 2L/yr",  "White-label for 500 students",       "Placement cells",             "B2B revenue"],
    ]
    el.append(tbl(pricing[0], pricing[1:], cw=[50, 75, 165, 120, CW-410]))
    el.append(sp(6))
    el.append(callout("💡 <b>Pricing Hypothesis to Test:</b> Run an A/B test — 50 students see "
                      "Rs.99 pricing, 50 see Rs.149. Track conversion and churn over 30 days "
                      "before locking in the price.",
                      bg=colors.HexColor("#F0FDF4"), border=GREEN))
    el.append(PageBreak())
    return el

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 6 — RISKS + 30-DAY PLAN + ACTIONS + SCORES + VERDICT
# ═══════════════════════════════════════════════════════════════════════════════
def risks_plan_verdict():
    el = []

    # ── Risks ──
    el.append(banner("11. TOP 5 RISKS", "Know these before you build"))
    el.append(sp(8))
    risks = [
        ["#", "Risk", "Prob.", "Impact", "Mitigation"],
        ["1", "ChatGPT adds structured career UX",         "High",   "High",
         "Build moat via India data, college partnerships, outcomes tracking"],
        ["2", "Students won't pay — price sensitivity",   "High",   "High",
         "Strong freemium; primary revenue via B2B college licensing"],
        ["3", "AI gives wrong career advice (hallucination)","Medium","High",
         "Curated roadmap templates + source citations + user feedback loop"],
        ["4", "Founder builds alone — bandwidth risk",     "Medium", "Medium",
         "No-code MVP first (Bubble/Framer + GPT API); find co-founder"],
        ["5", "No validation before building",             "High",   "High",
         "DO NOT BUILD until 30-day sprint is done — see plan below"],
    ]
    el.append(tbl(risks[0], risks[1:], cw=[18, 165, 45, 50, CW-278]))
    el.append(sp(10))

    # ── 30-Day Plan ──
    el.append(banner("12. 30-DAY MVP PLAN", "Execute this before writing any code"))
    el.append(sp(8))
    plan = [
        ["Week", "Focus", "Key Actions", "Output"],
        ["Wk 1\nDays 1–7",  "Validate Problem",
         "20 student interviews (JTBD framework); score pain severity",
         "Pain point ranking doc"],
        ["Wk 2\nDays 8–14", "Validate Solution",
         "Build landing page (Carrd); share in 5 college WhatsApp groups; collect 100+ emails",
         "100+ waitlist signups"],
        ["Wk 3\nDays 15–21","Validate WTP",
         "Show 3-tier pricing to 50 students; pitch 5 college placement cells for pilot",
         "Pricing data + 1 pilot lead"],
        ["Wk 4\nDays 22–30","Prepare to Build",
         "Define MVP scope; explore no-code tools; post for co-founder; draft 1-pager for angels",
         "MVP spec + co-founder lead"],
    ]
    el.append(tbl(plan[0], plan[1:], cw=[55, 85, 200, CW-340]))
    el.append(sp(10))

    # ── Founder Action Sheet ──
    el.append(banner("13. FOUNDER ACTION SHEET", "Top 10 next actions — start today"))
    el.append(sp(8))
    actions = [
        ["#", "Action", "Timeline", "Priority"],
        ["1", "Write 10 problem hypotheses; choose top 3 to test", "Day 1",    "🔴 Critical"],
        ["2", "Conduct 20 student interviews using JTBD framework", "Days 2–5", "🔴 Critical"],
        ["3", "Build a 1-page landing page with email capture",     "Days 6–7", "🔴 Critical"],
        ["4", "Share landing page in 5+ college WhatsApp groups",   "Day 8",    "🔴 Critical"],
        ["5", "Call 10 students who signed up — validate in depth", "Days 9–12","🔴 Critical"],
        ["6", "Test pricing with 50 students (Rs.99 vs Rs.149)",    "Days 13–15","🟠 High"],
        ["7", "Email 10 college placement officers for pilot talks", "Days 14–18","🟠 High"],
        ["8", "Interview 5 HR managers on intern skill expectations","Days 16–20","🟠 High"],
        ["9", "Define v1 MVP scope (1 feature only — roadmap)",     "Day 21",   "🟠 High"],
        ["10","Post for technical co-founder on LinkedIn + AngelList","Days 22–30","🟡 Medium"],
    ]
    el.append(tbl(actions[0], actions[1:], cw=[18, 220, 80, CW-318]))
    el.append(sp(10))

    # ── Scores ──
    el.append(banner("14. SCORES (0–100)", "Current state assessment"))
    el.append(sp(8))
    score_items = [
        ("Customer Clarity — How well-defined is your target user?", 72, 100, ACCENT),
        ("Problem Severity — How painful and urgent is the problem?", 80, 100, GREEN),
        ("PMF Potential — Does the market want this solution?",       65, 100, TEAL),
        ("MVP Readiness — Ready to start building right now?",        30, 100, AMBER),
    ]
    for label, val, mx, clr in score_items:
        el.append(score_bar(label, val, mx, clr))
    el.append(sp(10))

    # ── Final Verdict ──
    el.append(banner("15. FINAL VERDICT"))
    el.append(sp(8))
    verdict_box = Table([[
        Paragraph(
            "🟡 &nbsp;<b>PROMISING BUT UNVALIDATED</b><br/><br/>"
            "The AI Career Mentor targets a real, large, and underserved problem. "
            "The market timing is excellent. No competitor owns the end-to-end "
            "'career OS for students' in India. The idea deserves to be built — "
            "<b>but not yet.</b><br/><br/>"
            "Complete the 30-day validation sprint first. If you hit these gates:<br/>"
            "✅ 50 student interviews &nbsp;|&nbsp; ✅ 100+ waitlist signups &nbsp;|&nbsp; "
            "✅ 1 college pilot lead &nbsp;|&nbsp; ✅ Pricing data collected<br/><br/>"
            "<b>→ Then build the MVP. Then raise. Then scale.</b>",
            S("vt", fontSize=9.5, textColor=WHITE, fontName="Helvetica",
              leading=16, alignment=TA_LEFT))
    ]], colWidths=[CW])
    verdict_box.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), INDIGO),
        ("BOX",(0,0),(-1,-1), 2, AMBER),
        ("LEFTPADDING",(0,0),(-1,-1),16),("RIGHTPADDING",(0,0),(-1,-1),16),
        ("TOPPADDING",(0,0),(-1,-1),14), ("BOTTOMPADDING",(0,0),(-1,-1),14),
    ]))
    el.append(verdict_box)
    el.append(sp(14))

    # Footer
    footer = Table([[
        Paragraph("AI Career Mentor — Customer &amp; MVP Blueprint", sSmall),
        Paragraph("Confidential | AI Product Strategy Engine | June 2025",
                  S("fr", fontSize=7, textColor=DGRAY, alignment=TA_RIGHT, fontName="Helvetica")),
    ]], colWidths=[CW/2, CW/2])
    footer.setStyle(TableStyle([
        ("LINEABOVE",(0,0),(-1,-1),0.5,MGRAY),
        ("TOPPADDING",(0,0),(-1,-1),6),
        ("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),0),
    ]))
    el.append(footer)
    return el

# ═══════════════════════════════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════════════════════════════
def build(path):
    doc = SimpleDocTemplate(
        path, pagesize=A4,
        leftMargin=M, rightMargin=M, topMargin=M, bottomMargin=M,
        title="Customer & MVP Blueprint — AI Career Mentor",
        author="AI Product Strategy Engine",
    )
    story = []
    story += cover()
    story += exec_icp_persona()
    story += pain_journey()
    story += obj_trig_mvp()
    story += moscow_pricing_risks()
    story += risks_plan_verdict()
    doc.build(story)
    print(f"Saved: {path}")

build("/mnt/user-data/outputs/Customer_MVP_Blueprint_AI_Career_Mentor.pdf")
