# Lital & Gilad Explore Norway

A static GitHub Pages travel website for an Oslo-to-Bergen Norway road trip. It uses only HTML5, CSS3, and vanilla JavaScript. No Node.js, backend, or build step is required.

## Deploy to GitHub Pages
1. Commit and push these files to GitHub.
2. In the repository settings, open **Pages**.
3. Select **Deploy from a branch** and choose the branch plus `/ (root)`.
4. Visit `https://username.github.io/repository-name/`.

## Add manuscript content
Each chapter page has reusable sections: Story, Question, Interesting facts, Reflection, Gallery, and Map notes. Replace placeholder paragraphs directly in the matching `.html` file.

## Add photos
Place images in the relevant folder under `photos/`, for example:

```text
photos/day01/vigeland/
photos/oslo/cover.jpg
photos/trolltunga/ringedalsvatnet-01.jpg
```

Then add image paths to `data/photo-manifest.js` under the chapter key. GitHub Pages is static and cannot securely list folder contents at runtime, so the manifest is the lightweight static index that lets galleries load automatically without page edits.

Example:

```js
window.PHOTO_MANIFEST = {
  oslo: [
    { src: 'photos/oslo/opera-house.jpg', alt: 'Oslo Opera House at sunset' }
  ]
};
```

## Add a new chapter
1. Copy an existing chapter HTML file.
2. Update title, metadata, hero path, JSON-LD, and `data-gallery` key.
3. Add the page to navigation on all pages and to `sitemap.xml`.
4. Add a matching key in `data/photo-manifest.js`.

## Customize SEO
Every page includes title, description, keywords, canonical URL, Open Graph tags, Twitter Card tags, and JSON-LD. Update these in the `<head>` and structured data blocks when final text is available.
