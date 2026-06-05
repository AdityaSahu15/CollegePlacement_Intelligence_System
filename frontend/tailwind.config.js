/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        bg: {
          primary: '#0f172a',
          secondary: '#1e293b',
          tertiary: '#334155',
        },
        text: {
          primary: '#f8fafc',
          secondary: '#cbd5e1',
        },
        accent: {
          primary: '#3b82f6',
          secondary: '#8b5cf6',
        },
        glass: {
          bg: 'rgba(30, 41, 59, 0.7)',
          border: 'rgba(255, 255, 255, 0.1)'
        }
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        heading: ['Outfit', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
