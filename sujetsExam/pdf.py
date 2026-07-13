"""Renders a GeneratedExam into a paginated PDF (title, subject, level,
instructions, each exercise laid out like a real exam paper — heading,
statement, numbered questions — a running total, and page numbers) using
reportlab.
"""
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable,
)


def _add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica', 9)
    canvas.drawRightString(A4[0] - 2 * cm, 1.2 * cm, f"Page {doc.page}")
    canvas.restoreState()


def render_exam_pdf(exam) -> BytesIO:
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        topMargin=2 * cm, bottomMargin=2 * cm,
        leftMargin=2 * cm, rightMargin=2 * cm,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('ExamTitle', parent=styles['Title'], fontSize=18)
    meta_style = ParagraphStyle('ExamMeta', parent=styles['Normal'], fontSize=11, spaceAfter=4)
    instructions_style = ParagraphStyle('Instructions', parent=styles['Normal'], fontSize=10, leading=14)
    exercise_title_style = ParagraphStyle(
        'ExerciseTitle', parent=styles['Heading2'], fontSize=13,
        textColor=colors.HexColor('#1A3A6B'), spaceBefore=6, spaceAfter=6,
    )
    content_style = ParagraphStyle(
        'ExerciseContent', parent=styles['Normal'], fontSize=10.5, leading=14, spaceAfter=8,
    )
    question_style = ParagraphStyle(
        'Question', parent=styles['Normal'], fontSize=10.5, leading=15,
        leftIndent=14, spaceAfter=5,
    )

    items = list(
        exam.items.select_related('exercise').prefetch_related('exercise__questions').all()
    )
    total_marks = sum(item.marks for item in items)

    story = [
        Paragraph(exam.title, title_style),
        Spacer(1, 0.3 * cm),
        Paragraph(f"Matière : {exam.subject.subjectName}", meta_style),
        Paragraph(f"Niveau : {exam.level.level_name}", meta_style),
        Paragraph(f"Total des points : {total_marks}", meta_style),
        Spacer(1, 0.4 * cm),
    ]

    if exam.instructions:
        story.append(Paragraph("Instructions aux candidats", styles['Heading3']))
        story.append(Paragraph(exam.instructions, instructions_style))
        story.append(Spacer(1, 0.5 * cm))

    for index, item in enumerate(items, start=1):
        exercise = item.exercise
        story.append(
            Paragraph(f"Exercice {index} : {exercise.title} ({item.marks} pts)", exercise_title_style)
        )
        story.append(Paragraph(exercise.content, content_style))

        questions = list(exercise.questions.all())
        for q_index, question in enumerate(questions, start=1):
            marks_suffix = f" ({question.marks} pts)" if question.marks else ""
            story.append(Paragraph(f"{q_index}. {question.text}{marks_suffix}", question_style))

        if index < len(items):
            story.append(Spacer(1, 0.2 * cm))
            story.append(HRFlowable(width="100%", color=colors.HexColor('#D9E0EA'), thickness=0.75))
        story.append(Spacer(1, 0.4 * cm))

    doc.build(story, onFirstPage=_add_page_number, onLaterPages=_add_page_number)
    buffer.seek(0)
    return buffer
