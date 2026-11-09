/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        bmtc: {
          dark: '#001B2A',    // Main dark text/backgrounds
          navy: '#18263B',    // Secondary dark
          blue: '#415A77',    // Primary buttons/accents
          sage: '#77807A',    // Success/Green replacements
          tan: '#D4C4A8',     // Card backgrounds
          cream: '#F4F1DE',   // Main app background
        }
      }
    },
  },
  plugins: [],
}