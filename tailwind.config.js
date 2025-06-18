/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/templates/**/*.html", // inclui todos os arquivos html em subpastas
    "./app/templates/**/**/*.html" // segurança extra para subpastas mais profundas
  ],
  darkMode: 'class',
  theme: {
    extend: {},
  },
  plugins: [],
}

