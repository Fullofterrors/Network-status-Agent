
import hmac
import os


def authenticate_provider(api_key=None):
    """
    Verify a provider API key against the trusted
    key configured in the environment.

    Returns True only when both keys are present
    and match.
    """

    expected_key = os.environ.get("PROVIDER_API_KEY")

    if not isinstance(api_key, str) or not api_key:
        return False

    if not isinstance(expected_key, str) or not expected_key:
        return False

    return hmac.compare_digest(api_key, expected_key)