import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import rateLimit from 'express-rate-limit';
import dotenv from 'dotenv';
import path from 'path';
import { createServer } from 'http';
import { Server } from 'socket.io';

import { errorHandler } from './middleware/error_handler';
import { authRouter } from './routes/auth';
import { paletteRouter } from './routes/palettes';
import { colorRouter } from './routes/colors';
import { toolRouter } from './routes/tools';
import { userRouter } from './routes/users';

dotenv.config();

const app = express();
const httpServer = createServer(app);
const io = new Server(httpServer, {
  cors: {
    origin: process.env.NODE_ENV === 'production' 
      ? ['https://colorsnap.pro', 'https://www.colorsnap.pro']
      : ['http://localhost:3000', 'http://localhost:19006', 'capacitor://localhost'],
    methods: ['GET', 'POST']
  }
});

const PORT = process.env.PORT || 3001;

// Security middleware
app.use(helmet({
  crossOriginResourcePolicy: { policy: 'cross-origin' }
}));

app.use(cors({
  origin: process.env.NODE_ENV === 'production'
    ? ['https://colorsnap.pro', 'https://www.colorsnap.pro']
    : ['http://localhost:3000', 'http://localhost:19006', 'capacitor://localhost', 'http://127.0.0.1:3000'],
  credentials: true
}));

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: { error: 'Too many requests, please try again later.' }
});
app.use(limiter);

// Stricter rate limit for auth endpoints
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5,
  message: { error: 'Too many authentication attempts, please try again later.' }
});

app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));

// Static files for uploads
app.use('/uploads', express.static(path.join(__dirname, '../uploads')));

// Health check
app.get('/health', (req, res) => {
  res.json({ 
    status: 'ok', 
    timestamp: new Date().toISOString(),
    version: '1.0.0'
  });
});

// API routes
app.use('/api/auth', authLimiter, authRouter);
app.use('/api/palettes', paletteRouter);
app.use('/api/colors', colorRouter);
app.use('/api/tools', toolRouter);
app.use('/api/users', userRouter);

// WebSocket connection handling
io.on('connection', (socket) => {
  console.log('Client connected:', socket.id);
  
  socket.on('join-palette', (paletteId: string) => {
    socket.join(`palette-${paletteId}`);
  });
  
  socket.on('leave-palette', (paletteId: string) => {
    socket.leave(`palette-${paletteId}`);
  });
  
  socket.on('palette-update', (data: { paletteId: string; changes: any }) => {
    socket.to(`palette-${data.paletteId}`).emit('palette-updated', data);
  });
  
  socket.on('disconnect', () => {
    console.log('Client disconnected:', socket.id);
  });
});

// Make io accessible to routes
app.set('io', io);

// Error handling
app.use(errorHandler);

// 404 handler
app.use((req, res) => {
  res.status(404).json({ error: 'Endpoint not found' });
});

httpServer.listen(PORT, () => {
  console.log(`🚀 ColorSnap Pro API server running on port ${PORT}`);
  console.log(`📊 Health check: http://localhost:${PORT}/health`);
});

export { io };
