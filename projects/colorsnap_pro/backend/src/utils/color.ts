// Color utility functions

export interface RGB {
  r: number;
  g: number;
  b: number;
}

export interface HSL {
  h: number;
  s: number;
  l: number;
}

export interface ColorFormats {
  hex: string;
  rgb: RGB;
  hsl: HSL;
}

export function hexToRgb(hex: string): RGB {
  const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  if (!result) {
    throw new Error('Invalid hex color');
  }
  return {
    r: parseInt(result[1], 16),
    g: parseInt(result[2], 16),
    b: parseInt(result[3], 16),
  };
}

export function rgbToHex(r: number, g: number, b: number): string {
  const toHex = (n: number) => {
    const hex = Math.max(0, Math.min(255, n)).toString(16);
    return hex.length === 1 ? '0' + hex : hex;
  };
  return `#${toHex(r)}${toHex(g)}${toHex(b)}`.toUpperCase();
}

export function rgbToHsl(r: number, g: number, b: number): HSL {
  r /= 255;
  g /= 255;
  b /= 255;

  const max = Math.max(r, g, b);
  const min = Math.min(r, g, b);
  let h = 0;
  let s = 0;
  const l = (max + min) / 2;

  if (max !== min) {
    const d = max - min;
    s = l > 0.5 ? d / (2 - max - min) : d / (max + min);

    switch (max) {
      case r:
        h = ((g - b) / d + (g < b ? 6 : 0)) / 6;
        break;
      case g:
        h = ((b - r) / d + 2) / 6;
        break;
      case b:
        h = ((r - g) / d + 4) / 6;
        break;
    }
  }

  return {
    h: Math.round(h * 360),
    s: Math.round(s * 100),
    l: Math.round(l * 100),
  };
}

export function hslToRgb(h: number, s: number, l: number): RGB {
  h /= 360;
  s /= 100;
  l /= 100;

  let r: number, g: number, b: number;

  if (s === 0) {
    r = g = b = l;
  } else {
    const hue2rgb = (p: number, q: number, t: number) => {
      if (t < 0) t += 1;
      if (t > 1) t -= 1;
      if (t < 1 / 6) return p + (q - p) * 6 * t;
      if (t < 1 / 2) return q;
      if (t < 2 / 3) return p + (q - p) * (2 / 3 - t) * 6;
      return p;
    };

    const q = l < 0.5 ? l * (1 + s) : l + s - l * s;
    const p = 2 * l - q;

    r = hue2rgb(p, q, h + 1 / 3);
    g = hue2rgb(p, q, h);
    b = hue2rgb(p, q, h - 1 / 3);
  }

  return {
    r: Math.round(r * 255),
    g: Math.round(g * 255),
    b: Math.round(b * 255),
  };
}

export function generateHarmonies(hex: string): {
  complementary: string[];
  analogous: string[];
  triadic: string[];
  splitComplementary: string[];
  tetradic: string[];
} {
  const rgb = hexToRgb(hex);
  const hsl = rgbToHsl(rgb.r, rgb.g, rgb.b);

  // Complementary (opposite on color wheel)
  const complementary = [
    rgbToHex(...Object.values(hslToRgb((hsl.h + 180) % 360, hsl.s, hsl.l)) as [number, number, number]),
  ];

  // Analogous (adjacent colors)
  const analogous = [
    rgbToHex(...Object.values(hslToRgb((hsl.h - 30 + 360) % 360, hsl.s, hsl.l)) as [number, number, number]),
    hex,
    rgbToHex(...Object.values(hslToRgb((hsl.h + 30) % 360, hsl.s, hsl.l)) as [number, number, number]),
  ];

  // Triadic (evenly spaced, 120° apart)
  const triadic = [
    hex,
    rgbToHex(...Object.values(hslToRgb((hsl.h + 120) % 360, hsl.s, hsl.l)) as [number, number, number]),
    rgbToHex(...Object.values(hslToRgb((hsl.h + 240) % 360, hsl.s, hsl.l)) as [number, number, number]),
  ];

  // Split Complementary
  const splitComplementary = [
    hex,
    rgbToHex(...Object.values(hslToRgb((hsl.h + 150) % 360, hsl.s, hsl.l)) as [number, number, number]),
    rgbToHex(...Object.values(hslToRgb((hsl.h + 210) % 360, hsl.s, hsl.l)) as [number, number, number]),
  ];

  // Tetradic (rectangular, four colors)
  const tetradic = [
    hex,
    rgbToHex(...Object.values(hslToRgb((hsl.h + 90) % 360, hsl.s, hsl.l)) as [number, number, number]),
    rgbToHex(...Object.values(hslToRgb((hsl.h + 180) % 360, hsl.s, hsl.l)) as [number, number, number]),
    rgbToHex(...Object.values(hslToRgb((hsl.h + 270) % 360, hsl.s, hsl.l)) as [number, number, number]),
  ];

  return {
    complementary,
    analogous,
    triadic,
    splitComplementary,
    tetradic,
  };
}

