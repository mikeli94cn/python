The pip config set global.trusted-host command lets you permanently mark specific package repositories or domains as trusted. This bypasses SSL certificate verification errors, which is useful if you are behind a corporate firewall, using a proxy, or accessing a private network mirror. [1, 2, 3, 4] 
Here is how to view, set, or modify your trusted hosts using the pip config CLI:
## 1. Set a Single Trusted Host
To configure a single trusted host, run:

pip config set global.trusted-host pypi.org

## 2. Set Multiple Trusted Hosts
If you need to trust multiple domains (like standard PyPI and your corporate artifact repository), separate them with a space inside a single set command: [1, 5] 

pip config set global.trusted-host "pypi.org files.pythonhosted.org artifactory.mycompany.com"

(Note: Wrapping them in quotes ensures the terminal passes the hosts as a single string argument). [6] 
## 3. Check Current Configurations
To see where your configuration files are located and what hosts are currently trusted, use: [1, 6] 

pip config list

Or to see exactly which files are being read:

pip config -v list

------------------------------
## Alternative: One-Time Bypass
If you do not want to change your permanent configuration, you can append the --trusted-host flag directly to your install command instead: [7] 

pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org <package_name>

Are you trying to resolve a specific SSL certificate verification error, or are you setting up connection to a private corporate repository? Let me know so I can help you format the exact URLs or configuration block you need.
