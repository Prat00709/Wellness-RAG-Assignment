def check_safety(query: str):
    query = query.lower()

    pregnancy_keywords = [
        "pregnant", "pregnancy", "trimester", "prenatal"
    ]

    medical_keywords = [
        "hernia", "glaucoma", "high blood pressure",
        "bp", "hypertension", "surgery", "injury",
        "chronic pain", "operation"
    ]

    for word in pregnancy_keywords:
        if word in query:
            return {"isUnsafe": True, "reason": "pregnancy"}

    for word in medical_keywords:
        if word in query:
            return {"isUnsafe": True, "reason": "medical_condition"}

    return {"isUnsafe": False, "reason": None}
