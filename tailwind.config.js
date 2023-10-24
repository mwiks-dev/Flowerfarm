/** @type {import('tailwindcss').Config} */
module.exports = {
  mode: 'jit',
  content: ["./greenhouse/templates/**/*.html"],
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/forms'),              
  ],
}

