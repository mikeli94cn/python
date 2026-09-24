This error happens when uv tries to download packages via an HTTPS connection, but a corporate proxy, VPN, firewall, or a custom PyPI mirror blocks or changes the network payload.

The InvalidContentType message means uv was expecting a standard Python package stream, but the network connection handed back an unexpected layout—usually a plain text/HTML block containing an error page like a proxy login wall or a connection reset notice.
## Solution 1: Pass Your System Proxy to uv
If you are behind a company network or a VPN, uv needs to be told exactly how to route through your proxy. 

Open your terminal and set your proxy environment variables before running your command:

On Windows (Command Prompt):
```
set HTTP_PROXY=http://your-proxy-address:port
set HTTPS_PROXY=http://your-proxy-address:port
```
On Windows (PowerShell):
```
$env:HTTP_PROXY="http://your-proxy-address:port"
$env:HTTPS_PROXY="http://your-proxy-address:port"
```
On macOS / Linux:
```
export HTTP_PROXY="http://your-proxy-address:port"
export HTTPS_PROXY="http://your-proxy-address:port"
```
(Replace your-proxy-address:port with your actual corporate proxy address, such as http://company.com).
## Solution 2: Explicitly Trust TLS Certificates
If your network intercepts connections (SSL decryption), uv will reject the download for safety reasons. 

You can instruct uv to look at your system certificates or temporarily disable strict verification to test if it bypasses the issue:

Run your command with the --insecure flag to test if certificates are the core culprit:
```
uv pip install -r requirements.txt --insecure
```
Note: If --insecure works, it confirms a network interception issue. 

For a long-term secure fix instead of using --insecure, point uv to your company's network security certificate file using export UV_CERT_FILE=/path/to/cert.pem.
## Solution 3: Use an Alternative Mirror (If the official PyPI is blocked)
If your region or company network blocks access to the official pypi.org host entirely, pass a mirror index directly using the --index-url flag.

For instance, you can try routing through a reliable public mirror like Cloudflare or a local equivalent:
```
uv pip install -r requirements.txt --index-url https://cloudflare-pypi.org
```
## Solution 4: Clean the uv Network Cache
Sometimes a corrupted or broken half-download gets stuck in uv's internal storage cache, forcing it to throw an invalid content error continuously. Clear it explicitly by running:
```
uv cache clean
```
After clearing it, try running your original uv pip install -r requirements.txt command again.

Are you running this script inside a corporate network/office VPN, or are you on a standard home connection? If you continue to see errors, sharing your geographical region or if you use any private artifactory / mirror servers can help isolate the correct network path.

# uv set mirror
To configure uv to download packages from a mirror instead of the default PyPI, you can set a default custom index.

Depending on your preference, you can do this either via your project's configuration file or globally using environment variables:
## Option 1: Using pyproject.toml or uv.toml (Recommended)
Add the following snippet to your project's pyproject.toml or global uv.toml file: [1] 
```
[[tool.uv.index]]
url = "https://your-mirror-url.com"
default = true
```
Setting default = true tells uv to use this mirror as the primary package index instead of PyPI. [1] 
## Option 2: Using Environment Variables
Alternatively, you can set the UV_INDEX_URL environment variable in your terminal before running uv add:
```
export UV_INDEX_URL="https://your-mirror-url.com"
uv add <package-name>
```

## Mirroring Python Downloads (Optional)
If your network also blocks or slows down downloading Python toolchains themselves, you can mirror those as well by adding this to your pyproject.toml: [1] 
```
[tool.uv]
python-install-mirror = "https://your-mirror-url.com"
```
Are you using a specific public mirror (like Tsinghua/TUNA) or an internal enterprise proxy (like Artifactory/Nexus)? I can give you the exact URL structure if needed.


# uv set global configuration
To set a global uv.toml file, you need to create it manually in your operating system's specific user-level configuration directory. [1] 
## 1. Where to Put the File
Place the uv.toml file in one of the following directory paths based on your system: [2, 3] 

* macOS / Linux:
~/.config/uv/uv.toml
* Windows:
%APPDATA%\uv\uv.toml (This resolves to a path like C:\Users\<YourUsername>\AppData\Roaming\uv\uv.toml) [1] 


If the uv folder or the uv.toml file does not exist yet, you can safely create them yourself. [1] 

## 2. How to Format the Mirror Config Globally
When configuring a global mirror inside a user-level uv.toml, the TOML structure changes slightly from a project's pyproject.toml. You drop the tool.uv. prefix: [3] 
```
[[index]]
url = "https://your-mirror-url.com"
default = true
```
## Quick Setup Commands
You can instantly create the file and add your mirror by running one of these terminal snippets:
On macOS / Linux:
```
mkdir -p ~/.config/uv
cat <<EOF > ~/.config/uv/uv.toml
[[index]]
url = "https://your-mirror-url.com"
default = true
EOF
```
On Windows (PowerShell):
```
New-Item -ItemType Directory -Force -Path "\$env:APPDATA\uv"
Set-Content -Path "\$env:APPDATA\uv\uv.toml" -Value '[[index]]`nurl = "https://your-mirror-url.com"`ndefault = true'
```
Are you setting this up for a restricted enterprise network, or are you just trying to speed up downloads using a public regional mirror? I can give you the exact URL string or look up standard mirror options if needed.

# uv set trusted certificates
The invalid peer certificate: UnknownIssuer error happens because uv uses its own built-in certificate bundle by default. If you are behind a corporate network proxy, firewall, or a company VPN that decrypts and re-encrypts HTTPS traffic (like Zscaler or Fortinet), uv won't trust the custom network certificate. [1, 2, 3] 
You can resolve this issue by trying the following solutions:
## Solution 1: Tell uv to use your System Certificates (Most Common)
You can force uv to read the trusted certificates already installed on your operating system (like your macOS Keychain or Windows Certificate Manager). [3] 
Add it to your global uv.toml:
Open your global uv.toml file and add the native-tls = true flag at the root level: [4] 

native-tls = true

[[index]]
url = "https://your-mirror-url.com"
default = true

Alternatively, use an Environment Variable:
If you want to quickly test it in your terminal, run this before your uv commands: [3] 

* 
* macOS / Linux: export UV_NATIVE_TLS=true
* Windows (PowerShell): $env:UV_NATIVE_TLS="true" [3] 
* 


## Solution 2: Explicitly trust the Mirror Host
If your mirror itself is using a self-signed or internal enterprise SSL certificate, you can bypass the check strictly for that domain using the allow-insecure-host setting. [5] 
Add it to your global uv.toml:
```
allow-insecure-host = ["your-mirror-url.com"]

[[index]]
url = "https://your-mirror-url.com"
default = true

(Make sure to use only the root domain name—like mirrors.tools.huawei.com or nexus.company.local—without https:// or /simple/ inside the allow-insecure-host brackets). [5] 

## Solution 3: Point uv to a specific Root Certificate (For Corporate Proxies)
If your company provides a specific corporate root certificate file (usually a .pem or .crt file), you can map uv directly to it. [6, 7] 
Set the standard SSL environment variable in your terminal session before running uv: [8] 


* macOS / Linux: export SSL_CERT_FILE="/path/to/your/corporate-cert.pem"
* Windows (PowerShell): $env:SSL_CERT_FILE="C:\path\to\your\corporate-cert.pem" [7] 
  

If the error persists after trying Solution 1, let me know:


* What operating system you are on (Windows, macOS, or Linux)?
* Are you working on a corporate/company laptop that uses a VPN or firewall?
  
