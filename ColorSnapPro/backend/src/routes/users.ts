import { Router } from 'express';
import { z } from 'zod';
import { prisma } from '../utils/prisma';
import { asyncHandler } from '../middleware/errorHandler';
import { authenticate } from '../middleware/auth';
import { AuthenticatedRequest } from '../types';

const router = Router();

// Get user profile
router.get(
  '/:username',
  asyncHandler(async (req, res) => {
    const { username } = req.params;

    const user = await prisma.user.findUnique({
      where: { username },
      select: {
        id: true,
        username: true,
        displayName: true,
        avatarUrl: true,
        createdAt: true,
        _count: {
          select: {
            palettes: { where: { isPublic: true } },
          },
        },
      },
    });

    if (!user) {
      return res.status(404).json({
        success: false,
        error: 'User not found',
      });
    }

    res.json({
      success: true,
      data: user,
    });
  })
);

// Get user's public palettes
router.get(
  '/:username/palettes',
  asyncHandler(async (req, res) => {
    const { username } = req.params;
    const { page = '1', limit = '20' } = req.query;

    const user = await prisma.user.findUnique({
      where: { username },
    });

    if (!user) {
      return res.status(404).json({
        success: false,
        error: 'User not found',
      });
    }

    const skip = (parseInt(page as string) - 1) * parseInt(limit as string);
    const take = parseInt(limit as string);

    const [palettes, total] = await Promise.all([
      prisma.palette.findMany({
        where: {
          userId: user.id,
          isPublic: true,
        },
        skip,
        take,
        orderBy: { createdAt: 'desc' },
        include: {
          colors: {
            orderBy: { position: 'asc' },
          },
          _count: {
            select: { colors: true },
          },
        },
      }),
      prisma.palette.count({
        where: {
          userId: user.id,
          isPublic: true,
        },
      }),
    ]);

    res.json({
      success: true,
      data: {
        palettes,
        pagination: {
          page: parseInt(page as string),
          limit: take,
          total,
          pages: Math.ceil(total / take),
        },
      },
    });
  })
);

// Get current user's stats
router.get(
  '/me/stats',
  authenticate,
  asyncHandler(async (req: AuthenticatedRequest, res) => {
    const [paletteCount, colorHistoryCount, favoriteCount, publicPaletteCount] = await Promise.all([
      prisma.palette.count({
        where: { userId: req.user!.id },
      }),
      prisma.colorHistory.count({
        where: { userId: req.user!.id },
      }),
      prisma.favoriteColor.count({
        where: { userId: req.user!.id },
      }),
      prisma.palette.count({
        where: { 
          userId: req.user!.id,
          isPublic: true,
        },
      }),
    ]);

    // Get recent activity
    const recentPalettes = await prisma.palette.findMany({
      where: { userId: req.user!.id },
      orderBy: { updatedAt: 'desc' },
      take: 5,
      select: {
        id: true,
        name: true,
        updatedAt: true,
        _count: {
          select: { colors: true },
        },
      },
    });

    const recentColors = await prisma.colorHistory.findMany({
      where: { userId: req.user!.id },
      orderBy: { extractedAt: 'desc' },
      take: 5,
      select: {
        id: true,
        hexValue: true,
        sourceType: true,
        extractedAt: true,
      },
    });

    res.json({
      success: true,
      data: {
        counts: {
          palettes: paletteCount,
          publicPalettes: publicPaletteCount,
          colorHistory: colorHistoryCount,
          favorites: favoriteCount,
        },
        recent: {
          palettes: recentPalettes,
          colors: recentColors,
        },
      },
    });
  })
);

export { router as userRouter };
