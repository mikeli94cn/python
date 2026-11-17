PYTHON_HOME SETTING
The PYTHONHOME environment variable tells the Python interpreter where to locate its standard libraries. In most standard installations, you do not need to set this variable manually because Python automatically finds its libraries relative to its executable. [1] (/goto?url=CAESbQHEIkXX1JjAs63ppi0u2gzXdQ5hs5lc6KoLE1Vs6kh_2rGPQIYrIaVdr4ToZDiKTGRQoc71dRnxkP2XfrQ9VVrxkHlQg4zg05DVfRLpgmaJY92APsNjDjAhmNyZ3P6uJeL3GZpvB1zNbfE8TdQ), [2] (/goto?url=CAESkwEBxCJF10KqdgjnO4-Pc0oe8mxdBD49WI-hmu2eOhz9pFwPyCLso8HfvHiTvr7q5BKbSqro0ZiObplOOpTHoYPEAaRS5C2d4Y8Pbwjt1X-1OLxOvfpSi7lMb3pc45lpaX3BNAug-1UFlaGh-Mhj_ZXamQn92riAcFxhSVTcV6PBNVZD5VsfmMWleSfakuag-i9X8Ts)

How PYTHONHOME Works

• Single path format. You can point PYTHONHOME to a single root directory where Python is installed. Python will look for both platform-independent libraries (prefix) and platform-specific binaries (exec_prefix) inside that folder. [1] (/goto?url=CAESjQEBxCJF11bIJ7PoMke1uwK2AhMs0hnxJS_C2jXnzaTHqnVR3PGf38O9DLuGB5LnkFpOa6KgpJPb_enuU_K9DS_49i5SpBJ4NvzYA5ffOnP8kAT4ZLNbfc1_s3YrmrG3wmuG5U1IW65lg-b-H9avi4iB_QYns7Ns19EuYPZv7rwwdi4d_48zzpFxOOK13wI), [2] (/goto?url=CAESbQHEIkXX1JjAs63ppi0u2gzXdQ5hs5lc6KoLE1Vs6kh_2rGPQIYrIaVdr4ToZDiKTGRQoc71dRnxkP2XfrQ9VVrxkHlQg4zg05DVfRLpgmaJY92APsNjDjAhmNyZ3P6uJeL3GZpvB1zNbfE8TdQ)
• Dual path format. If your standard libraries and compiled extension modules live in separate locations, set PYTHONHOME using the format prefix:exec_prefix on macOS/Linux or prefix;exec_prefix on Windows. [1] (/goto?url=CAESiQEBxCJF1zdL130WN9lFzTfNgCvkGpgyJU2kmvvKn_x9Bwro27i6mLu0WuEtoB8c_BGwE0Ff1Hnl1UpMajB3xJZiSH7Zh8qc0nJYslwJJe1PfgTNt2jPhO8bu7UFvC-BV6NT1DmE27tUTIM5r102K2MB8JWsWEO_7nfDIWJnJo6oXLdC44-zeNPJBQ), [2] (/goto?url=CAESjQEBxCJF11bIJ7PoMke1uwK2AhMs0hnxJS_C2jXnzaTHqnVR3PGf38O9DLuGB5LnkFpOa6KgpJPb_enuU_K9DS_49i5SpBJ4NvzYA5ffOnP8kAT4ZLNbfc1_s3YrmrG3wmuG5U1IW65lg-b-H9avi4iB_QYns7Ns19EuYPZv7rwwdi4d_48zzpFxOOK13wI)
• When to avoid setting it. Setting PYTHONHOME globally often breaks virtual environments (venv or conda) and multiple Python versions by forcing them to load the wrong standard library.

How to Set PYTHONHOME by Operating System


Windows

1. Open Environment Variables. Press the Windows key, type Edit the system environment variables, and open the control panel.
2. Access the menu. Click the Environment Variables button near the bottom of the window.
3. Create the variable. Under User variables or System variables, click New.
4. Enter the details. Set the Variable name to PYTHONHOME and the Variable value to your Python root folder (for example, C:\Users\YourName\AppData\Local\Programs\Python\Python312).
5. Save and restart. Click OK on all windows and restart your terminal or IDE to apply the change. [1] (/goto?url=CAESaAHEIkXXRUcj6boBb1LNEDhIlWif3km9oVPErRVKq4ykJc_KJmox4s2yMElDtW1LmTq5sEzO6sbsMcqLxunlPMg1E_fca3E6XRwsvkLCJbZgdi_h_m3DbXTo_HaLWOhvcf5uzkUh_hox), [2] (/goto?url=CAESaAHEIkXXMGo2c-IgWFR3ttIU1Zt580OrbomH8tDsk7EiQcrSq5DGiehmX59vgIxH5lbIDxdzy37vk47OHamLS0m64NM2yP5MgxhrGS2GtQ9l6c6By9TYGtBNXehdex3plrXBU50Fm2y7), [3] (/goto?url=CAESbQHEIkXXLrtsgnlt0DkhMB505MB-Qxxw9NN3N0ITbycrtH7RNyJ92aaIbTPdNX5EDciYH75NHAcH-5h9Lf4ucV0nJSPr00Rb4ZZrQ-9Q_vgl_I8lkpawTntu3x2IARD1cFlyxSdQYDeJMRu7nSo)
To set it temporarily in a single terminal session:
• Command Prompt: set PYTHONHOME=C:\Path\To\Python
• PowerShell: $env:PYTHONHOME="C:\Path\To\Python"

