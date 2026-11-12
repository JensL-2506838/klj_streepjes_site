
import js from "@eslint/js";
import globals from "globals";

export default [
  {
    ignores: [
      "node_modules/**",
      "klj_site/database/**",
      "coverage/**",
      "dist/**",
    ],
  },
  {
    files: ["klj_site/UI/logic/**/*.js"],
    languageOptions: {
      ecmaVersion: "latest",
      sourceType: "module",
      globals: globals.browser,
    },
    ...js.configs.recommended,
  },
];
