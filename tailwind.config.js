/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/templates/*.html"],
  theme: {
    extend: {
      colors:{
        requiredfield:'#ff0000',
      },
    },
  },
  plugins: [],
}

