import RedditInterface
import WolframInterface


def parseSMS(body, phoneno):
    identifier = body[:3]
    if body[:-1] == '|':
        if body[:2] == 're':
            return formatReddit(body[3:], phoneno)
        elif body[:2] == 'wa':
            return WolframInterface.respond(body[3:])
        else:
            return ("Invalid identifier, please use 'wa|<query>' for a wolfram query or " +
                    "'re|<url>' for a reddit comment thread or subreddit list of posts")
    else:
        return WolframInterface.respond(body)


def formatReddit(body, phone_no):
    parts = body.split()
    if len(parts) < 1:
        return "You have not specified a url to navigate to"
    elif len(parts) == 1:
        return RedditInterface.respond(parts[0], phone_no, 0)
    elif len(parts) == 2:
        return RedditInterface.respond(parts[0], phone_no, parts[1])
    else:
        return "Invalid formatting of reddit request, please format 're|<url> [<direction - integer>]"