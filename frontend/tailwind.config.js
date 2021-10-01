module.exports = {
  purge: ["./src/**/*.html", "./src/**/*.tsx"],
  darkMode: 'class', // false, 'media' or 'class'
  theme: {
    extend: {
      colors:{
        'turqoise': '#00C4BA'
      },
      fontFamily:{
        'overpass': ['Overpass', 'sans-serif']
      }
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
};
