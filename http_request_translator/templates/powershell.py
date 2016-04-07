code_begin = """
$session = New-Object Microsoft.PowerShell.Commands.WebRequestSession
$cookie = New-Object System.Net.Cookie
"""

code_cookie = """
$cookie.Name = "{name}";
$cookie.Value = "{value}";
$cookie.Domain = "{domain}";
$session.Cookies.Add($cookie);
"""

code_invoke_begin = "$r = Invoke-WebRequest -WebSession $session "

code_dic = """ "{header}"="{value}"; """

code_header ="-Method {method} -Uri {url} -Headers {headers}"

code_proxy = """ -Proxy {proxy}"""

code_post = """ -Body {data} """

code_search = """ | grep "{search_string}" """

code_nosearch = """  """
