import { Router } from 'express';
import { z } from 'zod';
import { asyncHandler } from '../middleware/error_handler';
import { 
  generateHarmonies, 
  checkWCAGCompliance, 
  generateGradient,
  hexToRgb,
  rgbToHsl,
  rgbToHex,
  hslToRgb
} from '../utils/color';

const router = Router();

// Generate color harmonies
router.post(
  '/harmony',
  asyncHandler(async (req, res) => {
    const schema = z.object({
      hex: z.string().regex(/^#[0-9A-Fa-f]{6}$/),
    });

    const { hex } = schema.parse(req.body);
    const harmonies = generateHarmonies(hex.toUpperCase());

    res.json({
      success: true,
      data: {
        baseColor: hex.toUpperCase(),
        harmonies,
      },
    });
  })
);

// Check contrast ratio (WCAG)
router.post(
  '/contrast',
  asyncHandler(async (req, res) => {
    const schema = z.object({
      foreground: z.string().regex(/^#[0-9A-Fa-f]{6}$/),
      background: z.string().regex(/^#[0-9A-Fa-f]{6}$/),
    });

    const { foreground, background } = schema.parse(req.body);
    const compliance = checkWCAGCompliance(
      foreground.toUpperCase(),
      background.toUpperCase()
    );

    res.json({
      success: true,
      data: {
        foreground: foreground.toUpperCase(),
        background: background.toUpperCase(),
        compliance,
      },
    });
  })
);

// Generate gradient
router.post(
  '/gradient',
  asyncHandler(async (req, res) => {
    const schema = z.object({
      startColor: z.string().regex(/^#[0-9A-Fa-f]{6}$/),
      endColor: z.string().regex(/^#[0-9A-Fa-f]{6}$/),
      steps: z.number().int().min(2).max(20).default(5),
    });

    const { startColor, endColor, steps } = schema.parse(req.body);
    const gradient = generateGradient(
      startColor.toUpperCase(),
      endColor.toUpperCase(),
      steps
    );

    res.json({
      success: true,
      data: {
        startColor: startColor.toUpperCase(),
        endColor: endColor.toUpperCase(),
        steps,
        gradient,
      },
    });
  })
);

// Color blindness simulator
router.post(
  '/colorblind',
  asyncHandler(async (req, res) => {
    const schema = z.object({
      hex: z.string().regex(/^#[0-9A-Fa-f]{6}$/),
      type: z.enum(['protanopia', 'deuteranopia', 'tritanopia', 'achromatopsia']).optional(),
    });

    const { hex, type } = schema.parse(req.body);
    const rgb = hexToRgb(hex);

    // Simplified color blindness simulation matrices
    const simulations: Record<string, (r: number, g: number, b: number) => [number, number, number]> = {
      // Red-blind
      protanopia: (r, g, b) => [
        0.567 * r + 0.433 * g,
        0.558 * r + 0.442 * g,
        0.242 * g + 0.758 * b,
      ],
      // Green-blind
      deuteranopia: (r, g, b) => [
        0.625 * r + 0.375 * g,
        0.7 * r + 0.3 * g,
        0.3 * g + 0.7 * b,
      ],
      // Blue-blind
      tritanopia: (r, g, b) => [
        0.95 * r + 0.05 * g,
        0.433 * g + 0.567 * b,
        0.475 * g + 0.525 * b,
      ],
      // Complete color blindness
      achromatopsia: (r, g, b) => {
        const gray = 0.299 * r + 0.587 * g + 0.114 * b;
        return [gray, gray, gray];
      },
    };

    const results: Record<string, string> = {};

    if (type && simulations[type]) {
      const [r, g, b] = simulations[type](rgb.r, rgb.g, rgb.b);
      results[type] = rgbToHex(Math.round(r), Math.round(g), Math.round(b));
    } else {
      // Return all simulations
      for (const [simType, fn] of Object.entries(simulations)) {
        const [r, g, b] = fn(rgb.r, rgb.g, rgb.b);
        results[simType] = rgbToHex(Math.round(r), Math.round(g), Math.round(b));
      }
    }

    res.json({
      success: true,
      data: {
        original: hex.toUpperCase(),
        simulations: results,
      },
    });
  })
);

// Convert between color formats
router.post(
  '/convert',
  asyncHandler(async (req, res) => {
    const schema = z.union([
      z.object({
        hex: z.string().regex(/^#[0-9A-Fa-f]{6}$/),
      }),
      z.object({
        rgb: z.object({
          r: z.number().int().min(0).max(255),
          g: z.number().int().min(0).max(255),
          b: z.number().int().min(0).max(255),
        }),
      }),
      z.object({
        hsl: z.object({
          h: z.number().min(0).max(360),
          s: z.number().min(0).max(100),
          l: z.number().min(0).max(100),
        }),
      }),
    ]);

    const input = schema.parse(req.body);

    let hex: string;
    let rgb: { r: number; g: number; b: number };
    let hsl: { h: number; s: number; l: number };

    if ('hex' in input) {
      hex = input.hex.toUpperCase();
      rgb = hexToRgb(hex);
      hsl = rgbToHsl(rgb.r, rgb.g, rgb.b);
    } else if ('rgb' in input) {
      rgb = input.rgb;
      hex = rgbToHex(rgb.r, rgb.g, rgb.b);
      hsl = rgbToHsl(rgb.r, rgb.g, rgb.b);
    } else {
      hsl = input.hsl;
      rgb = hslToRgb(hsl.h, hsl.s, hsl.l);
      hex = rgbToHex(rgb.r, rgb.g, rgb.b);
    }

    res.json({
      success: true,
      data: {
        hex,
        rgb,
        hsl,
      },
    });
  })
);

export { router as toolRouter };
