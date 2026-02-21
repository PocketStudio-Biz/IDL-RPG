#!/bin/bash

# ColorSnap Pro - Full Stack Launcher
# This script starts both the backend API and the iOS app

set -e

echo "🎨 ColorSnap Pro - Launch Script"
echo "=================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored messages
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check for required tools
check_dependencies() {
    print_info "Checking dependencies..."
    
    # Check for Node.js
    if ! command -v node &> /dev/null; then
        print_error "Node.js is not installed. Please install Node.js 18+"
        exit 1
    fi
    
    NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
    if [ "$NODE_VERSION" -lt 18 ]; then
        print_error "Node.js 18+ is required. Current version: $(node -v)"
        exit 1
    fi
    print_success "Node.js $(node -v) found"
    
    # Check for npm
    if ! command -v npm &> /dev/null; then
        print_error "npm is not installed"
        exit 1
    fi
    print_success "npm found"
    
    # Check for Docker (optional but recommended)
    if command -v docker &> /dev/null; then
        print_success "Docker found"
        HAS_DOCKER=true
    else
        print_warning "Docker not found. Database setup will need to be done manually"
        HAS_DOCKER=false
    fi
    
    # Check for Xcode
    if command -v xcodebuild &> /dev/null; then
        print_success "Xcode found"
        HAS_XCODE=true
    else
        print_warning "Xcode not found. iOS app cannot be built"
        HAS_XCODE=false
    fi
    
    echo ""
}

# Setup backend
setup_backend() {
    print_info "Setting up backend..."
    cd "$SCRIPT_DIR/backend"
    
    # Install dependencies if needed
    if [ ! -d "node_modules" ]; then
        print_info "Installing backend dependencies..."
        npm install
    fi
    
    # Setup environment file
    if [ ! -f ".env" ]; then
        print_info "Creating .env file from template..."
        cp .env.example .env
        print_warning "Please review and update the .env file with your settings"
    fi
    
    # Generate Prisma client
    print_info "Generating Prisma client..."
    npx prisma generate
    
    print_success "Backend setup complete"
    echo ""
}

# Start backend
start_backend() {
    print_info "Starting backend server..."
    cd "$SCRIPT_DIR/backend"
    
    # Check if we should use Docker
    if [ "$HAS_DOCKER" = true ] && [ "$USE_DOCKER" = true ]; then
        print_info "Starting services with Docker..."
        cd "$SCRIPT_DIR"
        docker-compose up -d postgres
        
        # Wait for database
        print_info "Waiting for database to be ready..."
        sleep 5
        
        # Run migrations
        cd "$SCRIPT_DIR/backend"
        npx prisma migrate dev --name init --skip-generate 2>/dev/null || npx prisma migrate deploy
    fi
    
    # Start the server in the background
    npm run dev &
    BACKEND_PID=$!
    
    # Wait for server to be ready
    print_info "Waiting for backend to start..."
    for i in {1..30}; do
        if curl -s http://localhost:3001/health > /dev/null 2>&1; then
            print_success "Backend is running on http://localhost:3001"
            return 0
        fi
        sleep 1
    done
    
    print_error "Backend failed to start"
    return 1
}

