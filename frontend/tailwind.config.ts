import type { Config } from 'tailwindcss';

export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        ink: '#17211b',
        moss: '#31533f',
        sage: '#8aa394',
        paper: '#f7f4ed',
        coral: '#d46a4c',
        gold: '#c79a3d',
      },
      boxShadow: {
        soft: '0 18px 50px rgb(23 33 27 / 0.12)',
      },
    },
  },
  plugins: [],
} satisfies Config;
