# -*- coding: utf-8 -*-
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image,
                                PageBreak, Table, TableStyle, KeepTogether)
import os

FD = "/usr/share/fonts/truetype/nanum"
pdfmetrics.registerFont(TTFont("KR",  os.path.join(FD, "NanumBarunGothic.ttf")))
pdfmetrics.registerFont(TTFont("KRB", os.path.join(FD, "NanumBarunGothicBold.ttf")))
pdfmetrics.registerFontFamily("KR", normal="KR", bold="KRB")

IMG = "/home/user/AICP-/images/png"
ACCENT = colors.HexColor("#1F4E79")
GREY   = colors.HexColor("#595959")
LINE   = colors.HexColor("#BFBFBF")

PW, PH = A4
M = 42
CW = PW - 2*M

S = dict(
 title   = ParagraphStyle("t", fontName="KRB", fontSize=17, leading=23, alignment=TA_CENTER,
                          textColor=ACCENT, spaceAfter=4),
 sub     = ParagraphStyle("s", fontName="KR", fontSize=10, leading=14, alignment=TA_CENTER,
                          textColor=GREY, spaceAfter=14),
 sect    = ParagraphStyle("se", fontName="KRB", fontSize=12.5, leading=17, textColor=ACCENT,
                          spaceBefore=6, spaceAfter=7),
 body    = ParagraphStyle("b", fontName="KR", fontSize=9.6, leading=15, alignment=TA_JUSTIFY,
                          spaceAfter=5),
 bullet  = ParagraphStyle("bu", fontName="KR", fontSize=9.6, leading=15, leftIndent=12,
                          firstLineIndent=-12, alignment=TA_JUSTIFY, spaceAfter=3),
 q       = ParagraphStyle("q", fontName="KRB", fontSize=10, leading=15, spaceBefore=7, spaceAfter=3),
 qnote   = ParagraphStyle("qn", fontName="KR", fontSize=8.8, leading=13, textColor=GREY, spaceAfter=4),
 opt     = ParagraphStyle("o", fontName="KR", fontSize=9.4, leading=15, leftIndent=13, spaceAfter=1),
 lead    = ParagraphStyle("l", fontName="KRB", fontSize=10.5, leading=15, spaceAfter=7),
 trial   = ParagraphStyle("tr", fontName="KRB", fontSize=13, leading=18, textColor=ACCENT, spaceAfter=5),
 small   = ParagraphStyle("sm", fontName="KR", fontSize=8.6, leading=12.5, textColor=GREY, spaceAfter=3),
)

def P(t, st="body"):  return Paragraph(t, S[st])
def opts(items):      return [Paragraph("○&nbsp;&nbsp;" + i, S["opt"]) for i in items]