macOS and Linux

1. Find your Python prefix. Run python3 -c "import sys; print(sys.prefix)" in your terminal to get the exact installation path.
2. Set it temporarily. Run export PYTHONHOME="/path/to/python" in your current terminal session.
3. Set it permanently. Add that exact export PYTHONHOME=... line to your shell configuration file (~/.zshrc on modern macOS, or ~/.bashrc on most Linux distributions), then run source ~/.zshrc (or ~/.bashrc). [1] (/goto?url=CAESfgHEIkXXJLUn4JsLTcUv47M-5KxJOtZikZeBAHdnKWtvMQZ4nf5WpeAuioTpFwkIUAWtpTQEiPF8W86eEzvo4yMl_VlKEmND_nfFfAJQkekVoxZFrtUbiptTjjKiE9zod93q4LaiQjYIMh1Qo2H_1T-Jzno0y-N4Dd6TWbJCXg), [2] (/goto?url=CAESjQEBxCJF11bIJ7PoMke1uwK2AhMs0hnxJS_C2jXnzaTHqnVR3PGf38O9DLuGB5LnkFpOa6KgpJPb_enuU_K9DS_49i5SpBJ4NvzYA5ffOnP8kAT4ZLNbfc1_s3YrmrG3wmuG5U1IW65lg-b-H9avi4iB_QYns7Ns19EuYPZv7rwwdi4d_48zzpFxOOK13wI)

Common Confusion: PYTHONHOME vs. PYTHONPATH

Developers frequently confuse these two variables when troubleshooting import errors or terminal issues.

Variable	Purpose	Typical Value Example
PYTHONHOME	Points to the core Python installation and built-in standard library.	/usr/local/python3 or C:\Python312
PYTHONPATH	Adds extra directories where Python looks for your custom modules and third-party packages.	/Users/name/my_project/src

If you are trying to run python from any folder in your terminal, you should add the Python folder to your system PATH variable rather than setting PYTHONHOME. If you are trying to fix a ModuleNotFoundError for your own scripts, use PYTHONPATH instead. [1] (/goto?url=CAESbgHEIkXXcyXyodfSpWmqumO4cXjGR7e8-JuBEb_35SVzlWiP6oa_aSwJMOaaZU-rmhg2pTDUnEmt0XjiUQdVGFo604sFM2nnqDPDLoffacYooOwthjpUTIb_NAfRgO4HR6xR977bonnoj9A3F_ZD)
If you are configuring this to fix a specific issue, let me know:
• Your operating system (Windows, macOS, or Linux)
• Whether you are seeing a specific error message (such as encodings not found or a ModuleNotFoundError)
I can help you verify the exact path or troubleshoot your environment setup.


---

Fatal Python error: initfsencoding: unable to load the file system codec ModuleNotFoundError: No module named 'encodings'

This error means Python cannot locate its standard library directory during startup, usually because PYTHONHOME or PYTHONPATH environment variables point to a wrong or outdated Python folder, or your virtual environment is broken. Unlike standard module errors, encodings is a core built-in library that cannot be fixed with pip install. [1] (/goto?url=CAESuAEBxCJF11d7hwLl7GPv8mGlip1ojq7so9pYhgrhKSBM1y9FTj0uilUjAfVh6igfvDL1RWfbTHZkNfA9NFTMfQHY07MMm9ei7zvkN8Qw9uvleFqe-5pFqr8rezXDJ14Wd5O5SKSkRmPiF0Ys-BA__AOl5salItd2-dx5_UaJYiWOQmcPDvzJzm72HWKpapGkg0iYO-R2uaFAjUsunbAc1usR9gU8lkAN6wsGHr0GlkuSsT3YXeqByfAj), [2] (/goto?url=CAESjQEBxCJF13jjwMUkLmSuKSFvn9y2eBX-4p_4Udu3DeNohOVX3IBgbc_Tjt8Zi33HYxfBusyYZBTWiuku7bUtLtdo2mumB65CMP8dOc4a2H8vy3SClvc0_H7gbmNCAmNsiSC08i44gLKOWOM9JsLnnUkNQvoGG8ZDCE6MpjdWzaFwA4yO9Qrl7_2w3ue6AHI), [3] (/goto?url=CAESXwHEIkXXw_4FKJG43BYB7YLkJ8nf1jpkDWpfGGruaxFPMitbPWYmZ4EHbPxYswQCvKwwB9nIXJxFElJi2Rf6v6H3C_QxYL-YiHKT70Sgs0-0jrCwfaI_oqlA4ysS9B7e)

