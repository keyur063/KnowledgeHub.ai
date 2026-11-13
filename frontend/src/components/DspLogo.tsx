import React from 'react';
import { Brain } from 'lucide-react';

export interface DspLogoProps {
  /**
   * Presentation variant:
   * - 'card': Original cropped card container.
   * - 'transparent': Clean transparent background.
   * - 'badge': Square icon badge with rounded corners.
   * - 'full': Wide landscape banner with icon and text.
   */
  variant?: 'card' | 'transparent' | 'badge' | 'full';
  /**
   * Predefined size presets or specific height in px.
   */
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl' | number;
  className?: string;
  style?: React.CSSProperties;
  alt?: string;
  withGlow?: boolean;
}

const HEIGHT_MAP: Record<string, number> = {
  xs: 20,
  sm: 28,
  md: 36,
  lg: 48,
  xl: 64,
};

export default function DspLogo({
  variant = 'card',
  size = 'md',
  className = '',
  style = {},
  alt = 'KnowledgeHub AI Logo',
  withGlow = false,
}: DspLogoProps) {
  const height = typeof size === 'number' ? size : HEIGHT_MAP[size] || 36;
  const iconSize = Math.max(14, Math.round(height * 0.58));

  return (
    <div
      role="img"
      aria-label={alt}
      className={`dsp-brand-logo dsp-logo-${variant} ${className}`}
      style={{
        height: `${height}px`,
        width: variant === 'full' ? 'auto' : `${height}px`,
        display: 'inline-flex',
        alignItems: 'center',
        justifyContent: 'center',
        borderRadius: variant === 'badge' ? `${Math.max(4, Math.round(height * 0.22))}px` : '8px',
        background: variant === 'transparent' ? 'transparent' : 'rgba(59, 130, 246, 0.12)',
        border: variant === 'transparent' ? 'none' : '1px solid rgba(59, 130, 246, 0.25)',
        color: '#2563eb',
        boxShadow: withGlow ? '0 0 16px rgba(37, 99, 235, 0.35)' : undefined,
        flexShrink: 0,
        ...style,
      }}
    >
      <Brain style={{ width: iconSize, height: iconSize, color: '#2563eb' }} />
      {variant === 'full' && (
        <span
          style={{
            marginLeft: 8,
            fontWeight: 700,
            fontSize: `${Math.round(height * 0.42)}px`,
            color: '#0f172a',
            letterSpacing: '-0.02em',
          }}
        >
          KnowledgeHub AI
        </span>
      )}
    </div>
  );
}
