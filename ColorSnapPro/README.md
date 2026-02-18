# ColorSnap Pro

A full-stack color extraction and palette management application with a native iOS app and Node.js backend.

## 🎨 Features

- **Camera Color Picker**: Extract colors in real-time from your camera
- **Palette Management**: Create, edit, and share color palettes
- **Color Tools**: 
  - Color Harmony Generator (complementary, analogous, triadic, etc.)
  - Contrast Checker (WCAG compliance)
  - Gradient Generator
  - Color Blindness Simulator
  - Color Format Converter (HEX, RGB, HSL)
- **User Authentication**: JWT-based secure authentication
- **Cloud Sync**: Save and sync palettes across devices

## 🏗️ Architecture

### Backend (Node.js + Express)
- **Runtime**: Node.js 18+
- **Framework**: Express.js
- **Database**: PostgreSQL with Prisma ORM
- **Authentication**: JWT tokens
- **Real-time**: Socket.io for live updates

### Frontend (iOS + SwiftUI)
- **Framework**: SwiftUI
- **Minimum iOS**: 17.0
- **Camera**: AVFoundation
- **Networking**: URLSession

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- npm or yarn
- Xcode 15+ (for iOS app)
- PostgreSQL (or Docker)

### Option 1: Automated Launch

```bash
# Start everything (backend + iOS simulator)
./launch.sh

# Start only backend
./launch.sh -b

# Start only iOS app
./launch.sh -i

# Use Docker for database
./launch.sh -d
```

### Option 2: Manual Setup

#### 1. Backend Setup

```bash
cd backend

# Install dependencies
npm install

# Setup environment
cp .env.example .env
# Edit .env with your database credentials

# Generate Prisma client
npx prisma generate

# Run database migrations
npx prisma migrate dev

# Start development server
npm run dev
```

The backend will be available at `http://localhost:3001`

#### 2. iOS App Setup

```bash
cd ios-app

# Open in Xcode
open ColorSnapPro.xcodeproj

# Or build from command line
xcodebuild -project ColorSnapPro.xcodeproj -scheme ColorSnapPro -destination 'platform=iOS Simulator,name=iPhone 15 Pro' build
```

### Option 3: Docker Setup

```bash
# Start all services with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop services
docker-compose down
```

## 📁 Project Structure

```
ColorSnapPro/
├── backend/               # Node.js backend API
│   ├── src/
│   │   ├── routes/        # API routes
│   │   ├── middleware/    # Express middleware
│   │   ├── utils/         # Utility functions
│   │   └── server.ts      # Main server file
│   ├── prisma/
│   │   └── schema.prisma  # Database schema
│   └── package.json
├── ios-app/               # iOS SwiftUI app
│   ├── ColorSnapPro/
│   │   ├── Models/        # Data models
│   │   ├── Services/      # API services
│   │   ├── ViewModels/    # SwiftUI view models
│   │   └── Views/         # SwiftUI views
│   └── ColorSnapPro.xcodeproj
├── docker-compose.yml     # Docker setup
└── launch.sh              # Launch script
```

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login
- `GET /api/auth/me` - Get current user

### Palettes
- `GET /api/palettes` - List palettes
- `POST /api/palettes` - Create palette
- `GET /api/palettes/:id` - Get palette details
- `DELETE /api/palettes/:id` - Delete palette

### Colors
- `POST /api/colors/extract` - Extract color
- `GET /api/colors/history` - Get color history
- `GET /api/colors/favorites` - Get favorite colors

### Tools
- `POST /api/tools/harmony` - Generate color harmonies
- `POST /api/tools/contrast` - Check contrast ratio
- `POST /api/tools/gradient` - Generate gradient

## 🛠️ Development

### Backend Development

```bash
cd backend
npm run dev          # Start with hot reload
npm run db:studio    # Open Prisma Studio
npm run db:migrate   # Run migrations
npm run db:seed      # Seed database
```

### iOS Development

Open `ios-app/ColorSnapPro.xcodeproj` in Xcode and build using Cmd+R.

Make sure the simulator is running iOS 17+.

## 📝 Environment Variables

### Backend (.env)

```
NODE_ENV=development
PORT=3001
DATABASE_URL=postgresql://user:password@localhost:5432/colorsnap_pro
JWT_SECRET=your-super-secret-jwt-key
JWT_EXPIRES_IN=7d
```

## 🧪 Testing

### Backend Tests

```bash
cd backend
npm test
```

### iOS Tests

```bash
cd ios-app
xcodebuild test -project ColorSnapPro.xcodeproj -scheme ColorSnapPro -destination 'platform=iOS Simulator,name=iPhone 15 Pro'
```

## 📱 Screenshots

- Camera Color Picker with real-time color extraction
- Palette grid with color previews
- Color harmony generator
- Contrast checker with WCAG compliance

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Color conversion algorithms based on standard color theory
- WCAG 2.1 guidelines for accessibility compliance
- Apple Human Interface Guidelines for iOS app design
