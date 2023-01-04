/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './node_modules/flowbite/**/*.js'
  ],
  theme: {
    extend: {
      colors: {
        'main-dark': '#1C1C1C',
      },
      borderWidth: {
        '1': '1px',
      },
      fontFamily: {
        'font-1': ['Poppins', 'sans-serif'],
        'font-2': ['Roboto', 'sans-serif'],
      }
    },
  },
  plugins: [
    require('flowbite/plugin')
  ],
}
