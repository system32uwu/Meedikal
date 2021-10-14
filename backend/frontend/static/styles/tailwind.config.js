module.exports = {
  purge: {
    enabled: false,
    content: ["../../**/*.html"],
  },
  darkMode: "class", // false, 'media' or 'class'
  theme: {
    extend: {
      colors: {
        turqoise: "#00C4BA",
        skyblue: "#B2E1F4",
        "darker-skyblue": '#A2D3E7',
        "hard-blue": "#1786A3",   
      },
      fontFamily: {
        overpass: ["Overpass", "sans-serif"],
      },
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
};
