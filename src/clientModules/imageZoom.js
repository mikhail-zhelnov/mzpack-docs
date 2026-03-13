import mediumZoom from 'medium-zoom';

export function onRouteDidUpdate() {
  const timeoutId = setTimeout(() => {
    mediumZoom('article img', {
      background: 'rgba(0, 0, 0, 0.85)',
      margin: 24,
    });
  }, 100);
  return () => clearTimeout(timeoutId);
}
