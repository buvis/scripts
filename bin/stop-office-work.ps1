git config --global http.proxy localhost:3129
[Environment]::SetEnvironmentVariable("http_proxy","http://localhost:3129","User")
[Environment]::SetEnvironmentVariable("https_proxy","http://localhost:3129","User")
