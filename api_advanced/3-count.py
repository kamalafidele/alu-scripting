#!/usr/bin/python3
"""
Module for recursively counting keywords in Reddit hot posts.

This module contains a recursive function to query Reddit API, collect all
hot post titles, and count occurrences of specified keywords with sorting.
"""

import requests


def count_words(subreddit, word_list, hot_list=None, after=None):
    """
    Recursively count keywords in all hot post titles from a subreddit.

    Args:
        subreddit (str): The name of the subreddit to query
        word_list (list): List of keywords to count (case-insensitive)
        hot_list (list): List to accumulate titles (default: None)
        after (str): Pagination token for next page (default: None)

    Returns:
        None: Prints sorted word counts or nothing if no matches/invalid
    """
    # Initialize hot_list on first call to avoid mutable default argument
    if hot_list is None:
        hot_list = []

    if not subreddit or not isinstance(subreddit, str) or not word_list:
        return

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)

    # Custom User-Agent to avoid Too Many Requests errors
    headers = {
        'User-Agent': 'python:subreddit.word.counter:v1.0 (by /u/bot)'
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
            return

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
                    return count_words(subreddit, word_list, hot_list,
                                       after_token)
                else:
                    # No more pages, process and print results
                    _process_and_print_counts(hot_list, word_list)
                    return

    except (requests.exceptions.RequestException, ValueError, KeyError):
        return


def _process_and_print_counts(titles, word_list):
    """
    Process titles and print sorted word counts.

    Args:
        titles (list): List of post titles
        word_list (list): List of keywords to count
    """
    # Convert word_list to lowercase and count duplicates
    word_counts = {}
    for word in word_list:
        word_lower = word.lower()
        word_counts[word_lower] = word_counts.get(word_lower, 0)

    # Count occurrences of each word in titles
    for title in titles:
        # Split title into words and convert to lowercase
        title_words = title.lower().split()
        
        for title_word in title_words:
            # Remove punctuation from the end and beginning
            cleaned_word = title_word.strip('.,!?;:"()[]{}')
            
            # Check if this cleaned word matches any of our target words
            for target_word in word_counts:
                if cleaned_word == target_word:
                    word_counts[target_word] += 1

    # Filter out words with zero counts
    filtered_counts = {word: count for word, count in word_counts.items()
                       if count > 0}

    # Sort by count (descending) then alphabetically (ascending)
    sorted_words = sorted(filtered_counts.items(),
                          key=lambda x: (-x[1], x[0]))

    # Print results
    for word, count in sorted_words:
        print("{}: {}".format(word, count))
