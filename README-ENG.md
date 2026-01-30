# 🚀 IUTBox Uploader

<div align="center">

![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)
![NextCloud](https://img.shields.io/badge/NextCloud-0082C9?style=for-the-badge&logo=nextcloud&logoColor=white)

**Supercharge your IUTBox uploads with lightning-fast GitHub Actions! ⚡**

English | [فارسی](README_FA.md)

</div>

---

## 🎯 What is IUTBox Uploader?

**IUTBox Uploader** is a powerful automation tool that leverages **GitHub Actions** to download files from Telegram or direct links and automatically upload them to **IUTBox** (Isfahan University of Technology's NextCloud-based cloud storage).

### ✨ Why Use This Tool?

- 🚀 **Blazing Fast**: Utilize GitHub's powerful infrastructure for high-speed downloads and uploads
- 🤖 **Fully Automated**: No need to download files to your device first
- 🔒 **Secure**: All credentials are encrypted and stored in GitHub Secrets
- 🌐 **Multi-Source**: Support for direct download links and Telegram files
- 💾 **Unlimited Bandwidth**: Take advantage of GitHub Actions' generous resources
- 🎓 **Optimized for IUT**: Specifically designed for Isfahan University of Technology students

---

## 🎬 Getting Started

### Prerequisites

Before you begin, make sure you have:

- ✅ A GitHub account
- ✅ An IUTBox account (IUT students)
- ✅ Your student ID number
- ✅ Basic familiarity with GitHub (don't worry, we'll guide you!)

---

## 📋 Step-by-Step Setup Guide

### Step 1: Fork This Repository

First, you need to create your own copy of this repository.

1. Click the **"Fork"** button in the top-right corner of this page
2. Wait a few seconds for GitHub to create your fork
3. You'll be redirected to your forked repository: `https://github.com/YOUR_USERNAME/iutbox`

![Fork Button Location](https://docs.github.com/assets/cb-40742/mw-1440/images/help/repository/fork-button.webp)

---

### Step 2: Create IUTBox App Password

For security reasons, you need to create a special app password for this tool.

1. **Go to IUTBox Settings**: Navigate to [https://iutbox.iut.ac.ir/index.php/settings/user/security](https://iutbox.iut.ac.ir/index.php/settings/user/security)
2. **Log in** with your university credentials
3. **Scroll down** to the "App passwords" section
4. **Enter a name** for your app password (e.g., "GitHub Actions")
5. Click **"Create new app password"**
6. **Copy the generated password** (it will only be shown once!)

> ⚠️ **Important**: Save this password somewhere safe! You won't be able to see it again.

---

### Step 3: Configure GitHub Secrets

Now we need to securely store your credentials in GitHub.

1. **Go to your forked repository** on GitHub
2. Click the **"Settings"** tab (top navigation bar)
3. In the left sidebar, click **"Secrets and variables"**
4. Click **"Actions"**
5. Click the **"New repository secret"** button

You need to create **two secrets**:

#### Secret #1: `IUTBOX_USER`
- **Name**: `IUTBOX_USER`
- **Value**: Your student ID number (e.g., `401234567`)
- Click **"Add secret"**

#### Secret #2: `IUTBOX_PASS`
- **Name**: `IUTBOX_PASS`
- **Value**: The app password you created in Step 2
- Click **"Add secret"**

![GitHub Secrets Location](https://docs.github.com/assets/cb-58763/mw-1440/images/help/settings/actions-secrets-new.webp)

> 🔒 **Security Note**: GitHub Secrets are encrypted and cannot be viewed after creation. They're only accessible during workflow runs.

---

## 🎯 How to Use

### Method 1: Direct Download (Simple & Fast) 🔗

Perfect for downloading files from direct links (Google Drive, Dropbox, file servers, etc.)

1. **Go to the "Actions" tab** in your forked repository
2. **Click on the "Direct download and Upload to IUTBOX" workflow** (left sidebar)
3. **Click "Run workflow"** button (right side)
4. **Enter the direct download link** in the "File URL to download" field
   - Example: `https://example.com/files/document.pdf`
5. **Click the green "Run workflow" button**
6. **Wait for completion** (usually 1-5 minutes depending on file size)
7. **Check your IUTBox** - your file is there! 🎉

![Running a Workflow](https://docs.github.com/assets/cb-32237/mw-1440/images/help/actions/workflow-dispatch-button.webp)

---

### Method 2: Telegram Download (Coming Soon) 📱

> 🚧 **Under Development**: The Telegram download feature is currently being improved for easier setup. Stay tuned!

This method will allow you to:
- Download files from Telegram channels
- Download files from Telegram groups
- Download files from private chats
- Automatically upload them to IUTBox

**Additional Secrets Required** (documentation coming soon):
- `TELEGRAM_API_ID`
- `TELEGRAM_API_HASH`
- `TELEGRAM_PHONE`
- `TELEGRAM_SESSION_STRING`

---

## 📸 Visual Guide

### Finding the Actions Tab

```
Your Repository → Actions → Select Workflow → Run workflow
```

### Monitoring Progress

After starting a workflow:
1. You'll see a yellow dot (⚫) while it's running
2. It will turn into a green checkmark (✅) when complete
3. Or a red X (❌) if something went wrong

Click on the workflow run to see detailed logs and progress.

---

## 🛠️ Troubleshooting

### Common Issues and Solutions

#### ❌ Error: "Invalid credentials"
- **Solution**: Double-check your `IUTBOX_USER` and `IUTBOX_PASS` secrets
- Make sure you're using the **app password**, not your regular IUTBox password

#### ❌ Error: "Download failed"
- **Solution**: Verify the URL is a direct download link
- Some services require authentication - this tool works best with direct links

#### ❌ Error: "Workflow not found"
- **Solution**: Make sure you've forked the repository correctly
- Try refreshing the Actions tab

#### ❌ File doesn't appear in IUTBox
- **Solution**: Check the workflow logs for errors
- Verify your IUTBox connection
- Ensure you have enough storage space in IUTBox

---

## 🔧 Technical Details

### Architecture

```
┌─────────────────┐
│   Direct Link   │
│  or Telegram    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ GitHub Actions  │
│   (Download)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   IUTBox API    │
│    (Upload)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Your IUTBox   │
│    Storage      │
└─────────────────┘
```

### Technologies Used

- **GitHub Actions**: Workflow automation
- **Python 3.11**: Core programming language
- **Telethon**: Telegram API client
- **Requests**: HTTP library for uploads
- **WebDAV**: IUTBox/NextCloud protocol
- **Wget & cURL**: Download utilities

---

## 🤝 Contributing

Found a bug? Have a feature request? Contributions are welcome!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is open source and available to Isfahan University of Technology students.

---

## 💡 Tips & Tricks

### Maximizing Efficiency

- **Use direct links when possible**: They're faster and more reliable than Telegram downloads
- **Monitor your GitHub Actions quota**: Free accounts get 2000 minutes per month
- **Upload during off-peak hours**: For best IUTBox performance

### Advanced Usage

- **Batch uploads**: Run multiple workflows simultaneously
- **Scheduled uploads**: Modify workflows to run on a schedule (cron)
- **Custom paths**: Edit the workflow to upload to specific folders

---

## 📞 Support

- 🐛 **Report Bugs**: Open an issue on GitHub
- 💬 **Questions**: Check existing issues or open a new one
- 🎓 **IUT Students**: Contact university IT support for IUTBox-related issues

---

## 🌟 Show Your Support

If this tool helped you, consider:
- ⭐ Starring this repository
- 🔄 Sharing it with your classmates
- 🤝 Contributing improvements

---

<div align="center">

**Made with ❤️ for Isfahan University of Technology Students**

*Powered by GitHub Actions ⚡*

[Report Bug](https://github.com/mahdikarami8484/iutbox/issues) · [Request Feature](https://github.com/mahdikarami8484/iutbox/issues)

</div>
