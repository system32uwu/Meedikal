module.exports = {
  purge: ["./src/**/*.html", "./src/**/*.tsx"],
  darkMode: "class", // false, 'media' or 'class'
  theme: {
    extend: {
      colors: {
        turqoise: "#00C4BA",
        "pastel-skyblue": "#B2E1F4",
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
