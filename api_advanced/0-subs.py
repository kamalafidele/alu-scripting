#!/usr/bin/python3
"""
Module for querying Reddit API to get subreddit subscriber counts.

This module contains a function to retrieve the number of subscribers
for a given subreddit using Reddit's public API.
"""

import requests


def number_of_subscribers(subreddit):
    """
    Query Reddit API and return the number of subscribers for a subreddit.
    
    Args:
        subreddit (str): The name of the subreddit to query
        
    Returns:
        int: Number of subscribers, or 0 if subreddit is invalid
    """
    if not subreddit or not isinstance(subreddit, str):
        return 0
    
    url = "https://www.reddit.com/r/{}/about.json".format(subreddit)
    
    # Custom User-Agent to avoid Too Many Requests errors
    headers = {
        'User-Agent': 'python:subreddit.subscriber.counter:v1.0 (by /u/pythonbot)'
    }
    
    try:
        # Make request without following redirects
        response = requests.get(url, headers=headers, allow_redirects=False)
        
        # Check if we got a redirect (invalid subreddit)
        if response.status_code == 302:
            return 0
            
        # Check for successful response
        if response.status_code == 200:
            data = response.json()
            
            # Verify the response structure and extract subscribers
            if 'data' in data and 'subscribers' in data['data']:
                return data['data']['subscribers']
        
        return 0
        
    except (requests.exceptions.RequestException, ValueError, KeyError):
        return 0
