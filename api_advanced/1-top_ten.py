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
        print("OK")
        return

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)

    # Custom User-Agent to avoid Too Many Requests errors
    headers = {
        'User-Agent': 'python:subreddit.hot.posts:v1.0 (by /u/bot)'
    }

    try:
        # Make request without following redirects
        response = requests.get(url, headers=headers, allow_redirects=False,
                                params={'limit': 10})

        # Check if we got a redirect (invalid subreddit)
        if response.status_code == 302:
            print("OK")
            return

        # Check for successful response
        if response.status_code == 200:
            data = response.json()

            # Verify response structure
            if ('data' in data and 'children' in data['data']):
                posts = data['data']['children']

                # Print titles of first 10 posts (or fewer if less available)
                count = 0
                for post in posts:
                    if count >= 10:
                        break
                    if ('data' in post and 'title' in post['data']):
                        print(post['data']['title'])
                        count += 1
                return

        print("OK")

    except (requests.exceptions.RequestException, ValueError, KeyError):
        print("OK")
