from decision_maker.models.enums import AvailableIndicators

INDICATORS_CHECKLIST = [
    {"label": label, "value": value}
    for label, value in zip(AvailableIndicators.labels, AvailableIndicators.names)
]

STYLE_MM_CHECKLIST = {
    "display": "inline-block",
    "margin-right": "20px",
    "margin-bottom": "50px",
}
