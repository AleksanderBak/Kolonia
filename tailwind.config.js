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
        'dashboard-1': '#E3F5FF',
        'dashboard-2': '#E5ECF6',
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
