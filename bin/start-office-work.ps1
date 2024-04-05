git config --global --unset http.proxy
[Environment]::SetEnvironmentVariable("http_proxy", "", "User")
[Environment]::SetEnvironmentVariable("https_proxy", "", "User")