# Build and run iOS app
start_ios_app() {
    if [ "$HAS_XCODE" = false ]; then
        print_warning "Skipping iOS app - Xcode not found"
        return 0
    fi
    
    print_info "Building iOS app..."
    cd "$SCRIPT_DIR/ios-app"
    
    # Check if we should run on simulator or device
    if [ "$RUN_ON_DEVICE" = true ]; then
        print_info "Building for device..."
        # This requires proper signing configuration
        xcodebuild -project ColorSnapPro.xcodeproj -scheme ColorSnapPro -destination 'generic/platform=iOS' build
    else
        print_info "Building for simulator..."
        # Find available simulator
        SIMULATOR_ID=$(xcrun simctl list devices available | grep -E "iPhone.*(\d+\.)?\d+" | head -1 | grep -oE '[0-9A-F]{8}-([0-9A-F]{4}-){3}[0-9A-F]{12}')
        
        if [ -z "$SIMULATOR_ID" ]; then
            print_warning "No simulator found. Starting iPhone 15 simulator..."
            SIMULATOR_ID=$(xcrun simctl list devices | grep "iPhone 15 Pro" | grep -oE '[0-9A-F]{8}-([0-9A-F]{4}-){3}[0-9A-F]{12}' | head -1)
            xcrun simctl boot "$SIMULATOR_ID" 2>/dev/null || true
        fi
        
        print_info "Launching on simulator: $SIMULATOR_ID"
        
        # Build and run
        xcodebuild -project ColorSnapPro.xcodeproj \
                   -scheme ColorSnapPro \
                   -destination "id=$SIMULATOR_ID" \
                   -derivedDataPath build \
                   build
        
        # Install and launch
        APP_PATH="$SCRIPT_DIR/ios-app/build/Build/Products/Debug-iphonesimulator/ColorSnapPro.app"
        if [ -d "$APP_PATH" ]; then
            xcrun simctl install "$SIMULATOR_ID" "$APP_PATH"
            xcrun simctl launch "$SIMULATOR_ID" com.colorsnap.pro
            print_success "iOS app launched on simulator"
            
            # Open Simulator app
            open -a Simulator
        else
            print_error "App build not found at $APP_PATH"
        fi
    fi
}

# Print usage
print_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -h, --help       Show this help message"
    echo "  -b, --backend    Start only the backend"
    echo "  -i, --ios        Start only the iOS app"
    echo "  -d, --docker     Use Docker for database"
    echo "  --device         Run iOS app on connected device"
    echo "  --setup          Setup only (don't start services)"
    echo ""
    echo "Examples:"
    echo "  $0                    Start both backend and iOS app"
    echo "  $0 -b                 Start only backend"
    echo "  $0 -i                 Start only iOS app"
    echo "  $0 -d                 Use Docker for database"
}

# Main function
main() {
    # Parse arguments
    START_BACKEND=true
    START_IOS=true
    USE_DOCKER=false
    RUN_ON_DEVICE=false
    SETUP_ONLY=false
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                print_usage
                exit 0
                ;;
            -b|--backend)
                START_IOS=false
                shift
                ;;
            -i|--ios)
                START_BACKEND=false
                shift
                ;;
            -d|--docker)
                USE_DOCKER=true
                shift
                ;;
            --device)
                RUN_ON_DEVICE=true
                shift
                ;;
            --setup)
                SETUP_ONLY=true
                shift
                ;;
            *)
                print_error "Unknown option: $1"
                print_usage
                exit 1
                ;;
        esac
    done
    
    # Check dependencies
    check_dependencies
    
    # Setup
    if [ "$START_BACKEND" = true ]; then
        setup_backend
    fi
    
    if [ "$SETUP_ONLY" = true ]; then
        print_success "Setup complete!"
        exit 0
    fi
    
    # Create a trap to kill background processes on exit
    cleanup() {
        echo ""
        print_info "Shutting down..."
        if [ -n "$BACKEND_PID" ]; then
            kill $BACKEND_PID 2>/dev/null || true
        fi
        if [ "$USE_DOCKER" = true ]; then
            cd "$SCRIPT_DIR"
            docker-compose down 2>/dev/null || true
        fi
        print_success "Goodbye!"
    }
    trap cleanup EXIT INT TERM
    
    # Start services
    if [ "$START_BACKEND" = true ]; then
        start_backend
    fi
    
    if [ "$START_IOS" = true ]; then
        # Give backend time to fully start
        sleep 2
        start_ios_app
    fi
    
    echo ""
    print_success "All services started!"
    echo ""
    print_info "Backend API: http://localhost:3001"
    print_info "Health Check: http://localhost:3001/health"
    print_info "iOS App: Running on simulator"
    echo ""
    print_info "Press Ctrl+C to stop all services"
    
    # Keep script running
    if [ "$START_BACKEND" = true ]; then
        wait $BACKEND_PID
    else
        # Just wait indefinitely
        while true; do
            sleep 1
        done
    fi
}

main "$@"
