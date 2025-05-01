import praw
import json
import re

gender_regex = r'\b(?:\d+[FfMm]|male|female|husband|wife|boyfriend|girlfriend)\b'
female_regex = r'\b(?:\d+[Ff]|female|husband|boyfriend)\b'

#with open("files\\ids.json","w") as f:
    #json.dump([], f)

def authenticate(id='default'):
    reddit = praw.Reddit(id)

    reddit.user.me()
    reddit.read_only = True
    return reddit

def get_post_from_subreddit(reddit=praw.Reddit, subreddit="AmItheAsshole", limit=25):
    with open("files\\ids.json","r") as f:
        id_list = json.load(f)

    for submission in reddit.subreddit(subreddit).top(limit=limit):
        id = submission.id
        title = submission.title
        content = submission.selftext
        url = submission.url
        author = submission.author

        if submission.over_18: continue

        gender_codes = re.findall(gender_regex, content, re.IGNORECASE) 

        if len(gender_codes) != 0:
            if re.match(female_regex, gender_codes[0], re.IGNORECASE):
                gender = 'female'
            else:
                gender = 'male'
        else:
            gender = 'male'


        if id not in id_list:
            id_list.append(id)
            with open("files\\ids.json","w") as f:
                json.dump(id_list, f)

            return id, title, content, gender, url, author
    
    return '', '', '', '', '', ''

def get_post_from_id(reddit=praw.Reddit, id='1k84kn7'):
    submission = reddit.submission(id)
    id = submission.id
    title = submission.title
    content = submission.selftext
    url = submission.url

    gender_codes = re.findall(gender_regex, content, re.IGNORECASE) 

    if len(gender_codes) != 0:
        if re.match(female_regex, gender_codes[0], re.IGNORECASE):
            gender = 'female'
        else:
            gender = 'male'
    else:
        gender = 'male'
    
    return id, title, content, gender, url

    