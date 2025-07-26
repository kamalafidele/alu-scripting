#!/usr/bin/python3
"""
Module for querying Reddit API to get top 10 hot posts from a subreddit.

This module contains a function to retrieve and print the titles of the
first 10 hot posts for a given subreddit using Reddit's public API.
"""

import requests


def top_ten(subreddit):
    """
    Query Reddit API and print titles of first 10 hot posts for a subreddit.

    Args:
        subreddit (str): The name of the subreddit to query

    Returns:
        None: Prints titles or None if subreddit is invalid
    """
    if not subreddit or not isinstance(subreddit, str):
        print(None)
        return

    url = f"https://www.reddit.com/r/{subreddit}/hot.json"

    # Custom User-Agent to avoid Too Many Requests errors
    headers = {
        'User-Agent': 'python:subreddit.hot.posts:v1.0 (by /u/bot)'
    }

    try:
        # Make request without following redirects
        response = requests.get(url, headers=headers, allow_redirects=False,
                                params={'limit': 10})

        # Check for invalid subreddit (404 or other error codes)
        if response.status_code != 200:
            print(None)
            return

        # Parse JSON response
        data = response.json()

        # Verify response structure
        posts = data.get('data', {}).get('children', [])
        if not posts:
            print(None)
            return

        # Print titles of first 10 posts
        for post in posts:
            title = post.get('data', {}).get('title')
            if title:
                print(title)

    except requests.exceptions.RequestException:
        print(None)