1. Quick Check: Identify the Cause

Open your terminal or Command Prompt and run a quick check to see if environment variables are hijacking Python's startup path: [1] (/goto?url=CAESoQEBxCJF12b7kKmAbrnUePbXkGTnWNybrVKfXAVBpT4-5vEb2Fy_BYuteNCkyFsrPGcHpQXcROh0tCuo9US5MBlogDHKZLmlV1CVP6ooNSDJTf1dJwwUfBeV4tr2m3US5ZSFhBKbV0G2meeOkQzRlEnDRzjcyg2S6ig9UJEkDUEPKLWL_30yE_wcy89Y3H3QEsbggUY8BGup2ubSboL_RxbGww), [2] (/goto?url=CAESXwHEIkXXw_4FKJG43BYB7YLkJ8nf1jpkDWpfGGruaxFPMitbPWYmZ4EHbPxYswQCvKwwB9nIXJxFElJi2Rf6v6H3C_QxYL-YiHKT70Sgs0-0jrCwfaI_oqlA4ysS9B7e)
• Windows (Command Prompt): Run set PYTHON
• macOS / Linux (Terminal): Run env | grep PYTHON
If PYTHONHOME or PYTHONPATH appears in the output pointing to an old version or another program's bundled Python (such as PostgreSQL/EDB or an old install), that is the cause. [1] (/goto?url=CAESXwHEIkXXw_4FKJG43BYB7YLkJ8nf1jpkDWpfGGruaxFPMitbPWYmZ4EHbPxYswQCvKwwB9nIXJxFElJi2Rf6v6H3C_QxYL-YiHKT70Sgs0-0jrCwfaI_oqlA4ysS9B7e), [2] (/goto?url=CAESoQEBxCJF12b7kKmAbrnUePbXkGTnWNybrVKfXAVBpT4-5vEb2Fy_BYuteNCkyFsrPGcHpQXcROh0tCuo9US5MBlogDHKZLmlV1CVP6ooNSDJTf1dJwwUfBeV4tr2m3US5ZSFhBKbV0G2meeOkQzRlEnDRzjcyg2S6ig9UJEkDUEPKLWL_30yE_wcy89Y3H3QEsbggUY8BGup2ubSboL_RxbGww)

2. Fix Conflicting Environment Variables

Users on Stack Overflow agree that misconfigured PYTHONHOME variables are a primary trigger for this error. Removing them allows Python to find its own files automatically. [1] (/goto?url=CAESuAEBxCJF11d7hwLl7GPv8mGlip1ojq7so9pYhgrhKSBM1y9FTj0uilUjAfVh6igfvDL1RWfbTHZkNfA9NFTMfQHY07MMm9ei7zvkN8Qw9uvleFqe-5pFqr8rezXDJ14Wd5O5SKSkRmPiF0Ys-BA__AOl5salItd2-dx5_UaJYiWOQmcPDvzJzm72HWKpapGkg0iYO-R2uaFAjUsunbAc1usR9gU8lkAN6wsGHr0GlkuSsT3YXeqByfAj), [2] (/goto?url=CAESXwHEIkXXw_4FKJG43BYB7YLkJ8nf1jpkDWpfGGruaxFPMitbPWYmZ4EHbPxYswQCvKwwB9nIXJxFElJi2Rf6v6H3C_QxYL-YiHKT70Sgs0-0jrCwfaI_oqlA4ysS9B7e)
On Windows:
1. Press the Windows Key, type Environment Variables, and select Edit the system environment variables.
2. Click the Environment Variables... button near the bottom right.
3. Look under both User variables and System variables for PYTHONHOME and PYTHONPATH.
4. Select them and click Delete (back up the path string in a text file first just in case an older software suite relies on it).
5. Click OK to save, then restart your terminal or IDE. [1] (/goto?url=CAESXwHEIkXXw_4FKJG43BYB7YLkJ8nf1jpkDWpfGGruaxFPMitbPWYmZ4EHbPxYswQCvKwwB9nIXJxFElJi2Rf6v6H3C_QxYL-YiHKT70Sgs0-0jrCwfaI_oqlA4ysS9B7e)
On macOS / Linux:
1. Run unset PYTHONHOME and unset PYTHONPATH in your terminal to test if Python starts normally.
2. If that works, open your shell configuration file (such as ~/.zshrc or ~/.bashrc) and remove any export PYTHONHOME=... or export PYTHONPATH=... lines.

