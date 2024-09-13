/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./templates/**/*.html'],
  theme: {
    fontFamily: {
      'sans': ['Montserrat', 'sans-serif'],
      'serif': ['Garamond', 'serif'],
      'mono': ['Lato', 'monospace'],
    },
    extend: {
       fontFamily: {
        'montserrat': ['Montserrat'],
        'lato': ['Lato'],
        'garamond': ['Garamond']
      }
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}

