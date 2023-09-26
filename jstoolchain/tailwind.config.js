/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["../greenhouse/templates/**/*.html"],
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/forms'),                // new
  ],
}

