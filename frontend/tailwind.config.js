/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        navy: {
          950: "#0a0e1a",
          900: "#0f1420",
          800: "#151b2b",
          700: "#1c2438",
        },
        gain: "#00c896",
        loss: "#ff4d6d",
      },
    },
  },
  plugins: [],
}