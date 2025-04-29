import json
from datetime import datetime

# Temporarily defining statically
ALLOWLISTS = {
    'apple': 'Apple Services',
    'cas': 'Certificate Authorities - CRL and OCSP',
    'captcha': 'CAPTCHA Services',
    'cdn': 'Content Distribution Networks',
    'disney': 'Disney Plus',
    'fb': 'Facebook',
    'fbm': 'Facebook Messenger',
    'hulu': 'Hulu',
    'insta': 'Instagram',
    'li': 'LinkedIn',
    'google': 'Google Services',
    'msft': 'Microsoft Services',
    'netflix': 'Netflix',
    'ntp': 'Network Time Protocol',
    'pmount': 'Paramount Plus',
    'push': 'Push 2FA Services',
    'pwmgr': 'Password Managers',
    'signal': 'Signal Messenger',
    'tiktok': 'TikTok',
    'whats': 'WhatsApp Messenger',
    'plex': 'Plex Media Server',
    'spot': 'Spotify',
    'snap': 'SnapChat'
}

# Returns error or False if no error
def invalid_request(event):
    
    # If no query string paramaters, cannot be valid. Error 400 - invalid request.
    if "queryStringParameters" not in event:
        return {
            'statusCode': 400,
            'body': 
                f"""# Status: 400 Invalid request. No query parameters."""
        }

    # If no include parameter, cannot be valid. Error 400 - invalid request.
    if "include" not in event["queryStringParameters"]:
        return {
            'statusCode': 400,
            'body': 
                f"""# Status: 400 Invalid request. Include query parameter is missing."""
        }

    # If include parameter empty, cannot be valid. Error 400 - invalid request.
    if event["queryStringParameters"]["include"] == "":
        return {
            'statusCode': 400,
            'body': 
                f"""# Status: 400 Invalid request. Include query parameter is empty."""
        }

    # If no token parameter, cannot be valid. Error 400 - invalid request.
    if "token" not in event["queryStringParameters"]:
        return {
            'statusCode': 400,
            'body': 
                f"""# Status: 400 Invalid request. Token include query parameter is missing."""
        }
    
    # If token parameter empty, cannot be valid. Error 400 - invalid request.
    if event["queryStringParameters"]["token"] == "":
        return {
            'statusCode': 400,
            'body': 
                f"""# Status: 400 Invalid request. Token query parameter is empty."""
        }
    
    # If token parameter is not 1234567890, authN failed. Error 401 - Unauthorized
    if event["queryStringParameters"]["token"] != "1234567890":
        return {
            'statusCode': 401,
            'body': 
                f"""# Status: 401 Unauthorized."""
        }
    
    return False 

def lambda_handler(event, context):

    # If the request is invalid, return error
    if (invalid := invalid_request(event)) != False:
        return invalid

    # Includes are added to aggregate list
    # Drops are ignored (not found)
    queryStringIncludes = ""
    queryStringDrops = ""

    # include=all will pull full allowlist contents
    if event["queryStringParameters"]["include"].lower().split(",") == ["all"]:
        for allowlist in ALLOWLISTS:
            queryStringIncludes += f"""#\t{allowlist} - {ALLOWLISTS[allowlist]}\n"""

        return {
            'statusCode': 200,
            'headers': { "content-type": "text/plain" },
            'body':
                f"""# Status: 200 Success\n"""
                f"""# Timestamp: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\n"""
                f"""# Requested:\n"""
                f"""{queryStringIncludes}"""
        }

    # Otherwise, we'll include whatever they list
    for queryStringInclude in event["queryStringParameters"]["include"].lower().split(","):
        if queryStringInclude in ALLOWLISTS:
            queryStringIncludes += f"""#\t{queryStringInclude} - {ALLOWLISTS[queryStringInclude]}\n"""
        else:
            queryStringDrops += f"""#\t{queryStringInclude}\n"""

    return {
        'statusCode': 200,
        'headers': { "content-type": "text/plain" },
        'body': 
            f"""# Status: 200 Success\n"""
            f"""# Timestamp: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\n"""
            f"""# Requested:\n"""
            f"""{queryStringIncludes}"""
            f"""# Ignored:\n"""
            f"""{queryStringDrops}"""
    }

