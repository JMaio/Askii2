import py_wolfram.wap as wap

outerTypo = ""


def parse(e):
    # on okay request
    print e
    if e[2][1] == "true":
        return e[17][8][3][1]
    else:
        global outerTypo
        try:
            typo = e[-1][-1][-1]
        except IndexError:
            return "Sorry, I am unable to answer this..."
        typo = e[-1][-1][-1]
        outerTypo = str(typo)
        return "Did you mean " + outerTypo + "? " + respond(typo)


def query_wolfram(q):
    server = 'http://api.wolframalpha.com/v2/query.jsp'
    appid = 'WHXQR4-E2PWVYTVA7'

    waeo = wap.WolframAlphaEngine(appid, server)
    query = waeo.CreateQuery(q + "&format=plaintext&output=JSON")
    result = waeo.PerformQuery(query)
    waeqr = wap.WolframAlphaQueryResult(result)
    jsonresult = waeqr.JsonResult()

    return jsonresult


def respond(req):
    response = str(parse(eval(query_wolfram(req))))[0:1599]
    # response = response.encode('utf-8')
    r_typo = str(''.join([str(response)]))[0:1599]
    if len(outerTypo) == 0:
        return response
    else:
        return r_typo