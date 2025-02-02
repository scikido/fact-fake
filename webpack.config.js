const path = require("path");

module.exports = {
    entry: "./chartBundle.js",
    output: {
        filename: "chart.bundle.js",
        path: path.resolve(__dirname, "dist"),
    },
    mode: "production"
};
