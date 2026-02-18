import { Request } from 'express';

export interface AuthenticatedRequest extends Request {
  user?: {
    id: string;
    email: string;
    username: string;
  };
}

export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

export interface ColorInput {
  hex: string;
  name?: string;
}

export interface PaletteInput {
  name: string;
  description?: string;
  isPublic?: boolean;
  colors: ColorInput[];
}

export interface CreatePaletteBody {
  name: string;
  description?: string;
  isPublic?: boolean;
  colors?: Array<{
    hex: string;
    name?: string;
    position?: number;
  }>;
}
