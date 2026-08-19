import urllib.request
import http.cookiejar
import time

cookie_str = "_gcl_au=1.1.2048537226.1787167604; HSID=AnzF0aFhnanYtMgzZ; SSID=A9akFYtkqvyI9EtL-; APISID=WNXD7sKPPlsKSB_b/APEM7Cwylba4E4sjN; SAPISID=dJZfnr1svEcaijcg/AjdqSD26x27EtOK1U; __Secure-1PAPISID=dJZfnr1svEcaijcg/AjdqSD26x27EtOK1U; __Secure-3PAPISID=dJZfnr1svEcaijcg/AjdqSD26x27EtOK1U; SID=g.a000BgmdQn-V9o4uTngXqAIiwRsWxWyoh14jpA5BExk8kKnuryQUOWRjdDdpr0BvoKUwbU_9KAACgYKAXESARASFQHGX2Mie13uboRiuYrDaJsJq2QajhoVAUF8yKrmDlsjbHFaniByXiauOQi80076; __Secure-1PSID=g.a000BgmdQn-V9o4uTngXqAIiwRsWxWyoh14jpA5BExk8kKnuryQU82tAxKdBORCKfrz55q5oLQACgYKATMSARASFQHGX2MiCKF95KYjqUNZdpX36zVtDxoVAUF8yKp6kUynKRqMcgo0q-Pg7Sfj0076; __Secure-3PSID=g.a000BgmdQn-V9o4uTngXqAIiwRsWxWyoh14jpA5BExk8kKnuryQU9tmm4uXf3Fd6II_vcFRwfgACgYKAdASARASFQHGX2MiJkuYFPgxh0lND_u2d6dX7hoVAUF8yKqlOl1MURcw7irfdAhgLWsg0076; __Secure-1PSIDTS=sidts-CjQBXMw41WbistVeWbReSaaYBm-5OgJQE-H5d3-JCoqranKeoCTnY9NLOCPn79s50_f5gkJFEAA; __Secure-3PSIDTS=sidts-CjQBXMw41WbistVeWbReSaaYBm-5OgJQE-H5d3-JCoqranKeoCTnY9NLOCPn79s50_f5gkJFEAA; LOGIN_INFO=AFmmF2swRAIgBzgVwl_tBr20A5WS9mn4oWOP1FRqCpaVvw4E_abK1BkCICmUc3ywznSVaDLUKfoQSLLXjO2Zv_zorzsu0QZz7-Qb:QUQ3MjNmeTU0QTNJaDJXb1VaNmxTOFlfUjlhWk9zd3JHU1pwcFFGbFB0MFE3dkxMZTd5NDB3al9lbHBCc3o2Y1dOTW1oWGRqYzYtRzlzREw4b3ZXLVJzQ29NTklPbzhFQVEzWklJSEdJbVNvbHRLRVpPWnRoZVZjUVlNZFF4eG9zbC1UVGxnVFRlb0ctQ3ZSNXRrNTVqYjM4eG4yek9VSWxB; SIDCC=AKEyXzXL09wRycQnEphUPbc8DG5d8oeKEMu2RzkVPYXgcbk6HMzMH1mzbwtpvxT-qnXq6wh9; __Secure-1PSIDCC=AKEyXzUkSN5CncXroj7z5K1AXYXDQz0eV1BXDfB40wzBAqjx4w2S4PBWD_hqpN1uXVfgXAYJ; __Secure-3PSIDCC=AKEyXzXa-ZGVg-TpRXIX4q1SYcyP7Fz90Es_DppuFVBhPT2WNiRhRrbTTqX6--oRn-CqigDR"

jar = http.cookiejar.MozillaCookieJar('cookies.txt')
for item in cookie_str.split('; '):
    name, value = item.split('=', 1)
    c = http.cookiejar.Cookie(
        version=0, name=name, value=value,
        port=None, port_specified=False,
        domain='.youtube.com', domain_specified=True, domain_initial_dot=True,
        path='/', path_specified=True,
        secure=True, expires=int(time.time() + 31536000),
        discard=False, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False
    )
    jar.set_cookie(c)
jar.save(ignore_discard=True, ignore_expires=True)
