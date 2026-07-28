/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#FF9EB5',
          light: '#FFD1E0',
        },
        secondary: {
          DEFAULT: '#7ED7A7',
          light: '#B8EBCE',
        },
        danger: '#FF6B6B',
        success: '#51CF66',
      },
      backdropBlur: {
        '20': '20px',
      },
      borderRadius: {
        '14': '14px',
        '16': '16px',
        '20': '20px',
        '24': '24px',
      }
    },
  },
  plugins: [],
}
