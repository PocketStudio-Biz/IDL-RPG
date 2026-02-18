import { Router } from 'express';
import { z } from 'zod';
import { prisma } from '../utils/prisma';
import { asyncHandler } from '../middleware/errorHandler';
import { authenticate, optionalAuth } from '../middleware/auth';
import { AuthenticatedRequest, CreatePaletteBody } from '../types';
import { hexToRgb, rgbToHsl } from '../utils/color';

const router = Router();

const paletteSchema = z.object({
  name: z.string().min(1).max(100),
  description: z.string().max(500).optional(),
  isPublic: z.boolean().optional(),
  colors: z.array(z.object({
    hex: z.string().regex(/^#[0-9A-Fa-f]{6}$/, 'Invalid hex color'),
    name: z.string().optional(),
    position: z.number().int().min(0).optional(),
  })).optional(),
});

// Get all palettes (public ones + user's own)
router.get(
  '/',
  optionalAuth,
  asyncHandler(async (req: AuthenticatedRequest, res) => {
    const { page = '1', limit = '20', search, userId } = req.query;
    
    const skip = (parseInt(page as string) - 1) * parseInt(limit as string);
    const take = parseInt(limit as string);

    const where: any = {
      isPublic: true,
    };

    // If user is logged in, also show their private palettes
    if (req.user) {
      where.OR = [
        { isPublic: true },
        { userId: req.user.id },
      ];
    }

    if (search) {
      where.AND = where.AND || [];
      where.AND.push({
        OR: [
          { name: { contains: search as string, mode: 'insensitive' } },
          { description: { contains: search as string, mode: 'insensitive' } },
        ],
      });
    }

    if (userId) {
      where.userId = userId as string;
      // Only show user's public palettes unless it's the current user
      if (!req.user || req.user.id !== userId) {
        delete where.OR;
        where.isPublic = true;
      }
    }

    const [palettes, total] = await Promise.all([
      prisma.palette.findMany({
        where,
        skip,
        take,
        orderBy: { createdAt: 'desc' },
        include: {
          user: {
            select: {
              id: true,
              username: true,
              displayName: true,
              avatarUrl: true,
            },
          },
          colors: {
            orderBy: { position: 'asc' },
          },
          _count: {
            select: { colors: true },
          },
        },
      }),
      prisma.palette.count({ where }),
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

// Get single palette
router.get(
  '/:id',
  optionalAuth,
  asyncHandler(async (req: AuthenticatedRequest, res) => {
    const { id } = req.params;

    const palette = await prisma.palette.findUnique({
      where: { id },
      include: {
        user: {
          select: {
            id: true,
            username: true,
            displayName: true,
            avatarUrl: true,
          },
        },
        colors: {
          orderBy: { position: 'asc' },
        },
      },
    });

    if (!palette) {
      return res.status(404).json({
        success: false,
        error: 'Palette not found',
      });
    }

    // Check if user can access private palette
    if (!palette.isPublic && (!req.user || req.user.id !== palette.userId)) {
      return res.status(403).json({
        success: false,
        error: 'Access denied',
      });
    }

    res.json({
      success: true,
      data: palette,
    });
  })
);

// Create palette
router.post(
  '/',
  authenticate,
  asyncHandler(async (req: AuthenticatedRequest, res) => {
    const data = paletteSchema.parse(req.body);

    const palette = await prisma.palette.create({
      data: {
        name: data.name,
        description: data.description,
        isPublic: data.isPublic ?? false,
        userId: req.user!.id,
        colors: data.colors ? {
          create: data.colors.map((color, index) => {
            const rgb = hexToRgb(color.hex);
            const hsl = rgbToHsl(rgb.r, rgb.g, rgb.b);
            return {
              hexValue: color.hex.toUpperCase(),
              rgbR: rgb.r,
              rgbG: rgb.g,
              rgbB: rgb.b,
              hslH: hsl.h,
              hslS: hsl.s,
              hslL: hsl.l,
              name: color.name,
              position: color.position ?? index,
            };
          }),
        } : undefined,
      },
      include: {
        colors: {
          orderBy: { position: 'asc' },
        },
        user: {
          select: {
            id: true,
            username: true,
            displayName: true,
          },
        },
      },
    });

    res.status(201).json({
      success: true,
      data: palette,
      message: 'Palette created successfully',
    });
  })
);

// Update palette
router.put(
  '/:id',
  authenticate,
  asyncHandler(async (req: AuthenticatedRequest, res) => {
    const { id } = req.params;
    const data = paletteSchema.partial().parse(req.body);

    const existing = await prisma.palette.findUnique({
      where: { id },
    });

    if (!existing) {
      return res.status(404).json({
        success: false,
        error: 'Palette not found',
      });
    }

    if (existing.userId !== req.user!.id) {
      return res.status(403).json({
        success: false,
        error: 'Not authorized to update this palette',
      });
    }

    const palette = await prisma.palette.update({
      where: { id },
      data: {
        name: data.name,
        description: data.description,
        isPublic: data.isPublic,
      },
      include: {
        colors: {
          orderBy: { position: 'asc' },
        },
      },
    });

    res.json({
      success: true,
      data: palette,
      message: 'Palette updated successfully',
    });
  })
);

// Delete palette
router.delete(
  '/:id',
  authenticate,
  asyncHandler(async (req: AuthenticatedRequest, res) => {
    const { id } = req.params;

    const existing = await prisma.palette.findUnique({
      where: { id },
    });

    if (!existing) {
      return res.status(404).json({
        success: false,
        error: 'Palette not found',
      });
    }

    if (existing.userId !== req.user!.id) {
      return res.status(403).json({
        success: false,
        error: 'Not authorized to delete this palette',
      });
    }

    await prisma.palette.delete({
      where: { id },
    });

    res.json({
      success: true,
      message: 'Palette deleted successfully',
    });
  })
);

// Add color to palette
router.post(
  '/:id/colors',
  authenticate,
  asyncHandler(async (req: AuthenticatedRequest, res) => {
    const { id } = req.params;
    const colorSchema = z.object({
      hex: z.string().regex(/^#[0-9A-Fa-f]{6}$/),
      name: z.string().optional(),
      position: z.number().int().min(0).optional(),
    });
    
    const data = colorSchema.parse(req.body);

    const palette = await prisma.palette.findUnique({
      where: { id },
    });

    if (!palette) {
      return res.status(404).json({
        success: false,
        error: 'Palette not found',
      });
    }

    if (palette.userId !== req.user!.id) {
      return res.status(403).json({
        success: false,
        error: 'Not authorized',
      });
    }

    const rgb = hexToRgb(data.hex);
    const hsl = rgbToHsl(rgb.r, rgb.g, rgb.b);

    const color = await prisma.color.create({
      data: {
        paletteId: id,
        hexValue: data.hex.toUpperCase(),
        rgbR: rgb.r,
        rgbG: rgb.g,
        rgbB: rgb.b,
        hslH: hsl.h,
        hslS: hsl.s,
        hslL: hsl.l,
        name: data.name,
        position: data.position ?? 0,
      },
    });

    res.status(201).json({
      success: true,
      data: color,
    });
  })
);

export { router as paletteRouter };