// Calculate relative luminance
function getLuminance(r: number, g: number, b: number): number {
  const [rs, gs, bs] = [r, g, b].map((c) => {
    c = c / 255;
    return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
  });
  return 0.2126 * rs + 0.7152 * gs + 0.0722 * bs;
}

// Calculate contrast ratio between two colors
export function getContrastRatio(hex1: string, hex2: string): number {
  const rgb1 = hexToRgb(hex1);
  const rgb2 = hexToRgb(hex2);
  
  const l1 = getLuminance(rgb1.r, rgb1.g, rgb1.b);
  const l2 = getLuminance(rgb2.r, rgb2.g, rgb2.b);
  
  const lighter = Math.max(l1, l2);
  const darker = Math.min(l1, l2);
  
  return (lighter + 0.05) / (darker + 0.05);
}

// Check WCAG compliance
export function checkWCAGCompliance(hex1: string, hex2: string): {
  ratio: number;
  AA: boolean;
  AAA: boolean;
  AALarge: boolean;
  AAALarge: boolean;
} {
  const ratio = getContrastRatio(hex1, hex2);
  
  return {
    ratio: Math.round(ratio * 100) / 100,
    AA: ratio >= 4.5,
    AAA: ratio >= 7,
    AALarge: ratio >= 3,
    AAALarge: ratio >= 4.5,
  };
}

// Generate gradient between two colors
export function generateGradient(
  hex1: string, 
  hex2: string, 
  steps: number = 5
): string[] {
  const rgb1 = hexToRgb(hex1);
  const rgb2 = hexToRgb(hex2);
  const gradient: string[] = [];

  for (let i = 0; i < steps; i++) {
    const t = i / (steps - 1);
    const r = Math.round(rgb1.r + (rgb2.r - rgb1.r) * t);
    const g = Math.round(rgb1.g + (rgb2.g - rgb1.g) * t);
    const b = Math.round(rgb1.b + (rgb2.b - rgb1.b) * t);
    gradient.push(rgbToHex(r, g, b));
  }

  return gradient;
}

// Color name suggestions based on hue ranges
export function suggestColorName(hex: string): string[] {
  const rgb = hexToRgb(hex);
  const hsl = rgbToHsl(rgb.r, rgb.g, rgb.b);
  
  const hue = hsl.h;
  const saturation = hsl.s;
  const lightness = hsl.l;
  
  const names: string[] = [];
  
  // Descriptive terms based on lightness and saturation
  let descriptor = '';
  if (lightness < 15) descriptor = 'Dark ';
  else if (lightness > 85) descriptor = 'Light ';
  else if (saturation < 20) descriptor = 'Pale ';
  else if (saturation > 80) descriptor = 'Vivid ';
  else if (lightness > 60) descriptor = 'Soft ';
  else descriptor = 'Deep ';
  
  // Base color names based on hue
  if (hue >= 345 || hue < 15) names.push(`${descriptor}Red`, 'Crimson', 'Ruby');
  else if (hue >= 15 && hue < 45) names.push(`${descriptor}Orange`, 'Amber', 'Tangerine');
  else if (hue >= 45 && hue < 75) names.push(`${descriptor}Yellow`, 'Gold', 'Lemon');
  else if (hue >= 75 && hue < 105) names.push(`${descriptor}Lime`, 'Chartreuse', 'Spring Green');
  else if (hue >= 105 && hue < 135) names.push(`${descriptor}Green`, 'Emerald', 'Jade');
  else if (hue >= 135 && hue < 165) names.push(`${descriptor}Teal`, 'Mint', 'Seafoam');
  else if (hue >= 165 && hue < 195) names.push(`${descriptor}Cyan`, 'Turquoise', 'Aqua');
  else if (hue >= 195 && hue < 225) names.push(`${descriptor}Sky Blue`, 'Azure', 'Cerulean');
  else if (hue >= 225 && hue < 255) names.push(`${descriptor}Blue`, 'Sapphire', 'Cobalt');
  else if (hue >= 255 && hue < 285) names.push(`${descriptor}Purple`, 'Violet', 'Amethyst');
  else if (hue >= 285 && hue < 315) names.push(`${descriptor}Magenta`, 'Fuchsia', 'Orchid');
  else if (hue >= 315 && hue < 345) names.push(`${descriptor}Pink`, 'Rose', 'Coral');
  
  // Add neutral names for low saturation
  if (saturation < 15) {
    if (lightness < 25) names.push('Charcoal', 'Onyx', 'Jet Black');
    else if (lightness > 75) names.push('White', 'Snow', 'Ivory');
    else names.push('Gray', 'Silver', 'Slate');
  }
  
  return names.slice(0, 3);
}
