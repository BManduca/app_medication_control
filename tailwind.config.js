/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/templates/**/*.{html,jinja,jinja2}", // captura arquivos Jinja e HTML
    "./app/**/*.py", // captura strings de classe em rotas ou macros Python
    "./app/static/js/**/*.js", // se você tiver scripts JS com classes Tailwind
  ],
  darkMode: 'class',
  theme: {
    extend: {
      screens: {}
    },
  },
  plugins: [],
}