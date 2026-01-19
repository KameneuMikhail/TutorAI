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
        # Extract safe error message - only use string representation
        # Avoid passing exception objects to prevent serialization issues
        try:
            error_message = str(e) if e else "Unknown error"
            # Clean the error message to ensure it's JSON-safe
            error_message = error_message.replace('\n', ' ').replace('\r', ' ')[:500]
        except Exception:
            error_message = "Internal server error occurred"
        
        # Log error without exc_info to avoid serialization issues
        try:
            logging.error(f'Error processing request: {error_message}')
        except Exception:
            pass  # Silently fail logging if it causes issues
        
        # Create safe error response - only use string representation
        try:
            error_response = {
                "error": "Internal server error",
                "message": error_message
            }
            response_body = json.dumps(error_response, ensure_ascii=False)
        except Exception:
            # Fallback if JSON serialization fails
            response_body = json.dumps({"error": "Internal server error"}, ensure_ascii=False)
        
        try:
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
        except Exception:
            # Ultimate fallback - return minimal safe response
            return func.HttpResponse(
                b'{"error":"Internal server error"}',
                mimetype="application/json; charset=utf-8",
                status_code=500
            )
