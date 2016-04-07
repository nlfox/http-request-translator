"""

:synopsis: Define the specialize script classes that will generate the script code.

"""

from .base import AbstractScript


class BashScript(AbstractScript):
    """Extended `AbstractScript` class for Bash script code generation.
    Fills code variables for the request from `bash_template`.
    Overrides `_generate_request` method to generate bash specific code.
    """

    __language__ = 'bash'

    def _generate_request(self):
        code = self.code_nosearch.format(
            method=self.details.get('method', ''),
            url=self.url,
            headers=self._generate_headers())
        if self.search:
            code += self.code_search.format(search_string=self.search.replace('"', '\\"'))
        return code


class PowerShellScript(AbstractScript):
    """Extended `AbstractScript` class for PowerShell script code generation.
    Fills code variables for the request from `powershell_template`.
    """

    remove_headers = ['Connection', 'Content-Length']
    __language__ = 'powershell'

    def _generate_ps_header_dic(self):
        """Generation of powershell dics.
        :return: strings of powershell dics.
        :rtype: str
        """
        code = '@{'
        for item in self.headers:
            header, value = item.split(':', 1)
            if header == 'User-Agent':
                self.user_agent = value
                continue
            if header == 'Cookie':
                self.cookie = value
                continue
            if header == 'Host':
                self.domain = value
                continue

            if header in self.remove_headers:
                continue
            code += self.code_dic.format(header=header.replace('"', '\\"'), value=value.replace('"', '\\"'))

        code += '}'
        return code

    def _generate_begin(self):
        """Default generation of the beginning of the code.

        :return: Beginning of the code.
        :rtype: str
        """
        self.cookie = None
        self.ps_headers = self._generate_ps_header_dic()
        code = self.code_begin
        if self.cookie:
            code += self._generate_ps_cookie(self.cookie) + self.code_invoke_begin
        else:
            code += self.code_invoke_begin

        code += self.code_header.format(
            method=self.details.get('method', ''),
            url=self.url,
            headers=self.ps_headers)
        if self.user_agent:
            code += "-UserAgent '{user_agent}'".format(user_agent=self.user_agent)
        return code

    def _generate_ps_cookie(self, cookieStr):
        """special generation of powershell cookie format
        :return: cookies in powershell format
        :rtype: str
        """
        import Cookie
        C = Cookie.SimpleCookie()
        C.load(cookieStr)  # load from a string (HTTP header)
        res = ''
        for k, v in C.items():
            if v['domain'] == '' and self.domain:
                res += self.code_cookie.format(name=k, value=v.value, domain=self.domain.strip())
            else:
                res += self.code_cookie.format(name=k, value=v.value, domain=v['domain'])
        return res

    def _generate_post(self):
        """override _generate_post
        :return: post parameter in powershell format
        :rtype: str
        """
        import urllib
        code = "@{"
        data = self.details.get('data', '')
        dataArr = data.split('&')
        for i in dataArr:
            key, value = i.split('=')

            code += self.code_dic.format(header=urllib.unquote(key), value=urllib.unquote(value))
        code += '}'
        return self.code_post.format(data=code)

    def _generate_request(self):
        code = "\n$r.Content"
        if self.search:
            code += self.code_search.format(search_string=self.search.replace('"', '\\"'))
        return code


class PHPScript(AbstractScript):
    """Extended `AbstractScript` class for PHP script code generation.
    Fills code variables for the request from `php_template`.
    Overrides `_generate_begin` method to generate php specific code.
    """

    __language__ = 'php'

    def _generate_begin(self):
        return self.code_begin.format(url=self.url) + self._generate_headers()


class PythonScript(AbstractScript):
    """Extended `AbstractScript` class for Python script code generation.
    Fills code variables for the request from `python_template`.
    Overrides `_generate_begin` method to generate python specific code.
    """

    __language__ = 'python'

    def _generate_begin(self):
        return self.code_begin.format(url=self.url, headers=str(self.headers))


class RubyScript(AbstractScript):
    """Extended `AbstractScript` class for Ruby script code generation.
    Fills code variables for the request from `ruby_template`.
    Overrides `_generate_begin` method to generate Ruby specific code.
    """

    __language__ = 'ruby'

    def _generate_begin(self):
        code = self.code_begin.format(url=self.url, method=self.details.get('method', '').strip().lower())
        code += self.code_headers.format(headers=self._generate_headers())
        return code
