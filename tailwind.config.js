const colors = require('tailwindcss/colors')

module.exports = {
  purge: [],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      colors: {
        teal: colors.teal,
        mint: {
          light: "#e9f9fd",
          DEFAULT: "#17a8c9",
          dark: "#128aa6",
        },
        sogang: "#b30000",
      },
      boxShadow: {
        "neu": "15px 15px 30px #e6e6e6, -15px -15px 30px #ffffff",
      },

      maxWidth:{
        "10": "2.5rem",
        "20px": "20px",
        "30px": "30px",
        "50px": "50px",
        "70px": "70px",
      },
      minWidth:{
        "60%": "60%",
        "70%": "70%",
        "80%": "80%",
      }
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
