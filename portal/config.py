"""
Portal configuration — curriculum structure.

Each stage/lesson is defined here. When a lesson has an interactive Blueprint,
set 'has_app' to True and provide the steps list. The portal auto-discovers
and registers the Blueprint from portal/lessons/<folder>/__init__.py.
"""

STAGES = [
    {
        "id": "s1",
        "num": 1,
        "title": "Classic ML",
        "desc": "Foundations of machine learning with scikit-learn",
        "tier": "AI Foundations",
        "lessons": [
            {"id": "s1_01", "num": 1, "title": "What is ML?",
             "desc": "Explore the digits dataset interactively",
             "folder": "s1_01_what_is_ml", "has_app": True, "minutes": 100},
            {"id": "s1_02", "num": 2, "title": "Linear Regression",
             "desc": "Predict continuous values with a straight line",
             "folder": "s1_02_linear_regression", "has_app": False, "minutes": 90},
            {"id": "s1_03", "num": 3, "title": "Logistic Regression",
             "desc": "Binary classification and decision boundaries",
             "folder": "s1_03_logistic_regression", "has_app": False, "minutes": 90},
            {"id": "s1_04", "num": 4, "title": "Decision Trees",
             "desc": "Tree-based models and feature importance",
             "folder": "s1_04_decision_trees", "has_app": False, "minutes": 90},
            {"id": "s1_05", "num": 5, "title": "Model Evaluation",
             "desc": "Metrics, cross-validation, and overfitting",
             "folder": "s1_05_model_evaluation", "has_app": False, "minutes": 90},
        ],
    },
    {
        "id": "s2",
        "num": 2,
        "title": "Intermediate ML",
        "desc": "Feature engineering, ensembles, and unsupervised learning",
        "tier": "AI Foundations",
        "lessons": [
            {"id": "s2_01", "num": 1, "title": "Feature Engineering",
             "desc": "Transform raw data into useful features",
             "folder": "s2_01_feature_engineering", "has_app": True, "minutes": 90},
            {"id": "s2_02", "num": 2, "title": "Random Forests",
             "desc": "Ensemble methods and bagging",
             "folder": "s2_02_random_forests", "has_app": False, "minutes": 90},
            {"id": "s2_03", "num": 3, "title": "Clustering & Anomaly Detection",
             "desc": "Unsupervised learning for security",
             "folder": "s2_03_clustering_anomaly", "has_app": False, "minutes": 90},
            {"id": "s2_04", "num": 4, "title": "Overfitting & Cross-Validation",
             "desc": "Generalization and model selection",
             "folder": "s2_04_overfitting_crossval", "has_app": False, "minutes": 90},
        ],
    },
    {
        "id": "s3",
        "num": 3,
        "title": "Neural Networks",
        "desc": "Deep learning from perceptrons to CNNs",
        "tier": "AI Practitioner",
        "lessons": [
            {"id": "s3_01", "num": 1, "title": "First Neural Network",
             "desc": "Build a neural network from scratch",
             "folder": "s3_01_first_neural_network", "has_app": True, "minutes": 120},
            {"id": "s3_02", "num": 2, "title": "Dropout & Regularisation",
             "desc": "Prevent overfitting in deep networks",
             "folder": "s3_02_dropout_regularisation", "has_app": False, "minutes": 90},
            {"id": "s3_03", "num": 3, "title": "Convolutional Networks",
             "desc": "Image recognition with CNNs",
             "folder": "s3_03_convolutional_networks", "has_app": False, "minutes": 120},
            {"id": "s3_04", "num": 4, "title": "Hyperparameter Tuning",
             "desc": "Systematic model optimization",
             "folder": "s3_04_hyperparameter_tuning", "has_app": False, "minutes": 90},
        ],
    },
    {
        "id": "s4",
        "num": 4,
        "title": "Generative AI",
        "desc": "LLMs, APIs, RAG, and prompt engineering",
        "tier": "AI Ninja",
        "lessons": [
            {"id": "s4_01", "num": 1, "title": "How LLMs Work",
             "desc": "Transformers, tokens, and attention",
             "folder": "s4_01_how_llms_work", "has_app": False, "minutes": 90},
            {"id": "s4_02", "num": 2, "title": "Hugging Face",
             "desc": "Open-source model hub and inference",
             "folder": "s4_02_huggingface", "has_app": False, "minutes": 90},
            {"id": "s4_03", "num": 3, "title": "LLM APIs",
             "desc": "Building applications with LLM APIs",
             "folder": "s4_03_llm_api", "has_app": False, "minutes": 90},
            {"id": "s4_04", "num": 4, "title": "RAG",
             "desc": "Retrieval-Augmented Generation",
             "folder": "s4_04_rag", "has_app": False, "minutes": 120},
        ],
    },
    {
        "id": "s5",
        "num": 5,
        "title": "CP AI Security",
        "desc": "Check Point AI product positioning and demos",
        "tier": "AI Ninja",
        "lessons": [
            {"id": "s5_01", "num": 1, "title": "Workforce AI Security",
             "desc": "Securing workforce AI usage",
             "folder": "s5_01_workforce_ai_security", "has_app": False, "minutes": 60},
            {"id": "s5_02", "num": 2, "title": "AI Agent Security",
             "desc": "Protecting autonomous AI agents",
             "folder": "s5_02_ai_agent_security", "has_app": False, "minutes": 60},
            {"id": "s5_03", "num": 3, "title": "AI Guardrails",
             "desc": "Content safety and policy enforcement",
             "folder": "s5_03_ai_guardrails", "has_app": False, "minutes": 60},
            {"id": "s5_04", "num": 4, "title": "Positioning CP AI",
             "desc": "Technical depth for customer engagements",
             "folder": "s5_04_positioning_cp_ai", "has_app": False, "minutes": 60},
        ],
    },
]


def get_all_lessons():
    """Flat list of all lessons with stage info attached."""
    lessons = []
    for stage in STAGES:
        for lesson in stage["lessons"]:
            lessons.append({**lesson, "stage_id": stage["id"], "stage_title": stage["title"], "stage_num": stage["num"]})
    return lessons


def get_lesson(lesson_id):
    """Look up a lesson by its id (e.g. 's1_01')."""
    for stage in STAGES:
        for lesson in stage["lessons"]:
            if lesson["id"] == lesson_id:
                return {**lesson, "stage_id": stage["id"], "stage_title": stage["title"], "stage_num": stage["num"]}
    return None
