const fs = require("node:fs");
const path = require("node:path");

const projectRoot = path.resolve(__dirname, "..");
const ignoredDirectories = new Set(["node_modules", ".expo", "dist", "web-build"]);
const problems = [];

function walk(directory) {
  const entries = fs.readdirSync(directory, { withFileTypes: true });
  const files = [];

  for (const entry of entries) {
    if (entry.isDirectory()) {
      if (!ignoredDirectories.has(entry.name)) {
        files.push(...walk(path.join(directory, entry.name)));
      }
      continue;
    }

    files.push(path.join(directory, entry.name));
  }

  return files;
}

const typeScriptFiles = walk(projectRoot)
  .filter((filePath) => [".ts", ".tsx"].includes(path.extname(filePath)))
  .map((filePath) => path.relative(projectRoot, filePath));

if (typeScriptFiles.length > 0) {
  problems.push(`TypeScript files remain: ${typeScriptFiles.join(", ")}`);
}

if (fs.existsSync(path.join(projectRoot, "tsconfig.json"))) {
  problems.push("tsconfig.json remains in the mobile project");
}

const packageJsonPath = path.join(projectRoot, "package.json");
const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, "utf8"));
const scripts = packageJson.scripts ?? {};
const directDependencies = {
  ...(packageJson.dependencies ?? {}),
  ...(packageJson.devDependencies ?? {})
};

if (scripts.typecheck) {
  problems.push("package.json still defines the typecheck script");
}

const typeScriptDependencies = Object.keys(directDependencies).filter(
  (name) => name === "typescript" || name.startsWith("@types/")
);

if (typeScriptDependencies.length > 0) {
  problems.push(`TypeScript dependencies remain: ${typeScriptDependencies.join(", ")}`);
}

if (problems.length > 0) {
  console.error("JavaScript-only frontend verification failed:");
  for (const problem of problems) {
    console.error(`- ${problem}`);
  }
  process.exit(1);
}

console.log("JavaScript-only frontend verification passed.");
