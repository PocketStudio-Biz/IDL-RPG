#!/bin/bash

# ColorSnap Pro Backend Startup Script

echo "🎨 Starting ColorSnap Pro Backend..."

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Generate Prisma client
echo "🔧 Generating Prisma client..."
npx prisma generate

# Check if database is ready
echo "⏳ Waiting for database..."
for i in {1..30}; do
    if npx prisma db execute --stdin <<<'SELECT 1' >/dev/null 2>&1; then
        echo "✅ Database is ready!"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "⚠️  Could not connect to database, continuing anyway..."
    fi
    sleep 1
done

# Run migrations
echo "🗄️  Running database migrations..."
npx prisma migrate dev --name init --skip-generate || npx prisma migrate deploy

echo "🚀 Starting server..."
npm run dev
