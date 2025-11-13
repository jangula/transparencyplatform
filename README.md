# 🇳🇦 National Strategy Transparency Platform

A comprehensive web platform for enhancing transparency, accountability, and public engagement in Namibia's national development strategies.

![Namibia Flag Colors](https://img.shields.io/badge/Namibia-Democracy%20%26%20Transparency-003893?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)
![React](https://img.shields.io/badge/React-18+-61DAFB?style=for-the-badge&logo=react)

## 📋 Overview

The National Strategy Transparency Platform is a digital solution designed to bridge the gap between government strategies and public understanding. It provides a centralized hub where citizens can:

- 🔍 **Explore** national development strategies and initiatives
- 📊 **Track** real-time progress and budget utilization
- 💬 **Ask Questions** directly to strategy owners
- 🗺️ **Discover** Namibia's 14 regions and their development
- 📈 **Monitor** Vision 2030 goals and achievements

## ✨ Key Features

### For Citizens
- **Strategy Dashboard**: Browse all national strategies with real-time progress tracking
- **Interactive Q&A**: Submit questions and get answers from government officials
- **Regional Information**: Explore interactive map with all 14 Namibian regions
- **Progress Tracking**: Monitor budget allocation and milestone completion
- **Public Engagement**: Stay informed about national development initiatives

### For Government Officials
- **Strategy Management**: Create and manage national strategies
- **Progress Updates**: Post regular updates on strategy implementation
- **Question Management**: Review and respond to public inquiries
- **Analytics Dashboard**: Track engagement and public interest
- **Role-Based Access**: Secure, hierarchical permission system

### Interactive Features
- 🗺️ **Namibia Regional Map**: Click on any of the 14 regions to learn about their unique characteristics
- 📊 **Development Targets**: Visual progress bars for Vision 2030 goals
- 📜 **Historical Timeline**: Journey through Namibia's presidential history
- 👥 **Current Leadership**: Up-to-date information on government leaders

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- PostgreSQL 13+
- npm or yarn

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/transparency-platform.git
cd transparency-platform
```

2. **Start the system**
```bash
chmod +x START_SYSTEM.sh
./START_SYSTEM.sh
```

3. **Access the platform**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Default Login Credentials

```
Platform Admin:
  Email: admin@gov.na
  Password: Admin@123456

Ministry Admin:
  Email: admin.mme@gov.na
  Password: Admin@123456

Strategy Owner:
  Email: owner1.mme@gov.na
  Password: Owner@123456
```

> ⚠️ **Important**: Change these credentials in production!

## 🏗️ Architecture

### Backend (FastAPI)
```
backend/
├── api/              # API endpoints
│   ├── auth.py       # Authentication
│   ├── strategies.py # Strategy management
│   ├── questions.py  # Q&A system
│   └── updates.py    # Progress updates
├── models/           # Database models
├── services/         # Business logic
└── core/            # Configuration
```

### Frontend (React + TypeScript)
```
frontend/
├── src/
│   ├── components/   # Reusable components
│   │   ├── NamibiaMap.tsx
│   │   ├── Leadership.tsx
│   │   └── DevelopmentTargets.tsx
│   ├── pages/        # Page components
│   │   ├── HomePage.tsx
│   │   ├── AboutPage.tsx
│   │   └── StrategyDetailPage.tsx
│   ├── services/     # API services
│   └── types/        # TypeScript types
```

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL + SQLAlchemy
- **Authentication**: JWT tokens
- **Validation**: Pydantic
- **Migration**: Alembic

### Frontend
- **Framework**: React 18 + TypeScript
- **UI Library**: Material-UI (MUI)
- **Routing**: React Router v6
- **HTTP Client**: Axios
- **Maps**: react-simple-maps (Natural Earth data)
- **Date Handling**: date-fns

### DevOps
- **Containerization**: Docker + Docker Compose
- **Reverse Proxy**: Nginx
- **Database**: PostgreSQL 13

## 📚 Documentation

- [Project Structure](PROJECT_STRUCTURE.md) - Detailed codebase organization
- [Quick Start Guide](QUICKSTART.md) - Step-by-step setup instructions
- [Login Credentials](LOGIN_CREDENTIALS.md) - Test account information
- [API Documentation](http://localhost:8000/docs) - Interactive Swagger docs

## 🔐 Security Features

- JWT-based authentication
- Role-based access control (RBAC)
- Password hashing with bcrypt
- SQL injection prevention
- XSS protection
- CORS configuration
- Environment variable management

## 🎨 Design Principles

- **User-Centric**: Intuitive interface for all user types
- **Accessible**: WCAG 2.1 compliant design
- **Responsive**: Mobile-first approach
- **Fast**: Optimized performance and loading times
- **Transparent**: Clear data visualization and reporting

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Development Team** - Initial work and ongoing development

## 🙏 Acknowledgments

- Republic of Namibia for inspiration
- Natural Earth for open-source map data
- FastAPI and React communities
- All contributors and testers

## 📞 Support

For support, open an issue on GitHub or contact the development team.

## 🗺️ Roadmap

- [ ] Mobile application (iOS/Android)
- [ ] SMS notification system
- [ ] Multi-language support (English, Afrikaans, Oshiwambo)
- [ ] Advanced analytics dashboard
- [ ] Integration with government systems
- [ ] Public API for developers
- [ ] Accessibility improvements

## 📊 Project Status

Active development - Version 1.0.0

---

**Made with ❤️ for Namibia's transparency and democratic governance**
