#!/usr/bin/python3
"""
Module for recursively querying Reddit API to get all hot posts from a subreddit.

This module contains a recursive function to retrieve the titles of all
hot posts for a given subreddit using Reddit's public API with pagination.
"""

import requests


def recurse(subreddit, hot_list=None, after=None):
    """
    Recursively query Reddit API and return list of all hot post titles.

    Args:
        subreddit (str): The name of the subreddit to query
        hot_list (list): List to accumulate titles (default: None)
        after (str): Pagination token for next page (default: None)

    Returns:
        list: List of all hot post titles, or None if subreddit is invalid
    """
    # Initialize hot_list on first call to avoid mutable default argument
    if hot_list is None:
        hot_list = []

    if not subreddit or not isinstance(subreddit, str):
        return None

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)

    # Custom User-Agent to avoid Too Many Requests errors
    headers = {
        'User-Agent': 'python:subreddit.hot.recurse:v1.0 (by /u/bot)'
    }

    # Set up parameters for pagination
    params = {}
    if after:
        params['after'] = after

    try:
        # Make request without following redirects
        response = requests.get(url, headers=headers, allow_redirects=False,
                                params=params)

        # Check if we got a redirect (invalid subreddit)
        if response.status_code == 302:
            return None

        # Check for successful response
        if response.status_code == 200:
            data = response.json()

            # Verify response structure
            if ('data' in data and 'children' in data['data']):
                posts = data['data']['children']

                # Extract titles from current page
                for post in posts:
                    if ('data' in post and 'title' in post['data']):
                        hot_list.append(post['data']['title'])

                # Check if there's a next page
                after_token = data['data'].get('after')
                if after_token:
                    # Recursively get next page
                    return recurse(subreddit, hot_list, after_token)
                else:
                    # No more pages, return accumulated list
                    return hot_list

        return None

    except (requests.exceptions.RequestException, ValueError, KeyError):
        return None
