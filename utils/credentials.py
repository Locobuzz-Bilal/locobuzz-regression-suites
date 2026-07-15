# """Credential helper utilities.

# Loads sensitive values (like usernames/passwords) from environment variables.
# Keep your real secrets inside a local .env file that is NOT committed to Git.

# Example .env entries:
#     FB_USERNAME=your_facebook_username
#     FB_PASSWORD=your_facebook_password

# Usage:
#     from utils.credentials import get_fb_creds
#     username, password = get_fb_creds()
# """

# from __future__ import annotations

# import os
# from typing import Tuple


# def get_fb_creds() -> Tuple[str, str]:
#     """Return Facebook (Meta) login credentials from environment variables.

#     Returns:
#         (username, password)

#     Raises:
#         RuntimeError: if either FB_USERNAME or FB_PASSWORD is missing.
#     """
#     username = os.getenv("FB_USERNAME")
#     password = os.getenv("FB_PASSWORD")
#     if not username or not password:
#         raise RuntimeError(
#             "Missing Facebook credentials. Set FB_USERNAME and FB_PASSWORD in your .env or environment."
#         )
#     return username, password


# __all__ = ["get_fb_creds"]




# def get_twitter_creds() -> Tuple[str, str]:
#     """Return Twitter login credentials from environment variables.

#     Returns:
#         (username, password)

#     Raises:
#         RuntimeError: if either TWITTER_USERNAME or TWITTER_PASSWORD is missing.
#     """
#     username = os.getenv("TWITTER_USERNAME")
#     password = os.getenv("TWITTER_PASSWORD")
#     if not username or not password:
#         raise RuntimeError(
#             "Missing Twitter credentials. Set TWITTER_USERNAME and TWITTER_PASSWORD in your .env or environment."
#         )
#     return username, password


# __all__ = ["get_twitter_creds", "get_twitter_creds"]











# def get_workflow_creds():
#     """Get workflow automation test credentials"""
#     u = os.getenv("WORKFLOW_USERNAME")
#     p = os.getenv("WORKFLOW_PASSWORD")
#     if not u or not p:
#         raise RuntimeError(
#             "Missing Workflow credentials. Set WORKFLOW_USERNAME and WORKFLOW_PASSWORD in your .env or environment."
#         )
#     return u, p


















import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root (2 levels up from utils/credentials.py)
env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)

def get_twitter_creds():
    """Get Twitter test credentials"""
    u = os.getenv("TWITTER_USERNAME")
    p = os.getenv("TWITTER_PASSWORD")
    if not u or not p:
        raise RuntimeError(
            "Missing Twitter credentials. Set TWITTER_USERNAME and TWITTER_PASSWORD in your .env or environment."
        )
    return u, p

def get_twitter_csd_creds():
    """Get Twitter CSD credentials"""
    u = os.getenv("TWITTER_CSD")
    p = os.getenv("TWITTER_CSD_PASSWORD")
    if not u or not p:
        raise RuntimeError(
            "Missing Twitter CSD credentials. Set TWITTER_CSD and TWITTER_CSD_PASSWORD in your .env or environment."
        )
    return u, p

def get_twitter_ot_creds():
    """Get Twitter Open-Ticket (xagent) credentials"""
    u = os.getenv("TWITTER_AGENT_OT")
    p = os.getenv("TWITTER_AGENT_OT_PASSWORD")
    if not u or not p:
        raise RuntimeError(
            "Missing Twitter OT credentials. Set TWITTER_AGENT_OT and TWITTER_AGENT_OT_PASSWORD in your .env or environment."
        )
    return u, p

def get_instagram_creds():
    """Get Instagram test credentials"""
    u = os.getenv("INSTAGRAM_USERNAME")
    p = os.getenv("INSTAGRAM_PASSWORD")
    if not u or not p:
        raise RuntimeError(
            "Missing Instagram credentials. Set INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD in your .env or environment."
        )
    return u, p

def get_instagram_csd_creds():
    """Get Instagram CSD credentials"""
    u = os.getenv("INSTAGRAM_CSD")
    p = os.getenv("INSTAGRAM_CSD_PASSWORD")
    if not u or not p:
        raise RuntimeError(
            "Missing Instagram CSD credentials. Set INSTAGRAM_CSD and INSTAGRAM_CSD_PASSWORD in your .env or environment."
        )
    return u, p

def get_facebook_creds():
    """Get Facebook test credentials"""
    u = os.getenv("FB_USERNAME")
    p = os.getenv("FB_PASSWORD")
    if not u or not p:
        raise RuntimeError(
            "Missing Facebook credentials. Set FB_USERNAME and FB_PASSWORD in your .env or environment."
        )
    return u, p

def get_facebook_csd_creds():
    """Get Facebook CSD credentials"""
    u = os.getenv("FB_CSD")
    p = os.getenv("FB_CSD_PASSWORD")
    if not u or not p:
        raise RuntimeError(
            "Missing Facebook CSD credentials. Set FB_CSD and FB_CSD_PASSWORD in your .env or environment."
        )
    return u, p

def get_email_creds():
    """Get email credentials"""
    u = os.getenv("EMAIL_USERNAME")
    p = os.getenv("EMAIL_PASSWORD")
    if not u or not p:
        raise RuntimeError(
            "Missing Email credentials. Set EMAIL_USERNAME and EMAIL_PASSWORD in your .env or environment."
        )
    return u, p

def get_csd_creds():
    """Get CSD credentials for approvals"""
    u = os.getenv("EMAIL_CSD")
    p = os.getenv("EMAIL_CSD_PASSWORD")
    if not u or not p:
        raise RuntimeError(
            "Missing CSD credentials. Set EMAIL_CSD and EMAIL_CSD_PASSWORD in your .env or environment."
        )
    return u, p

def get_sa_creds():
    """Get SuperAdmin credentials"""
    u = os.getenv("SA_USERNAME")
    p = os.getenv("SA_PASSWORD")
    if not u or not p:
        # Debug: print what was loaded
        print(f"Debug: SA_USERNAME = {u}")
        print(f"Debug: SA_PASSWORD exists = {bool(p)}")
        print(f"Debug: .env path = {env_path}")
        print(f"Debug: .env exists = {env_path.exists()}")
        raise RuntimeError(
            "Missing SuperAdmin credentials. Set SA_USERNAME and SA_PASSWORD in your .env or environment."
        )
    return u, p


def get_youtube_creds():
    """Get youtube credentials"""
    u = os.getenv("YOUTUBE_USERNAME")
    p = os.getenv("YOUTUBE_PASSWORD")
    if not u or not p:
        raise RuntimeError(
            "Missing YouTube credentials. Set YOUTUBE_USERNAME and YOUTUBE_PASSWORD in your .env or environment."
        )
    return u, p


def get_linkedin_creds():
    """Get linkedin credentials"""
    u = os.getenv("LINKEDIN_USERNAME")
    p = os.getenv("LINKEDIN_PASSWORD")
    if not u or not p:
        raise RuntimeError(
            "Missing LinkedIn credentials. Set LINKEDIN_USERNAME and LINKEDIN_PASSWORD in your .env or environment."
        )
    return u, p