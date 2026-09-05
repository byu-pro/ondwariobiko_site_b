const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..");
const outDir = path.join(root, "dist");

const excludedDirs = new Set([
  ".git",
  ".github",
  ".vscode",
  "dist",
  "node_modules",
  "scratch",
  "scripts",
  "source-files"
]);

const copiedExtensions = new Set([
  ".jpg",
  ".jpeg",
  ".png",
  ".gif",
  ".svg",
  ".webp",
  ".ico",
  ".woff",
  ".woff2",
  ".ttf",
  ".eot",
  ".otf",
  ".mp4",
  ".webm",
  ".ogv",
  ".php",
  ".webmanifest"
]);

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

function cleanDir(dir) {
  fs.rmSync(dir, { recursive: true, force: true });
  ensureDir(dir);
}

function listFiles(dir, files = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (excludedDirs.has(entry.name)) continue;

    const absolute = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      listFiles(absolute, files);
    } else {
      files.push(absolute);
    }
  }

  return files;
}

function relativeToRoot(file) {
  return path.relative(root, file).replace(/\\/g, "/");
}

function stripHtmlComments(html) {
  return html.replace(/<!--(?!\[if).*?-->/gs, "");
}

function minifyHtml(html) {
  return stripHtmlComments(html)
    .replace(/>\s+</g, "><")
    .replace(/\s{2,}/g, " ")
    .replace(/\s*(=)\s*/g, "$1")
    .trim();
}

function stripCssComments(css) {
  return css.replace(/\/\*[\s\S]*?\*\//g, "");
}

function minifyCss(css) {
  return stripCssComments(css)
    .replace(/\s+/g, " ")
    .replace(/\s*([{}:;,>+~])\s*/g, "$1")
    .replace(/;}/g, "}")
    .replace(/\b0(px|em|rem|%)\b/g, "0")
    .trim();
}

function minifyJs(js) {
  // Safely strip block comments /* ... */
  let output = js.replace(/\/\*[\s\S]*?\*\//g, "");
  // Safely strip standalone line comments starting with //
  output = output.replace(/^[ \t]*\/\/[^\r\n]*/gm, "");
  return output.trim();
}

function rewriteHtmlReferences(html) {
  const version = '1775953000';
  return html
    .replace(/css\/loaders\/loader\.css(\?[^"']*)?/g, `css/loaders/loader.min.css?v=${version}`)
    .replace(/css\/plugins\.css(\?[^"']*)?/g, `css/plugins.min.css?v=${version}`)
    .replace(/css\/main\.css(\?[^"']*)?/g, `css/main.min.css?v=${version}`)
    .replace(/js\/app\.js(\?[^"']*)?/g, `js/app.min.js?v=${version}`)
    .replace(/js\/libs\.min\.js(\?[^"']*)?/g, `js/libs.min.js?v=${version}`);
}

function writeFile(relative, content) {
  const destination = path.join(outDir, relative);
  ensureDir(path.dirname(destination));
  fs.writeFileSync(destination, content);
}

function copyFile(file, relative) {
  const destination = path.join(outDir, relative);
  ensureDir(path.dirname(destination));
  fs.copyFileSync(file, destination);
}

function buildFile(file) {
  const relative = relativeToRoot(file);
  const ext = path.extname(file).toLowerCase();

  if (ext === ".html") {
    const html = fs.readFileSync(file, "utf8");
    writeFile(relative, minifyHtml(rewriteHtmlReferences(html)));
    return;
  }

  if (ext === ".css") {
    const css = fs.readFileSync(file, "utf8");
    if (relative === "css/loaders/loader.css") {
      writeFile("css/loaders/loader.min.css", minifyCss(css));
    } else if (relative === "css/plugins.css") {
      writeFile("css/plugins.min.css", minifyCss(css));
    } else if (relative === "css/main.css") {
      writeFile("css/main.min.css", minifyCss(css));
    } else if (!relative.endsWith(".min.css")) {
      writeFile(relative, minifyCss(css));
    }
    return;
  }

  if (ext === ".js") {
    const js = fs.readFileSync(file, "utf8");
    if (relative === "js/app.js") {
      writeFile("js/app.min.js", minifyJs(js));
    } else if (relative === "js/app.min.js") {
      return;
    } else if (relative.endsWith(".min.js")) {
      copyFile(file, relative);
    } else {
      writeFile(relative, minifyJs(js));
    }
    return;
  }

  if (copiedExtensions.has(ext) || path.basename(file).startsWith(".")) {
    copyFile(file, relative);
  }
}

cleanDir(outDir);
for (const file of listFiles(root)) {
  buildFile(file);
}

console.log(`Protected production build written to ${path.relative(root, outDir)}`);
