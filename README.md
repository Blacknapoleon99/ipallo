# 🌐 BlackzAllocator - Professional IP Pool Management

<div align="center">

![BlackzAllocator Logo](blackz_icon.ico)

**A modern, professional IP pool management system with a beautiful GUI**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Windows](https://img.shields.io/badge/platform-Windows-blue.svg)](https://www.microsoft.com/windows/)

[📦 Download Latest Release](../../releases/latest) | [🚀 Quick Start](#-quick-start) | [📖 Documentation](#-features)

</div>

## 🎯 What is BlackzAllocator?

BlackzAllocator is a professional-grade IP pool management system designed for network administrators, developers, and IT professionals. It features a modern, intuitive interface inspired by macOS and Flutter applications, with smooth rounded corners and a dark theme.

## ✨ Key Features

- 🎨 **Modern GUI** - Smooth rounded corners, dark theme, professional design
- 🏊 **IP Pool Management** - Create, edit, and delete IP pools with CIDR notation
- 🎲 **Dynamic Allocation** - Multiple allocation strategies (first-fit, random, sequential, load-balanced)
- 📊 **Real-time Monitoring** - Live utilization statistics and pool health monitoring
- 🔗 **Network Interface Binding** - Bind allocated IPs to network interfaces
- 💾 **Database Storage** - SQLite backend for reliable data persistence
- 🚀 **RESTful API** - FastAPI backend for automation and integration
- 🔒 **IP Reservations** - Reserve specific IP addresses for critical services

## 🚀 Quick Start

### For Users (Windows)

1. **Download** the latest release from [Releases](../../releases/latest)
2. **Extract** the ZIP file
3. **Run** `install.bat` for automatic installation
4. **Launch** BlackzAllocator from desktop shortcut or Start Menu

### Manual Installation

1. Download `BlackzAllocator.exe` from releases
2. Run directly - no installation required!

## 🖼️ Screenshots

*Beautiful modern interface with dark theme and rounded corners*

## 🛠️ Development Setup

### Prerequisites
- Python 3.12+
- Windows 10/11 (64-bit)

### Installation

```bash
# Clone the repository
git clone https://github.com/YourUsername/BlackzAllocator.git
cd BlackzAllocator

# Install dependencies
pip install -r requirements.txt

# Run the application
python start_modern_gui.py
```

### Building from Source

```bash
# One-click build
./build_release.bat

# Or manual build
python build_release.py
```

## 🏗️ Architecture

- **Frontend**: CustomTkinter (Modern GUI framework)
- **Backend**: FastAPI (High-performance async API)
- **Database**: SQLite (Embedded database)
- **Networking**: psutil (System and network utilities)

## 📋 System Requirements

- **OS**: Windows 10/11 (64-bit)
- **RAM**: 512 MB minimum
- **Storage**: 100 MB available space
- **Network**: Internet connection for interface management

## 🎮 Usage

### Creating IP Pools
1. Click **"Create Pool"**
2. Enter pool name and CIDR (e.g., `192.168.1.0/24`)
3. Configure allocation strategy
4. Save and start managing IPs!

### Allocating IPs
1. Select a pool
2. Click **"Allocate IP"**
3. Choose allocation method
4. Optionally bind to network interface

### Monitoring
- View real-time utilization statistics
- Monitor pool health and usage patterns
- Track allocated vs. available IPs

## 🔧 API Documentation

BlackzAllocator includes a RESTful API for automation:

```bash
# Get all pools
GET /api/pools

# Create new pool
POST /api/pools
{
    "name": "office_network",
    "cidr": "192.168.1.0/24",
    "strategy": "first_fit"
}

# Allocate IP
POST /api/pools/{pool_id}/allocate
```

Visit `http://localhost:8000/docs` for interactive API documentation.

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **CustomTkinter** - For the beautiful modern GUI framework
- **FastAPI** - For the high-performance async API framework
- **SQLAlchemy** - For robust database operations
- **psutil** - For system and network utilities

## 📞 Support

- 🐛 **Bug Reports**: [Open an Issue](../../issues/new?template=bug_report.md)
- 💡 **Feature Requests**: [Open an Issue](../../issues/new?template=feature_request.md)
- 💬 **Questions**: [Start a Discussion](../../discussions)

## 🚀 Roadmap

- [ ] Linux and macOS support
- [ ] DHCP integration
- [ ] Advanced network scanning
- [ ] Multi-tenant support
- [ ] Cloud deployment options
- [ ] REST API authentication
- [ ] Backup and restore functionality

---

<div align="center">

**Made with ❤️ for network administrators and developers**

[⭐ Star this repo](../../stargazers) | [🍴 Fork it](../../fork) | [🐛 Report bug](../../issues)

</div> 