
import js from "@eslint/js";
import globals from "globals";

export default [
  {
    ignores: [
      "node_modules/**",
      "site/database/**",
      "coverage/**",
      "dist/**",
    ],
  },
  {
    files: ["site/UI/logic/**/*.js"],
    languageOptions: {
      ecmaVersion: "latest",
      sourceType: "module",
      globals: globals.browser,
    },
    ...js.configs.recommended,
  },
];
