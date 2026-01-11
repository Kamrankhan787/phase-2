/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx}",       // Next.js app folder
    "./pages/**/*.{js,ts,jsx,tsx}",     // optional, if you use pages
    "./components/**/*.{js,ts,jsx,tsx}",// your components
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