def scale(labels):
    """0-10 슬라이더 표현"""
    cells = [[str(i) for i in range(11)]]
    t = Table(cells, colWidths=[ (CW-20)/11 ]*11, rowHeights=[17])
    t.setStyle(TableStyle([
        ("FONT",(0,0),(-1,-1),"KR",9),
        ("ALIGN",(0,0),(-1,-1),"CENTER"),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("GRID",(0,0),(-1,-1),0.5,LINE),
        ("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),0),
    ]))
    return [Paragraph(labels, S["qnote"]), t, Spacer(1,4)]

def rule(space_before=6, space_after=6):
    t = Table([[""]], colWidths=[CW], rowHeights=[0.1])
    t.setStyle(TableStyle([("LINEABOVE",(0,0),(-1,0),0.7,LINE)]))
    return [Spacer(1,space_before), t, Spacer(1,space_after)]

# ---------------- 공통 문항 ----------------
Q1 = ("문항1. 이번 회의에서 연준은 평소 회의와 비교해 앞으로의 경제 상황을 어떻게 전망하고 "
      "있다고 보십니까?")
Q1N = ("('평소 회의'란 최근 몇 년간 열렸던 FOMC 회의들의 평균적인 수준을 뜻합니다. "
       "확실하지 않더라도, 자료를 보고 받으신 인상대로 하나를 골라 주세요.)")
Q2 = "문항2. 이번 회의에서 연준의 전망은 얼마나 낙관적이었다고 생각하십니까?"
Q2N = "(0 = 매우 비관 · 5 = 평소 수준 · 10 = 매우 낙관)"
Q3 = ("문항3. 미국 주식을 보유하고 계시다고 가정해 주세요. 이 자료를 보고, 보유 비중을 "
      "어떻게 조정하고 싶으십니까?")
Q3N = "(0 = 많이 줄이고 싶다 · 5 = 그대로 두고 싶다 · 10 = 많이 늘리고 싶다)"
Q4 = "문항4. 앞의 세 문항에 답하시면서, 본인의 판단에 얼마나 확신이 있으셨습니까?"
Q4N = "(0 = 전혀 확신할 수 없다 · 5 = 보통이다 · 10 = 매우 확신한다)"

TRIALS = [(1,"A","2021","2021년 4월"), (2,"C","2024","2024년 1월"),
          (3,"B","2023","2023년 6월"), (4,"D","2025","2025년 1월")]

def build(kind, filekind, outfile, group_label):
    """kind: 응답자 표기 / filekind: 파일명 표기"""
    st = []
    # ---- 표지 + 동의 ----
    st += [P("FOMC 회의 자료 해석 설문", "title"),
           P(f"{group_label} · 설문지 전문 (인쇄본)", "sub")]
    st += [P("[연구 참여 동의]", "sect")]
    st += [P("본 설문은 UNIST 경영과학부 AICP 연구 프로젝트의 일환으로 진행되는 조사입니다. (팀 : EconPilot)"),
           P("참여 전에 아래 내용을 읽어 주세요.")]
    st += [P("■ 무엇을 하나요?", "q"),
           P("미국 연방공개시장위원회(FOMC) 회의와 관련된 자료를 네 차례 보시고, 각 자료에 대한 문항에 "
             "답하시면 됩니다. 전체 소요 시간은 약 9분입니다.")]
    st += [P("■ 어떤 정보를 수집하나요?", "q"),
           P("응답 내용, 투자 경험 여부, 연령대만 수집합니다. 수집된 응답은 통계 처리되어 집단 단위로만 "
             "보고되며, 개별 응답이 공개되는 일은 없습니다.")]
    st += [P("■ 참여는 자유입니다.", "q"),
           P("참여를 원하지 않으시면 언제든 창을 닫으셔도 됩니다.")]
    st += [P("■ 유의 사항", "q"),
           P("본 설문에 제시되는 모든 자료는 연구 목적의 예시이며, 투자 조언이 아닙니다.")]
    st += [P("■ 문의", "q"), P("최인영 / dlsdud0510@unist.ac.kr")]
    st += rule()
    st += [P("위 내용을 모두 읽었으며, 연구 참여에 동의합니다.", "lead")]
    st += opts(["동의합니다", "동의하지 않습니다"])
    st += [PageBreak()]

    # ---- 참가자 정보 + 과제 안내 ----
    st += [P("[참가자 정보]", "sect")]
    st += [P("1. 참가자 번호", "q"),
           P("진행자가 안내해 드린 두 자리 번호를 입력해 주세요. (예: 11, 12)", "qnote"),
           Paragraph("<font color='#999999'>______________________</font>", S["opt"]), Spacer(1,4)]
    st += [P("2. 현재 또는 과거에 주식·펀드·ETF 등에 직접 투자해 본 경험이 있으십니까?", "q")]
    st += opts(["있다", "없다"])
    st += [P("3. 연령대를 선택해 주세요.", "q")]
    st += opts(["20대", "30대", "40대 이상"])
    st += rule(14, 8)
    st += [P("[과제 안내]", "sect")]
    st += [P("■ 상황", "q"),
           P("지금부터 실제 있었던 미국 연준(Fed)의 통화정책 회의(FOMC)와 관련된 자료를 네 차례 "
             "보시게 됩니다.")]
    st += [P("■ 자료를 보시는 동안, 꼭 지켜 주세요.", "q"),
           P("· 다음으로 넘어가신 뒤에는 이전 화면으로 돌아가지 말아 주세요.", "bullet"),
           P("· 중간에 멈추지 마시고 한 번에 끝까지 진행해 주세요.", "bullet"),
           P("· 검색하거나 다른 자료를 찾아보지 마시고, 화면에 보이는 자료만으로 판단해 주세요.", "bullet")]
    st += [Spacer(1,4), P("준비가 되셨으면 아래 'Next page'을 눌러 주세요.")]
    st += [PageBreak()]

    # ---- 시행 1~4 ----
    for n, sid, year, when in TRIALS:
        path = os.path.join(IMG, f"{sid}_{year}_{filekind}.png")
        iw = CW - 60
        ih = iw * 1500.0 / 2000.0
        st += [P(f"시행 {n}", "trial"),
               P(f"아래는 {when} 미국 FOMC 회의에 대한 {kind}입니다.", "lead"),
               Image(path, width=iw, height=ih, hAlign="CENTER"),
               Spacer(1, 9)]
        st += [P(Q1, "q"), P(Q1N, "qnote")]
        st += opts(["평소보다 낙관적이었다", "평소보다 비관적이었다"])
        st += [P(Q2, "q")] + scale(Q2N)
        st += [P(Q3, "q")] + scale(Q3N)
        st += [P(Q4, "q")] + scale(Q4N)
        st += [PageBreak()]

    # ---- 사후 문항 ----
    st += [P("[사후 문항]", "sect")]
    st += [P("1. 설문에 얼마나 집중해서 응답하셨습니까?", "q")]
    st += opts(["매우 집중했다", "대체로 집중했다", "보통이다", "집중하지 못했다"])
    st += [P("2. 응답 중에 검색하거나 다른 자료를 참고하신 적이 있습니까?", "q"),
           P("사실대로 답하셔도 어떠한 불이익도 없습니다.", "qnote")]
    st += opts(["없다", "한두 번 있다", "여러 번 있다"])
    st += [P("3. 자료를 보고 판단하실 때 어려운 점이 있었다면 자유롭게 적어 주세요.", "q"),
           Paragraph("<font color='#999999'>" + "_"*72 + "</font>", S["opt"]),
           Paragraph("<font color='#999999'>" + "_"*72 + "</font>", S["opt"])]
    st += [PageBreak()]

    # ---- 디브리핑 ----
    st += [P("[설문을 마치며]", "sect")]
    st += [P("참여해 주셔서 감사합니다. 어떤 연구였는지 간단히 안내드립니다.")]
    st += [P("■ 방금 보신 자료에 대해", "q"),
           P("네 자료는 모두 실제로 열렸던 FOMC 회의의 자료입니다. 설문지 종류에 따라 형식만 두 가지로 "
             "달랐습니다. 하나는 그날 보도된 뉴스 기사이고, 다른 하나는 그날의 회의 문서(성명문·기자회견)의 "
             "어조를 수치로 요약한 분석 화면입니다.")]
    st += [P("■ 이 연구가 알아보려는 것", "q"),
           P("같은 회의라도 어떤 형식으로 정보를 접하느냐에 따라 사람들의 해석과 행동 의향이 달라지는지를 "
             "살펴봅니다.")]
    st += [P("■ 왜 '평소와 비교해'를 물었나", "q"),
           P("연준의 회의 문서는 대체로 조심스럽고 긍정적인 표현으로 쓰입니다. 실제로 2012년 이후 열린 "
             "FOMC 회의 성명문의 약 73%가 절대 기준으로 양(+)의 어조 점수를 받았습니다. 그래서 한 회의의 "
             "문서를 그 자체로만 읽으면 거의 항상 '낙관적'으로 보입니다. 의미 있는 판단은 '평소 회의에 비해 "
             "이번이 더 낙관적인가, 더 신중한가'입니다. 설문에서 '평소보다'를 계속 강조한 이유입니다.")]
    st += [P("■ 응답 결과에 대해", "q"),
           P("개별 응답의 맞고 틀림은 알려드리지 않습니다. 이 연구는 개인의 정확도를 평가하지 않으며, "
             "참가자 전체의 응답 경향만을 분석합니다.")]
    st += [P("■ 한 가지 부탁드립니다", "q"),
           P("아직 참여하지 않은 분들이 있습니다. 설문 내용을 주변에 알리지 말아 주세요.")]
    st += rule()
    st += [P("문의 : 최인영 / dlsdud0510@unist.ac.kr", "small"),
           P("아래 '제출'을 누르시면 응답이 저장되고 설문이 끝납니다.", "small")]

    def footer(canv, doc):
        canv.saveState()
        canv.setFont("KR", 7.5); canv.setFillColor(GREY)
        canv.drawString(M, 22, f"FOMC 회의 자료 해석 설문 · {group_label}")
        canv.drawRightString(PW - M, 22, f"{doc.page}")
        canv.setStrokeColor(LINE); canv.setLineWidth(0.4)
        canv.line(M, 33, PW - M, 33)
        canv.restoreState()

    doc = SimpleDocTemplate(outfile, pagesize=A4,
                            leftMargin=M, rightMargin=M, topMargin=M, bottomMargin=40,
                            title=f"FOMC 회의 자료 해석 설문 ({group_label})",
                            author="EconPilot")
    doc.build(st, onFirstPage=footer, onLaterPages=footer)
    return outfile

a = build("기사", "기사", "설문지_언론군.pdf", "언론군")
b = build("도표", "대시보드", "설문지_도표군.pdf", "도표군")
for f in (a, b):
    print(f, os.path.getsize(f)//1024, "KB")
