from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

styles = getSampleStyleSheet()

def create_report(result):

    pdf = SimpleDocTemplate("Resume_Report.pdf")

    story = []

    parsed = result["resume_data"]

    info = parsed["basic_info"]

    story.append(Paragraph("<b>AI Resume Intelligence Report</b>", styles["Title"]))

    story.append(Paragraph(f"<br/>Name : {info['name']}", styles["Normal"]))
    story.append(Paragraph(f"Email : {info['email']}", styles["Normal"]))
    story.append(Paragraph(f"Phone : {info['phone']}", styles["Normal"]))

    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(Paragraph(f"ATS Score : {parsed['ats_score']}%", styles["Heading2"]))

    story.append(Paragraph(f"Job Match Score : {result['match_score']}%", styles["Heading2"]))

    story.append(Paragraph("<br/><b>Matched Skills</b>", styles["Heading2"]))

    for skill in result["matched_skills"]:
        story.append(Paragraph(skill, styles["Normal"]))

    story.append(Paragraph("<br/><b>Missing Skills</b>", styles["Heading2"]))

    for skill in result["missing_skills"]:
        story.append(Paragraph(skill, styles["Normal"]))

    story.append(Paragraph("<br/><b>Extracted Skills</b>", styles["Heading2"]))

    for skill in parsed["skills"]:
        story.append(Paragraph(skill, styles["Normal"]))

    pdf.build(story)

    return "Resume_Report.pdf"