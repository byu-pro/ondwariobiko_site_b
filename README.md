# ondwariobiko_site_b
Site B

## Protected Production Build

Run `npm run build` before publishing. It creates a `dist/` folder with minified HTML, CSS, and JavaScript, strips comments, and rewrites pages to use the minified CSS/JS assets.

Keep editing the source files in the project root. Publish the contents of `dist/` when you want the public website code to be harder to inspect or reuse.

GitHub Actions also runs this build on every push to `main` and deploys the protected `dist/` output to GitHub Pages.
