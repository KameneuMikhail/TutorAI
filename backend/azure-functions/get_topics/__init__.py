import azure.functions as func
import json
import logging

# Topics for 4th grade Polish school curriculum
# Localized topics for Math and English
TOPICS = {
    "ru": {
        "Math": [
            "Сложение и вычитание в пределах 1000",
            "Умножение и деление",
            "Дроби (половина, четверть, треть)",
            "Геометрия: фигуры и их свойства",
            "Измерение длины, массы, времени",
            "Решение текстовых задач",
            "Работа с таблицами и диаграммами",
            "Периметр и площадь простых фигур"
        ],
        "English": [
            "Базовый словарный запас (семья, школа, дом)",
            "Простые предложения (Present Simple)",
            "Чтение и понимание коротких текстов",
            "Основы грамматики (артикли, множественное число)",
            "Диалоги и разговорные фразы",
            "Описание предметов и людей",
            "Время и распорядок дня",
            "Письмо простых предложений"
        ]
    },
    "en": {
        "Math": [
            "Addition and subtraction within 1000",
            "Multiplication and division",
            "Fractions (half, quarter, third)",
            "Geometry: shapes and their properties",
            "Measurement of length, mass, time",
            "Solving word problems",
            "Working with tables and charts",
            "Perimeter and area of simple shapes"
        ],
        "English": [
            "Basic vocabulary (family, school, home)",
            "Simple sentences (Present Simple)",
            "Reading and understanding short texts",
            "Grammar basics (articles, plural forms)",
            "Dialogues and conversational phrases",
            "Describing objects and people",
            "Time and daily routines",
            "Writing simple sentences"
        ]
    }
}

# Subject mapping for different languages
SUBJECT_MAPPING = {
    "ru": {
        "Math": "Math",
        "Математика": "Math",
        "English": "English",
        "Английский": "English"
    },
    "en": {
        "Math": "Math",
        "Математика": "Math",
        "English": "English",
        "Английский": "English"
    }
}

# Default language
DEFAULT_LANG = "ru"


def get_language_from_request(req: func.HttpRequest) -> str:
    """
    Extract language from request.
    Checks query parameter 'lang' or 'language', then Accept-Language header.
    Returns 'ru' (Russian) if no valid language found in request.
    """
    # Check query parameters
    lang = req.params.get('lang') or req.params.get('language')
    if lang:
        lang = lang.lower()[:2]
        if lang in TOPICS:
            return lang
    
    # Check Accept-Language header
    accept_lang = req.headers.get('Accept-Language', '')
    if accept_lang:
        for lang_part in accept_lang.split(','):
            lang = lang_part.strip().split(';')[0].lower()[:2]
            if lang in TOPICS:
                return lang
    
    # Default to Russian if no localization in request
    return DEFAULT_LANG


def get_subject_from_request(req: func.HttpRequest, language: str) -> str:
    """
    Extract subject from request.
    Checks query parameter, then request body (JSON), then route parameter.
    Returns None if subject not found.
    """
    # Check query parameter
    subject = req.params.get('subject')
    if subject:
        # Normalize subject name
        subject_normalized = subject.strip()
        mapping = SUBJECT_MAPPING.get(language, SUBJECT_MAPPING[DEFAULT_LANG])
        if subject_normalized in mapping:
            return mapping[subject_normalized]
        # Try case-insensitive match
        for key, value in mapping.items():
            if key.lower() == subject_normalized.lower():
                return value
    
    # Check request body (for POST requests)
    try:
        req_body = req.get_json()
        if req_body and 'subject' in req_body:
            subject = req_body['subject']
            subject_normalized = subject.strip()
            mapping = SUBJECT_MAPPING.get(language, SUBJECT_MAPPING[DEFAULT_LANG])
            if subject_normalized in mapping:
                return mapping[subject_normalized]
            # Try case-insensitive match
            for key, value in mapping.items():
                if key.lower() == subject_normalized.lower():
                    return value
    except ValueError:
        # Not JSON or no body
        pass
    
    return None


def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Azure Function that returns topics for a specific subject.
    Subject should be passed via query parameter or request body.
    Returns topics for 4th grade Polish school curriculum.
    Supports Russian (default) and English localization.
    """
    logging.info('Python HTTP trigger function processed a request for topics.')
    
    try:
        # Get language from request, default to Russian
        language = get_language_from_request(req)
        logging.info(f'Language from request: {language}')
        
        # Get subject from request
        subject = get_subject_from_request(req, language)
        
        if not subject:
            return func.HttpResponse(
                json.dumps({
                    "error": "Subject parameter is required",
                    "message": "Please provide 'subject' parameter (Math or English) via query string or request body"
                }, ensure_ascii=False),
                mimetype="application/json; charset=utf-8",
                status_code=400,
                headers={
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                    "Access-Control-Allow-Headers": "Content-Type, Accept-Language"
                }
            )
        
        logging.info(f'Subject requested: {subject}')
        
        # Get topics for the subject and language
        topics = TOPICS.get(language, TOPICS[DEFAULT_LANG]).get(subject)
        
        if not topics:
            return func.HttpResponse(
                json.dumps({
                    "error": "Subject not found",
                    "message": f"Topics not available for subject: {subject}. Available subjects: Math, English"
                }, ensure_ascii=False),
                mimetype="application/json; charset=utf-8",
                status_code=404,
                headers={
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                    "Access-Control-Allow-Headers": "Content-Type, Accept-Language"
                }
            )
        
        logging.info(f'Returning {len(topics)} topics for {subject} in {language}')
        
        # Return response with CORS headers and proper UTF-8 encoding
        response_body = json.dumps(topics, ensure_ascii=False)
        return func.HttpResponse(
            response_body.encode('utf-8'),
            mimetype="application/json; charset=utf-8",
            status_code=200,
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, Accept-Language",
                "Content-Language": language
            }
        )
    
    except Exception as e:
        # Log error with full traceback but only send safe string representation
        error_message = str(e) if e else "Unknown error"
        logging.error(f'Error processing request: {error_message}', exc_info=True)
        
        # Create safe error response - only use string representation
        try:
            error_response = {
                "error": "Internal server error",
                "message": error_message
            }
            response_body = json.dumps(error_response, ensure_ascii=False)
        except Exception as json_error:
            # Fallback if JSON serialization fails
            response_body = json.dumps({"error": "Internal server error"}, ensure_ascii=False)
            logging.error(f'Error serializing error response: {str(json_error)}')
        
        return func.HttpResponse(
            response_body.encode('utf-8'),
            mimetype="application/json; charset=utf-8",
            status_code=500,
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, Accept-Language"
            }
        )
