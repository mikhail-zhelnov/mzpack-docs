import mediumZoom from 'medium-zoom';

export function onRouteDidUpdate() {
  const article = document.querySelector('article');
  if (!article) return undefined;

  const zoom = mediumZoom({
    background: 'rgba(0, 0, 0, 0.85)',
    margin: 24,
  });

  // Attach zoom to any not-yet-attached <img> in the article.
  const attachNew = () => {
    const fresh = [...article.querySelectorAll('img')].filter(
      (img) => !img.dataset.zoomAttached,
    );
    fresh.forEach((img) => {
      img.dataset.zoomAttached = 'true';
    });
    if (fresh.length) zoom.attach(...fresh);
  };

  // IdealImage renders an <svg> placeholder and swaps in the real <img> only
  // once the figure scrolls into view (lazy-load), so the image usually mounts
  // AFTER this hook first runs. A single early attach (the previous approach)
  // therefore found no <img> and nothing was zoomable. Attach what's present
  // now, then watch the article subtree and attach each <img> as it appears.
  attachNew();
  const observer = new MutationObserver(attachNew);
  observer.observe(article, {childList: true, subtree: true});

  return () => {
    observer.disconnect();
    zoom.detach();
  };
}