3. Fix Broken Virtual Environments or Embedded Tools

If no environment variables are set, the specific Python installation or virtual environment you are invoking is corrupted or incomplete. [1] (/goto?url=CAESjQEBxCJF1xTHjFZAIsf66Ol8kwisRJAGqJGcAK5jlg71cVsLIsYCfluHQU-Id1VSOgylwdfb3T1L4iDDLJ4ClryD5RC-SrvRpGv71Lf1XM9QrD8Ss-JmVpMc00PJPZgTsBlnNZNhzi0HHBG_dByq-plVQeSM4163Pj_rDmhVDr3u_3x69Tn0XO5JpUqlS88), [2] (/goto?url=CAESjQEBxCJF13jjwMUkLmSuKSFvn9y2eBX-4p_4Udu3DeNohOVX3IBgbc_Tjt8Zi33HYxfBusyYZBTWiuku7bUtLtdo2mumB65CMP8dOc4a2H8vy3SClvc0_H7gbmNCAmNsiSC08i44gLKOWOM9JsLnnUkNQvoGG8ZDCE6MpjdWzaFwA4yO9Qrl7_2w3ue6AHI)
• Virtual Environments (venv / conda): If this happens inside a project folder, the virtual environment's link to the base Python installation broke (often after a system Python update). Delete the venv folder and recreate it using your active Python installation (python -m venv venv), then reinstall your requirements.txt. [1] (/goto?url=CAESjQEBxCJF13jjwMUkLmSuKSFvn9y2eBX-4p_4Udu3DeNohOVX3IBgbc_Tjt8Zi33HYxfBusyYZBTWiuku7bUtLtdo2mumB65CMP8dOc4a2H8vy3SClvc0_H7gbmNCAmNsiSC08i44gLKOWOM9JsLnnUkNQvoGG8ZDCE6MpjdWzaFwA4yO9Qrl7_2w3ue6AHI)
• Arduino IDE / PlatformIO: Embedded boards (like Raspberry Pi Pico/RP2040 or ESP32/ESP8266) bundle their own standalone Python tools. In the Arduino IDE, open Tools > Board > Boards Manager, remove the affected board package, manually delete its leftover folder inside your Arduino15/packages/ directory, and reinstall it. [1] (/goto?url=CAESgQEBxCJF12PhEcUdM915XTt7sxdKSyDCW-R0bGaIso02jCEb_6xujHWYbagQjtqLAGS3hO1tey8G1m0SN-tuQkymN89zCn6wUAd-tmfcy_AzLVaaazJMJEHF-VXFvTcbf4tn6AJQpRXesesnfsGoqjw4m4mex-zr5YIIRxNMuBr4w5k), [2] (/goto?url=CAESjQEBxCJF1xTHjFZAIsf66Ol8kwisRJAGqJGcAK5jlg71cVsLIsYCfluHQU-Id1VSOgylwdfb3T1L4iDDLJ4ClryD5RC-SrvRpGv71Lf1XM9QrD8Ss-JmVpMc00PJPZgTsBlnNZNhzi0HHBG_dByq-plVQeSM4163Pj_rDmhVDr3u_3x69Tn0XO5JpUqlS88)
• Corrupted System Python: If running the global python command outside any virtual environment still fails, run the official Python installer again and choose Repair (or uninstall and reinstall it). [1] (/goto?url=CAESjQEBxCJF13jjwMUkLmSuKSFvn9y2eBX-4p_4Udu3DeNohOVX3IBgbc_Tjt8Zi33HYxfBusyYZBTWiuku7bUtLtdo2mumB65CMP8dOc4a2H8vy3SClvc0_H7gbmNCAmNsiSC08i44gLKOWOM9JsLnnUkNQvoGG8ZDCE6MpjdWzaFwA4yO9Qrl7_2w3ue6AHI)
If the error persists, let me know:
• Your operating system (Windows, macOS, or Linux)
• What you were doing when it appeared (running a script, activating a venv, compiling in Arduino, etc.)
I can help you trace the exact broken path.
