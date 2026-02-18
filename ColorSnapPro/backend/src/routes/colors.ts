import { Router } from 'express';
import { z } from 'zod';
import { prisma } from '../utils/prisma';
import { asyncHandler } from '../middleware/errorHandler';
import { authenticate } from '../middleware/auth';
import { AuthenticatedRequest } from '../types';
import { hexToRgb, rgbToHsl, suggestColorName } from '../utils/color';

const router = Router();

// Extract color and save to history
router.post(
  '/extract',
  authenticate,
  asyncHandler(async (req: AuthenticatedRequest, res) => {
    const schema = z.object({
      hex: z.string().regex(/^#[0-9A-Fa-f]{6}$/),
      sourceType: z.enum(['camera', 'image', 'manual', 'picker']).default('manual'),
      sourceImage: z.string().optional(),
    });

    const data = schema.parse(req.body);
    const rgb = hexToRgb(data.hex);
    const hsl = rgbToHsl(rgb.r, rgb.g, rgb.b);

    // Save to color history
    const historyEntry = await prisma.colorHistory.create({
      data: {
        userId: req.user!.id,
        hexValue: data.hex.toUpperCase(),
        rgbR: rgb.r,
        rgbG: rgb.g,
        rgbB: rgb.b,
        sourceType: data.sourceType,
        sourceImage: data.sourceImage,
      },
    });

    // Get color name suggestions
    const nameSuggestions = suggestColorName(data.hex);

    res.json({
      success: true,
      data: {
        hex: data.hex.toUpperCase(),
        rgb,
        hsl,
        nameSuggestions,
        historyEntry,
      },
    });
  })
);

// Get color history
router.get(
  '/history',
  authenticate,
  asyncHandler(async (req: AuthenticatedRequest, res) => {
    const { page = '1', limit = '50' } = req.query;
    
    const skip = (parseInt(page as string) - 1) * parseInt(limit as string);
    const take = parseInt(limit as string);

    const [history, total] = await Promise.all([
      prisma.colorHistory.findMany({
        where: { userId: req.user!.id },
        skip,
        take,
        orderBy: { extractedAt: 'desc' },
      }),
      prisma.colorHistory.count({
        where: { userId: req.user!.id },
      }),
    ]);

    res.json({
      success: true,
      data: {
        history,
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

// Delete from history
router.delete(
  '/history/:id',
  authenticate,
  asyncHandler(async (req: AuthenticatedRequest, res) => {
    const { id } = req.params;

    const entry = await prisma.colorHistory.findUnique({
      where: { id },
    });

    if (!entry) {
      return res.status(404).json({
        success: false,
        error: 'History entry not found',
      });
    }

    if (entry.userId !== req.user!.id) {
      return res.status(403).json({
        success: false,
        error: 'Not authorized',
      });
    }

    await prisma.colorHistory.delete({
      where: { id },
    });

    res.json({
      success: true,
      message: 'History entry deleted',
    });
  })
);

// Get favorite colors
router.get(
  '/favorites',
  authenticate,
  asyncHandler(async (req: AuthenticatedRequest, res) => {
    const favorites = await prisma.favoriteColor.findMany({
      where: { userId: req.user!.id },
      orderBy: { createdAt: 'desc' },
    });

    res.json({
      success: true,
      data: favorites,
    });
  })
);

// Add to favorites
router.post(
  '/favorites',
  authenticate,
  asyncHandler(async (req: AuthenticatedRequest, res) => {
    const schema = z.object({
      hex: z.string().regex(/^#[0-9A-Fa-f]{6}$/),
      name: z.string().optional(),
    });

    const data = schema.parse(req.body);
    const rgb = hexToRgb(data.hex);

    try {
      const favorite = await prisma.favoriteColor.create({
        data: {
          userId: req.user!.id,
          hexValue: data.hex.toUpperCase(),
          rgbR: rgb.r,
          rgbG: rgb.g,
          rgbB: rgb.b,
          name: data.name,
        },
      });

      res.status(201).json({
        success: true,
        data: favorite,
      });
    } catch (error: any) {
      if (error.code === 'P2002') {
        return res.status(409).json({
          success: false,
          error: 'Color already in favorites',
        });
      }
      throw error;
    }
  })
);

// Remove from favorites
router.delete(
  '/favorites/:id',
  authenticate,
  asyncHandler(async (req: AuthenticatedRequest, res) => {
    const { id } = req.params;

    const favorite = await prisma.favoriteColor.findUnique({
      where: { id },
    });

    if (!favorite) {
      return res.status(404).json({
        success: false,
        error: 'Favorite not found',
      });
    }

    if (favorite.userId !== req.user!.id) {
      return res.status(403).json({
        success: false,
        error: 'Not authorized',
      });
    }

    await prisma.favoriteColor.delete({
      where: { id },
    });

    res.json({
      success: true,
      message: 'Removed from favorites',
    });
  })
);

// Get color name suggestions
router.get(
  '/suggestions',
  asyncHandler(async (req, res) => {
    const schema = z.object({
      hex: z.string().regex(/^#[0-9A-Fa-f]{6}$/),
    });

    const { hex } = schema.parse(req.query);
    const suggestions = suggestColorName(hex);

    res.json({
      success: true,
      data: {
        hex: hex.toUpperCase(),
        suggestions,
      },
    });
  })
);

export { router as colorRouter };
