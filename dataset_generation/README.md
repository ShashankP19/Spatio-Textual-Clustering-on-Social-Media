## Getting Twitter Data
Twitter API provides tweets of last 7 days which can be searched for the needed keywords


### Dependencies
- [tweepy](http://docs.tweepy.org/en/v3.4.0/install.html): `sudo pip3 install tweepy`
- pandas 

### Generate keys

    1. Create a twitter account and register for a developer account.
    2. Go to [https://apps.twitter.com/](https://apps.twitter.com/) and log in with your twitter credentials.
    3. Click "Create New App"
    4. Fill out the form, agree to the terms, and click "Create your Twitter application"
    5. In the next page, click on "API keys" tab, and copy your "API key" and "API secret".
    6. Scroll down and click "Create my access token", and copy your "Access token" and "Access token secret"
    7. Copy `twitter_config_template.py` contents to `twitter_config.py` and add the keys there

### Running code

    `python getdata.py <Space separated keywords to search for>`
    > e.g.: `python3 getdata.py 'Oxford Univ' 'oxford univ' oxford`

### References

- http://adilmoujahid.com/posts/2014/07/twitter-analytics/ 
- https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object
- https://www.programcreek.com/python/example/76301/tweepy.Cursor
