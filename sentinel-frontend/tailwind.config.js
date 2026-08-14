/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        canvas: '#0A0E14',
        surface: {
          DEFAULT: '#10151D',
          raised: '#161C26',
          hover: '#1B222D',
        },
        border: {
          DEFAULT: '#212A38',
          muted: '#171E29',
        },
        ink: {
          DEFAULT: '#E7ECF3',
          secondary: '#8291A3',
          muted: '#56626F',
        },
        accent: {
          DEFAULT: '#2FDFC7',
          dim: '#1B8577',
          glow: 'rgba(47, 223, 199, 0.16)',
        },
        critical: '#FF4D4F',
        high: '#FF9142',
        caution: '#F4C542',
        safe: '#34D399',
        info: '#4EA1FF',
      },
      fontFamily: {
        display: ['"Space Grotesk"', 'sans-serif'],
        body: ['Inter', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'monospace'],
      },
      boxShadow: {
        panel: '0 1px 0 0 rgba(255,255,255,0.02) inset, 0 8px 24px -12px rgba(0,0,0,0.5)',
        glow: '0 0 0 1px rgba(47,223,199,0.25), 0 0 24px -4px rgba(47,223,199,0.35)',
      },
      backgroundImage: {
        grid: 'linear-gradient(rgba(255,255,255,0.025) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.025) 1px, transparent 1px)',
      },
    },
  },
  plugins: [],
};
