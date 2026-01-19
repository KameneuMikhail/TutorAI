import azure.functions as func
import json
import logging

# Localized subjects mapping
SUBJECTS = {
    "ru": ["Математика", "Английский"],
    "en": ["Math", "English"]
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
        if lang in SUBJECTS:
            return lang
    
    # Check Accept-Language header
    accept_lang = req.headers.get('Accept-Language', '')
    if accept_lang:
        for lang_part in accept_lang.split(','):
            lang = lang_part.strip().split(';')[0].lower()[:2]
            if lang in SUBJECTS:
                return lang
    
    # Default to Russian if no localization in request
    return DEFAULT_LANG


def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Azure Function that returns localized list of subjects.
    Applies localization from request (query param or header), defaults to Russian.
    """
    logging.info('Python HTTP trigger function processed a request.')
    
    try:
        # Get language from request, default to Russian
        language = get_language_from_request(req)
        logging.info(f'Language from request: {language}')
        
        # Apply localization - get subjects for the detected language
        subjects = SUBJECTS.get(language, SUBJECTS[DEFAULT_LANG])
        
        logging.info(f'Returning subjects in {language}: {subjects}')
        
        # Return response with CORS headers and proper UTF-8 encoding
        response_body = json.dumps(subjects, ensure_ascii=False)
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
        logging.error(f'Error processing request: {str(e)}', exc_info=True)
        return func.HttpResponse(
            json.dumps({"error": "Internal server error", "message": str(e)}),
            mimetype="application/json",
            status_code=500
        )
