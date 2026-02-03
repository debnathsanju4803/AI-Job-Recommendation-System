#!/bin/bash

# AI Job Recommendation System Startup Script

echo "🚀 Starting AI Job Recommendation System"
echo "=========================================="

# Check if we're in the right directory
if [ ! -f "src/api/main.py" ]; then
    echo "❌ Error: src/api/main.py not found. Please run this script from the project root directory."
    exit 1
fi

# Start the backend server in the background
echo "🌐 Starting backend server..."
python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Give the server time to start
echo "⏳ Waiting for backend server to start..."
sleep 3

# Check if server is running
if kill -0 $BACKEND_PID 2>/dev/null; then
    echo "✅ Backend server started successfully (PID: $BACKEND_PID)"
else
    echo "❌ Failed to start backend server"
    exit 1
fi

# Start frontend development server
echo "📱 Starting frontend development server..."
cd frontend
npm run dev &
FRONTEND_PID=$!

# Give the frontend server time to start
sleep 3

if kill -0 $FRONTEND_PID 2>/dev/null; then
    echo "✅ Frontend server started successfully (PID: $FRONTEND_PID)"
else
    echo "❌ Failed to start frontend server"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

echo ""
echo "🎉 System is ready!"
echo "📊 Backend: http://localhost:8000"
echo "🌐 Frontend: http://localhost:3000"
echo ""
echo "To stop the system, press Ctrl+C or run: kill $BACKEND_PID $FRONTEND_PID"
echo ""

# Wait for user to stop the system
trap "echo '🛑 Stopping system...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0" INT TERM

# Keep the script running
wait $BACKEND_PID $FRONTEND_PID