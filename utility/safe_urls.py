from flask import url_for, request
from urllib.parse import urlparse, urljoin


# Helper function to check if a URL is safe for redirection
def is_safe_url(target):
    # Parse the application's host URL
    ref_url = urlparse(request.host_url)
    # Parse the target URL to be tested
    test_url = urlparse(urljoin(request.host_url, target))
    # Check if the target URL's scheme is HTTP or HTTPS and belongs to the same domain
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc


# Function to perform safe redirection
def get_safe_redirect(redirect_route):
    # Get the referrer URL from the request
    destination = request.referrer
    # If the referrer URL exists and is safe, return it for redirection
    if destination and is_safe_url(destination):
        return destination
    # Otherwise, fallback to a safe internal route specified by 'redirect_route'
    return url_for(redirect_route)
