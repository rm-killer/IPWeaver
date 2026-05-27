# **⚡ IPWeaver**

[**🇮🇷 برای مشاهده توضیحات به زبان فارسی کلیک کنید (Persian Version)**](http://docs.google.com/README-fa.md)

**IPWeaver** is a high-performance, local network utility designed to automate IP discovery and multiplex proxy configurations for V2Ray. It bridges local ICMP concurrent pings with bulk URL parsing to generate optimized node configurations instantly.

## **✨ Features**

* **Multi-Threaded Mass Scanner:** Paste a bulk list of IPs and concurrently test their latency using raw ICMP pings.  
* **Bulk Config Generator:** Multiplex your existing V2Ray configurations (VMess, VLESS, Trojan, SS) across multiple working IPs instantly.  
* **Port Override:** Easily rewrite the ports for all generated configurations in one click.  
* **Dual-UI Design:** Toggle between a modern, stacked layout and a classic, side-by-side dark mode interface.  
* **Standalone Desktop App:** Runs as a portable .exe file with a native Windows UI, or as a Python script via your web browser.

## **🚀 Installation & Usage**

### **Option 1: Run the Standalone App (Easiest)**

We provide a pre-compiled .exe file so you don't need to install Python or compile anything yourself\!

1. Go to the [**Releases**](http://docs.google.com/releases](https://github.com/rm-killer/IPWeaver/releases) tab on GitHub.  
2. Download the latest IPWeaver.exe.  
3. Double-click the file to launch the native desktop application. No installation required\!

### **Option 2: Run from Source Code (For Developers)**

If you prefer to run the raw Python script:

1. Clone this repository:  
   git clone https://github.com/rm-killer/IPWeaver.git  
   cd IPWeaver

2. Install the required Python dependencies:  
   pip install fastapi uvicorn ping3 pywebview

3. Run the application:  
   python main.py

   *The application will automatically open in your default web browser.*

## **💖 Support the Project**

If IPWeaver helps you save time, consider supporting the development\!

**ETH Wallet Address:**

0x961CAdFe78395AEE95CC31a4BC3890E3e4dF7E59

*Created by [@rm-killer](https://github.com/rm-killer) · Open Source Initiative*
